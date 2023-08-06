"""
PyTorch seems to store checkpoints in a weird zipfile that contains
a pickle file and a bunch of raw arrays. The pickle makes it a big security
risk to load other people's model weights, and unfortunately a lot of the
ML community uses such unsafe formats.

This is a module implementing loading for a decent subset of the format.
"""

import dataclasses
import functools
import operator
import pathlib
import warnings
import zipfile
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Tuple

import attr
import numpy as np
from marshmallow import fields

from .. import DefaultFirewall, Handler, Unpickler
from . import marshmallow as mext

storage_manager_var = ContextVar("storage_manager")


@contextmanager
def setting(contextvar: ContextVar, value: object):
    token = contextvar.set(value)
    try:
        yield
    finally:
        contextvar.reset(token)


class InvalidDTypeWarning(UserWarning):
    pass


@dataclasses.dataclass
class StoredTensor:
    storage: "StorageInfo"
    storage_offset: int
    size: Tuple[int]
    stride: Tuple[int]
    requires_grad: bool
    backward_hooks: object
    storage_manager: "StorageManager" = dataclasses.field(
        default_factory=lambda: storage_manager_var.get(None)
    )

    # do not add "object" to the list below, because then it will try to load
    # python objects using pickle
    ALLOWED_DTYPES = {
        "float16",
        "float32",
        "int8",
        "int16",
        "int32",
        "int64",
        "uint8",
        "uint16",
        "uint32",
        "uint64",
    }

    @functools.cached_property
    def dtype(self):
        dtype = self.storage.dtype
        if dtype not in self.ALLOWED_DTYPES:
            warnings.warn(f"not loading dtype {dtype!r}", InvalidDTypeWarning)
            return None

        return np.dtype(dtype).newbyteorder("<")

    @property
    def obj_key(self):
        return self.storage.key

    def _byte_size(self):
        return functools.reduce(operator.mul, self.size, self.dtype.itemsize)

    def _load_from_file(self, fileobj):
        byte_size = self._byte_size()
        fileobj.seek(self.storage_offset)
        buf: bytes = fileobj.read(byte_size)
        if len(buf) != byte_size:
            raise ValueError(f"expected {len(buf)} bytes, got {byte_size}")
        return self._load_from_buffer(buf)

    def _load_from_buffer(self, buffer):
        dt = self.dtype
        if dt is None:
            return

        return np.frombuffer(buffer, self.dtype).reshape(self.size)

    def _load_from_zipfile(self):
        if self.dtype is None:
            return

        with self.storage_manager.open(f"data/{self.obj_key}") as f:
            return self._load_from_file(f)

    @property
    def array(self):
        if self.dtype is None:
            raise AssertionError("invalid dtype")

        return self._load_from_zipfile()


@attr.s
class StorageInfo:
    dtype: str = attr.ib()
    key: str = attr.ib()


class StorageManager:
    def open(self, key: str):
        raise NotImplementedError


@attr.s
class StorageManagerZip(StorageManager):
    zip_file: zipfile.ZipFile = attr.ib()
    prefix: str = attr.ib(repr=False)

    def open(self, path: str):
        # ZipFile.open doesn't support 'b'...
        return self.zip_file.open(self.prefix + path, "r")


class StorageInfoField(mext.XTuple):
    def __init__(self, **kwargs):
        super().__init__((mext.XString(), mext.XString()), **kwargs)

    def _deserialize(self, value, attr, data, **kwargs):
        if type(value) is not tuple:
            raise fields.ValidationError

        value = value[1:3]
        value = super()._deserialize(value, attr, data, **kwargs)

        return StorageInfo(*value)


class StoredTensorHandler(mext.BaseMarshmallowHandler):
    imports = {"torch._utils:_rebuild_tensor_v2": StoredTensor}

    class Schema(mext.BaseMarshmallowHandler.Schema):
        storage = StorageInfoField()
        storage_offset = fields.Integer()
        size = mext.XListAsPyTuple(fields.Integer())
        stride = mext.XListAsPyTuple(fields.Integer())
        requires_grad = fields.Boolean()
        backward_hooks = fields.Raw()


class StorageHandler(Handler):
    imports = {
        "torch:HalfStorage": "float16",
        "torch:FloatStorage": "float32",
        "torch:IntStorage": "int32",
        "torch:LongStorage": "int64",
    }
    imports_register_instance = False


class PyTorchFirewall(DefaultFirewall):
    def get_autoregister_handlers(self):
        handlers = super().get_autoregister_handlers()
        handlers.append(StorageHandler())
        handlers.append(StoredTensorHandler())
        return handlers


class MyUnpickler(Unpickler):
    def persistent_load(self, value):
        return value


def fake_torch_load_zipped(
    zip_file: zipfile.ZipFile,
    firewall: DefaultFirewall = None,
    Unpickler=MyUnpickler,
):
    """
    from zipfile import ZipFile

    zf = ZipFile("/data/ml/sd-v1-4.ckpt")
    zipped = fake_torch_load_zipped(zf)
    """

    if firewall is None:
        firewall = PyTorchFirewall(unknown=True)

    entries = [pathlib.PurePosixPath(entry.filename) for entry in zip_file.infolist()]
    entries = [entry for entry in entries if entry.name == "data.pkl"]
    if len(entries) != 1:
        raise ValueError(f"expected one data.pkl entry, found {len(entries)}")

    prefix = str(entries[0].parent) + "/"
    sm = StorageManagerZip(zip_file=zip_file, prefix=prefix)

    with setting(storage_manager_var, sm), sm.open("data.pkl") as pf:
        return Unpickler(file=pf, firewall=firewall).load()
