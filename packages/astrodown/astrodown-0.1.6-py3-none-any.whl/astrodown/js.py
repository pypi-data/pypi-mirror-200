"""
functions used by js
"""

from inspect import signature
from typing import Callable, TypedDict
from .utils import file_ext
import enum
import pyodide_http

pyodide_http.patch_all()


class ExportDataType(str, enum.Enum):
    pandas = "pandas"
    s3 = "s3"
    database = "database"
    raw = "raw"


class ExportData(TypedDict):
    name: str
    type: ExportDataType
    value: str


def get_doc(value: any) -> str:
    return value.__doc__ if value.__doc__ else ""


def inspect_function(f: Callable):
    doc = get_doc(f)
    return "\n".join([doc, f"{f.__name__}{str(signature(f))}"]).strip()


def load_export(export: ExportData):
    match export["type"]:
        case ExportDataType.pandas:
            return _load_pandas(export)

        case ExportDataType.s3:
            # load s3
            pass

        case ExportDataType.database:
            # load database
            pass

        case ExportDataType.raw:
            # load raw
            return _load_raw(export)

        case _:
            raise ValueError("Unknown export type")


def _load_pandas(export: ExportData):
    import pandas as pd

    value = export["value"]
    match file_ext(value):
        case "csv":
            return pd.read_csv(value)
        case "tsv":
            return pd.read_csv(value, sep="\t")
        case "json":
            return pd.read_json(value)
        case _:
            raise ValueError("Unknown pandas file type")


def _load_raw(export: ExportData):
    return export["value"]
