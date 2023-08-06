from __future__ import annotations as _annotations 
from .structured_data import StructBase, UnionBase
from .constants import SelfRef, SelfPointer
from .constants import Py_ssize_t
import ctypes as _py_ctypes
from functools import cache as _cache
from typing import List as _List


__all__ = ("StructBase", "UnionBase", "SelfRef", "SelfPointer", "Py_ssize_t")
__all__ = list(set(dir(_py_ctypes)).union(__all__))


def __getattr__(name: str):
    return getattr(_py_ctypes, name)


@_cache
def __dir__() -> _List[str]:
    return __all__