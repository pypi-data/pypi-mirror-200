# module level doc-string
from .pyspark_add_on import PySpark, PyArrow, Utf8Encoder
from .pyspark_add_on import to_dwh, drop_table, drop_table_and_delete_data, read_table, sql, refresh_table, spark_dataframe_to_dwh
from .pyspark_add_on import ls, mkdir, cat, exists, info, open
from .pyspark_add_on import read_dwh_pd, read_csv, read_json, write_json, read_parquet, read_dwh
from .pyspark_add_on import show, refresh_table
from .pyspark_add_on import limit_timestamp
from .pyspark_add_on import spark_dataframe_info
from .create_yaml_file import CreateYamlDWH
from .pandas_decrypt import decrypt, decrypt_column

#from .nosql.reader import _repr_html_ as PandasDataFrame_repr_html_

# from .pyspark_add_on.PySpark import to_dwh
from .utils import modulereload, choose_num_core
from pandas.core.series import Series


import pandas as pd
from pandas import DataFrame


DataFrame.to_dwh = to_dwh
#DataFrame._repr_html_ = PandasDataFrame_repr_html_
modulereload(pd)

Series.decrypt_column = decrypt_column
pd.read_dwh = read_dwh_pd
modulereload(pd)


from pyspark.sql import DataFrame as SparkDataFrame
SparkDataFrame.to_dwh = spark_dataframe_to_dwh
SparkDataFrame.info = spark_dataframe_info


SparkDataFrame.show = show



__version__ = '0.0.10'
__all__ = ["PySpark", "PyArrow"]

__doc__ = """
cads-sdk: Functions to help Data Scientist work more effectively with unstructured data and datalake
=====================================================================
**cads-sdk**
Function to convert 
-------------
Here are just a few of the things that cads_sdk does well:
# Image pre-processing ready for train
    - Function Convert from image folders to parquet: 
      from cads.nosql.converter import ConvertFromFolderImage
    - Function Convert from zip fize to parquet: 
      from cads.nosql.converter import ConvertFromFolderImage
    - Function Convert parquet to folder of image: 
      from cads.nosql.converter import ConvertToFolderImage
    - Function to display parquet image
      from cads.nosql import display
      
# Audio pre-processing ready for train
    - Function Convert from audio folders to parquet: 
      from cads.nosql.converter import ConvertToFolderAudio
    - Function Convert from audio folders to parquet: 
      from cads.nosql.converter import ConvertFromFolderAudio
# Video
    - Function Convert from video files to parquet of frame: 
      from cads.nosql.converter import ConvertFromVideo2Image
    - Function to display frame parquet
      from cads.nosql import display
"""

