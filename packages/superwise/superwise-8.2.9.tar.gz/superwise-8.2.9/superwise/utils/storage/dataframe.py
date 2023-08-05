import io
import sys
import tempfile

import pandas as pd

from superwise.utils.storage import validate_file_size


def load_from_dataframe(df: pd.DataFrame, filename: str = "DataFrame", validate_size: bool = False) -> dict:
    file_size = None
    f = io.BytesIO()
    df.to_parquet(f)
    f.seek(0)
    data = f.read()
    if validate_size:
        file_size = sys.getsizeof(data)
        validate_file_size(file_path="in memory", file_size=file_size, upload_type="DataFrame")

    return dict(filename=filename, data=data, size=file_size)


def dataframe_to_tempfile(dataframe: pd.DataFrame, name: str) -> str:
    tf = tempfile.NamedTemporaryFile(prefix=f"{name}_from_dataframe-", suffix=".parquet", delete=False)
    dataframe.to_parquet(tf)
    return tf.name
