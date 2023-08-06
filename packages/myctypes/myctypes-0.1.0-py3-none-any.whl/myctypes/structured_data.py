from .constants import StructInfo, PyCStructType, PyCUnionType, _parse_fields
from ctypes import Structure, Union
from ctypes._endian import _swapped_meta
import sys


class CStructureMeta(PyCStructType):
    _fields_: StructInfo

    def __new__(mcs: type, name: str, bases: tuple, clsdict: dict, base_struct: bool = False) -> type:
        if "_fields_" in clsdict:
            msg = "Ambiguous to have both class member type annotations and "
            msg += f"a _fields_ attribute for struct class {name}"
            raise TypeError(msg)
        cls = super().__new__(mcs, name, bases, clsdict)
        if not base_struct:
            cls._fields_ = [(name, _parse_fields(name, field_type))
                             for name, field_type in clsdict.get("__annotations__", {}).items()]
        return cls


class CStructureEndianMeta(CStructureMeta, _swapped_meta):
    pass


class CUnionMeta(PyCUnionType):
    _fields_: StructInfo

    def __new__(mcs: type, name: str, bases: tuple, clsdict: dict, base_struct: bool = False) -> type:
        if "_fields_" in clsdict:
            msg = "Ambiguous to have both class member type annotations and "
            msg += f"a _fields_ attribute for Union class {name}"
            raise TypeError(msg)
        cls = super().__new__(mcs, name, bases, clsdict)
        if not base_struct:
            cls._fields_ = [(name, _parse_fields(name, field_type))
                            for name, field_type in clsdict.get("__annotations__", {}).items()]
        return cls


class StructBase(Structure, metaclass=CStructureMeta, base_struct=True):
    """Creates an interface for structs that allows for type annotations,
    better IDE and development tool support, and is more intuitive

    Usage:
        class MyPointStruct(StructBase):
            x: ctypes.c_float
            y: ctypes.c_float
    """
    _fields_: StructInfo


class UnionBase(Union, metaclass=CUnionMeta, base_struct=True):
    """Creates an interface for unions that allows for type annotations,
    better IDE and development tool support, and is more intuitive

    Usage:
        class MyUnionStruct(UnionBase):
            name: ctypes.c_char * 25
            age: ctypes.c_ulong
    """
    _fields_: StructInfo


if sys.byteorder == "little":

    LittleEndianStructBase = StructBase

    class BigEndianStructBase(StructBase, metaclass=CStructureEndianMeta, base_struct=True):
        """Structure with big endian byte order"""
        __slots__ = ()
        _swappedbytes_ = None

elif sys.byteorder == "big":

    BigEndianStructBase = StructBase
    class LittleEndianStructBase(StructBase, metaclass=CStructureEndianMeta, base_struct=True):
        """Structure with little endian byte order"""
        __slots__ = ()
        _swappedbytes_ = None

else:
    raise RuntimeError("Invalid byteorder")

