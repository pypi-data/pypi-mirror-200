import base64
import numpy as np
import pandas as pd
import pyarrow as pa
import uuid

from typing import Union

from ... import DataSet


def unique_id_str() -> str:
    return str(uuid.uuid1())


def unique_id_int() -> int:
    return uuid.uuid1().int


def _to_utf64_arrow_buffer(data: Union[pd.DataFrame, DataSet], preserve_index: bool = True) -> str:
    """
    Transform pandas dataframe or Shapelets dataset to an arrow buffer
    """
    if isinstance(data, pd.DataFrame):
        # df = dataframe.astype(float)
        table = pa.Table.from_pandas(data, preserve_index=preserve_index)
    elif isinstance(data, DataSet):
        table = data.to_arrow_table(1024)

    sink = pa.BufferOutputStream()
    with pa.ipc.RecordBatchFileWriter(sink, table.schema) as writer:
        writer.write(table)
    buffer = sink.getvalue()
    return base64.b64encode(buffer).decode("utf-8")


def _to_utf64_arrow_buffer_numpy(array: np.ndarray) -> str:
    parray = pa.array(array.flatten())
    batch = pa.record_batch([parray], names=["values"])
    sink = pa.BufferOutputStream()
    with pa.ipc.RecordBatchFileWriter(sink, batch.schema) as writer:
        writer.write(batch)
    buffer = sink.getvalue()
    return base64.b64encode(buffer).decode("utf-8")


def _to_utf64_arrow_buffer_series(series: pd.Series) -> str:
    parray = pa.Array.from_pandas(series)
    batch = pa.record_batch([parray], names=["values"])
    sink = pa.BufferOutputStream()
    with pa.ipc.RecordBatchFileWriter(sink, batch.schema) as writer:
        writer.write(batch)
    buffer = sink.getvalue()
    return base64.b64encode(buffer).decode("utf-8")
