# Copyright Formic Technologies 2023
import uuid
from datetime import datetime

from asyncua.ua.uatypes import VariantType

type_map = {
    VariantType.SByte: int,
    VariantType.Byte: int,
    VariantType.ByteString: bytes,
    VariantType.Int16: int,
    VariantType.Int32: int,
    VariantType.Int64: int,
    VariantType.UInt16: int,
    VariantType.UInt32: int,
    VariantType.UInt64: int,
    VariantType.Boolean: bool,
    VariantType.Double: float,
    VariantType.Float: float,
    VariantType.String: str,
    VariantType.DateTime: datetime,
    VariantType.Guid: uuid.UUID,
}


def convert_type(value, var_type):
    return type_map[var_type](value)
