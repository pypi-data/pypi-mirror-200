from __future__ import annotations
import ctypes
from ctypes import POINTER
from types import FunctionType
from typing import Sequence, Union


PyCStructType: type = type(ctypes.Structure)
PyCUnionType: type = type(ctypes.Union)
_CData = ctypes.c_int.mro()[-2]
StructInfo = Sequence[Union[tuple[str, type[_CData]], tuple[str, type[_CData], int]]]
PyCFuncType = Union[ctypes.CDLL._FuncPtr, FunctionType]
Py_ssize_t = ctypes.c_ssize_t


class _SelfRefClass:
    """A special class to create an object for Structures and Unions to refer to themselves"""
    _instance = None

    def __new__(cls: type[_SelfRefClass]) -> _SelfRefClass:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


class _SelfRefPointerClass:
    """A special class to create an object for Structures and Unions to refer to pointers of themselves"""
    _instance = None

    def __new__(cls: type[_SelfRefPointerClass]) -> _SelfRefPointerClass:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


SelfRef: _SelfRefClass = _SelfRefClass()
SelfPointer: _SelfRefPointerClass = _SelfRefPointerClass()

FieldType = Union[ctypes.Union, ctypes.Structure, ctypes.Array,
            ctypes._Pointer, _SelfRefClass, _SelfRefPointerClass]


def _parse_fields(cls: Union[ctypes.Structure, ctypes.Union], field: FieldType) -> _CData:
    """Convert self references into proper structure and union references"""
    if field is SelfRef:
        return cls
    elif field is SelfPointer:
        return POINTER(cls)
    else:
        return field
