import os
try:
    from PIL import Image
except:
    os.system("pip install --proxy http://proxy.hcm.fpt.vn:80 Pillow")
    from PIL import Image
    pass


try:
    import cv2

    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False

from cads_sdk.nosql.etl import read_mp3,read_pcm

import base64
import io

from typing import (
    Any,
    Callable,
    Dict,
    Iterator,
    List,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
    overload,
    TYPE_CHECKING,
)
from pyspark.sql.column import Column

import pandas as pd
pd.options.display.width = 200


def cvtColor(binary):
    b,g,r = Image.open(io.BytesIO(binary)).split()
    return Image.merge("RGB", (r, g, b))

def openImage(binary):
    return Image.open(io.BytesIO(binary))

def get_thumbnail(i):
    width = pd.options.display.width
    i.thumbnail((width, width), Image.LANCZOS)
    return i

def image_base64(im):
    # if isinstance(im, str):
    #     im = get_thumbnail(im)
    im = get_thumbnail(im)    
    with io.BytesIO() as buffer:
        im.save(buffer, 'jpeg')
        return base64.b64encode(buffer.getvalue()).decode()

def image_formatter(im):
    return f'<img src="data:image/jpeg;base64,{image_base64(im)}">'
    # return f'<img src="data:image/jpeg;base64,{image_base64(im)}">'

    
    
def _create_idx_dataframe(self, orderBy='path'):
    from pyspark.sql.functions import spark_partition_id, monotonically_increasing_id, count, lit, first, sum, col, udf
    from pyspark.sql.window import Window

    offset = 1
    df_with_partition_id = self.withColumn("partition_id", spark_partition_id()).withColumn("inc_id", monotonically_increasing_id())

    partition_offsets = df_with_partition_id \
        .orderBy("partition_id") \
        .groupBy("partition_id") \
        .agg(count(lit(1)).alias("cnt"), first("inc_id").alias("inc_id")) \
        .withColumn("cnt", sum("cnt").over(Window.orderBy("partition_id")) - col("cnt") - col("inc_id") + lit(offset).alias("cnt")) \
        .select(["partition_id", "cnt"]) \
        .collect()

    get_offset = {}
    for row in partition_offsets:
        get_offset[row[0]] = row[1]


    spark_df = df_with_partition_id \
        .withColumn("partition_offset", udf(lambda partition_id: get_offset[partition_id], "long")(col("partition_id"))) \
        .withColumn("idx", col("partition_offset") + col("inc_id")) \
        .drop("partition_id", "partition_offset", "inc_id")
    return spark_df

def _filter_idx(self):
    self.createOrReplaceTempView('spark_df')

    spark_df = ss.sql(f"""
    select 
        *
    from spark_df
    where idx between {self.from_idx} and {self.to_idx}
    """)
    return spark_df.drop('idx')

def convert_to_index_sliceable(self):
    if isinstance(self.from_idx, int):
        self.from_idx = self.from_idx
        if isinstance(self.to_idx, int):
            self.to_idx = self.to_idx
        else:
            self.to_idx = self.from_idx + self.limit_idx
    else:
        self.from_idx = 0
        if isinstance(self.to_idx, int):
            self.to_idx = self.to_idx
        else:
            self.to_idx = self.limit_idx
    from pyspark.sql import DataFrame as SparkDataFrame
    SparkDataFrame.from_idx = self.from_idx
    SparkDataFrame.to_idx = self.to_idx


def __getitem__(self, item: Union[int, str, Column, List, Tuple]) -> Union[Column, "DataFrame"]:
        """Returns the column as a :class:`Column`.

        .. versionadded:: 1.3.0

        Examples
        --------
        >>> df.select(df['age']).collect()
        [Row(age=2), Row(age=5)]
        >>> df[ ["name", "age"]].collect()
        [Row(name='Alice', age=2), Row(name='Bob', age=5)]
        >>> df[ df.age > 3 ].collect()
        [Row(age=5, name='Bob')]
        >>> df[df[0] > 3].collect()
        [Row(age=5, name='Bob')]
        """
        if isinstance(item, str):
            jc = self._jdf.apply(item)
            return Column(jc)
        elif isinstance(item, Column):
            return self.filter(item)
        elif isinstance(item, (list, tuple)):
            return self.select(*item)
        elif isinstance(item, int):
            jc = self._jdf.apply(self.columns[item])
            return Column(jc)
        elif isinstance(item, slice):
            self.from_idx = item.start
            self.to_idx = item.stop
            self.limit_idx = 100

            self.convert_to_index_sliceable()
            self = self._create_idx_dataframe()
            spark_df = self._filter_idx()
            return spark_df
            
        else:
            raise TypeError("unexpected item type: %s" % type(item))
    
    
def toPandasImage(self, limit:int = 100, mode='RGB'):
    """
    Function to display image in parquet as a DataFrame
    Parameters
    ----------
    limit : int
        Default: 100
        Limit number of display image at the same time
        Maxium is 100
    mode : str
        Color mode 
        Default: 'RGB'
        RGB or BGR
        
    """
    if limit > 100:
        limit = 100
    pdf = self.limit(limit).toPandas()
    
    need_convert_dict = {}
    for c in self.schema:
        if "BinaryType" in str(c.dataType):
            c_name = c.name
            # pdf[c_name] = pdf[c_name].apply(lambda x: Image.open(io.BytesIO(x)))
            if mode=='BGR':
                pdf[c_name] = pdf[c_name].apply(cvtColor)
            else:
                pdf[c_name] = pdf[c_name].apply(openImage)
            need_convert_dict[c_name] = image_formatter
    DataFrame.need_convert_dict = need_convert_dict
    pdf.need_convert_dict = need_convert_dict
    return pdf


from pyspark.sql import DataFrame as SparkDataFrame
SparkDataFrame.__getitem__ = __getitem__
SparkDataFrame.convert_to_index_sliceable = convert_to_index_sliceable
SparkDataFrame._create_idx_dataframe = _create_idx_dataframe
SparkDataFrame._filter_idx = _filter_idx


SparkDataFrame.toPandasImage = toPandasImage

from pandas._config import get_option
from io import StringIO
from pandas.io.formats import format as fmt
from typing import Optional

def _repr_html_(self) -> Optional[str]:
    """
    Function display Image with pandas
    Return a html representation for a particular DataFrame.
    Mainly for IPython notebook.
    """
    if self._info_repr():
        buf = StringIO()
        self.info(buf=buf)
        # need to escape the <class>, should be the first line.
        val = buf.getvalue().replace("<", r"&lt;", 1)
        val = val.replace(">", r"&gt;", 1)
        return f"<pre>{val}</pre>"

    if get_option("display.notebook_repr_html"):
        max_rows = get_option("display.max_rows")
        min_rows = get_option("display.min_rows")
        max_cols = get_option("display.max_columns")
        show_dimensions = get_option("display.show_dimensions")
        
        if 'need_convert_dict' not in self.__dict__:
            if self._is_copy:
                pass
            else:
                self.need_convert_dict = {}
                
        formatter = fmt.DataFrameFormatter(
            self,
            columns=None,
            col_space=None,
            na_rep="NaN",
            formatters=self.need_convert_dict,
            float_format=None,
            sparsify=None,
            justify=None,
            index_names=True,
            header=True,
            index=True,
            bold_rows=True,
            escape=False,
            max_rows=max_rows,
            min_rows=min_rows,
            max_cols=max_cols,
            show_dimensions=show_dimensions,
            decimal=".",
        )
        
        return fmt.DataFrameRenderer(formatter).to_html()
    else:
        return None

from pandas import DataFrame
DataFrame._repr_html_ = _repr_html_

import os
import tempfile


from cads_sdk.utils import import_or_install
import_or_install("ipywidgets")
try:
    os.system("jupyter nbextension enable --py --sys-prefix widgetsnbextension")
except:
    os.system("pip install --proxy http://proxy.hcm.fpt.vn:80 ipywidgets")
    os.system("jupyter nbextension enable --py --sys-prefix widgetsnbextension")
    
from ipywidgets.widgets import Box
from ipywidgets import widgets
from traitlets import traitlets

from cads_sdk import PySpark
import cads_sdk as ss

import numpy as np
from io import BytesIO

class LoadedButton(widgets.Button):
    """A button that can holds a value as a attribute."""

    def __init__(self, value=None, *args, **kwargs):
        super(LoadedButton, self).__init__(*args, **kwargs)
        # Create the value attribute.
        self.add_traits(value=traitlets.Any(value))


class Video(object):
    def __init__(self, 
                 input_path=None, 
                 width=None, 
                 height=None, 
                 html_attributes="controls",
                 thumbnail_width = 256,
                 thumbnail_height = 144,
                 from_idx = None,
                 to_idx = None,
                 limit = 100
                ):
        
        self.input_path = input_path
        self.width = width
        self.height = height
        self.html_attributes = html_attributes
        self.thumbnail_width = thumbnail_width
        self.thumbnail_height = thumbnail_height
        self.from_idx = from_idx
        self.to_idx = to_idx
        self.limit = limit
        
    def convert_to_index_sliceable(self):
        if isinstance(self.from_idx, int):
            self.from_idx = self.from_idx
            if isinstance(self.to_idx, int):
                self.to_idx = self.to_idx
            else:
                self.to_idx = self.from_idx + self.limit
        else:
            self.from_idx = 0
            if isinstance(self.to_idx, int):
                self.to_idx = self.to_idx
            else:
                self.to_idx = self.limit
        
        
    def get_spark(self):
        return ss.PySpark(driver_memory='32G', num_executors='4', executor_memory='4G', port='', yarn=False).spark
    
    def check_delta(self, input_path):
        list_file = ss.ls(input_path)
        for f in list_file:
            if '_delta_log' in f:
                if len(ss.ls(os.path.join(input_path, '_delta_log'))) > 0:
                    return True
        return False

        
    def generate_sql(self, columns):
        spark = self.get_spark()
        if self.check_delta(self.input_path):
            df = spark.sql(f"""select {columns} from delta.`{self.input_path}` """)
        else:
            df = spark.sql(f"""select {columns} from parquet.`{self.input_path}`""")
        return df
    
    
    def write_to_folder(self, row):
        with open(self.tmp_file, 'wb') as wfile:
            wfile.write(row.video)
            
    def displayVideo(self, ex):
        get_value = ex.description
        df = self.generate_sql("*").filter(f"path = '{get_value}'").limit(1)

        self.temp_folder = tempfile.TemporaryDirectory(dir='./tmp_sdk')

        # self.temp_folder = './tmp_sdk'
        self.base_path = os.path.basename(str(get_value))
        self.tmp_file = os.path.join(self.temp_folder.name, self.base_path)

        _ = [self.write_to_folder(row) for row in df.collect()]

        from IPython.display import Video
        self.output.append_display_data(Video(self.tmp_file, width=self.width, height=self.height))

    def __getitem__(self, key):
        _valid_types = (
            "integer, integer slice (START point is INCLUDED, END "
            "point is EXCLUDED), listlike of integers, boolean array"
        )
        
        from pandas.core.indexers import (check_array_indexer, is_list_like_indexer)
        
        if not isinstance(key, slice):
            raise ValueError("Invalid call for scalar access (getting)!")
        # if not is_list_like_indexer(key):
        #     raise ValueError(f"Can only index by location with a {key}]")
            
        
        self.from_idx = key.start
        self.to_idx = key.stop
        return self._repr_html_()
        
        
    def _repr_html_(self):
        width = height = ''
        if self.width:
            width = ' width="%d"' % self.width
        if self.height:
            height = ' height="%d"' % self.height
            
        if isinstance(self.input_path, str):
            df_path = self.generate_sql("path, thumbnail")
        
            if self.from_idx:
                self.convert_to_index_sliceable()
                df_path = df_path[self.from_idx:self.to_idx]
        else:
            raise ValueError("Check your input_path, it not string or can not be found")
        
        selection_box = widgets.VBox()
        selection_toggles = []
        selected_labels = {}
        labels = {}
        
        
        layout = widgets.Layout(width=str(pd.options.display.max_colwidth*5)+'px', height=f"{self.thumbnail_height}px")
        
        for row in sorted(df_path.orderBy("path").collect()):
            o = LoadedButton(description=row.path, value=row.path, layout=layout)
            o.on_click(self.displayVideo)
            
            
            thumbnail = widgets.Image(
                value=row.thumbnail,
                format='jpg',
                width=self.thumbnail_width,
                height=self.thumbnail_height,
            )
            
            video_button = widgets.HBox()
            video_button.children = [o, thumbnail]
            
            selection_toggles.append(video_button)

        selection_box.children = selection_toggles
        self.output = widgets.Output()
        return display(selection_box, self.output)
    
    
    def __repr__(self):
        return ""
    

class Audio(object):
    """
    Audio 
    Function to display all audio files in parquet file as a list of buttons
    When click on button with lable, audio user just clicked will pop up and display
    
    :param 
    input_path: path to parquet/delta file

    Return:
    HTML list of buttons base on path name can be clicked to display Video
    
    # Test case 1: Open parquet pcm file
    from cads_sdk.nosql.reader import Video
    Audio('file:/home/duyvnc/image_storage/audio_pcm.parquet')
    
    # Test case 2: Open parquet mp3 file
    Audio('file:/home/duyvnc/image_storage/audio_mp3.parquet')
    
    # Test case 3: Open parquet wav file
    Audio('file:/home/duyvnc/image_storage/audio_wav.parquet')
    """
    def __init__(self, 
                 input_path=None, 
                 width=None, 
                 height=None, 
                 html_attributes="controls",
                 thumbnail_width = 256,
                 thumbnail_height = 144,
                 from_idx = None,
                 to_idx = None,
                 limit = 100
                ):
        
        self.input_path = input_path
        self.width = width
        self.height = height
        self.html_attributes = html_attributes
        self.thumbnail_width = thumbnail_width
        self.thumbnail_height = thumbnail_height
        self.from_idx = from_idx
        self.to_idx = to_idx
        self.limit = limit
        
    def convert_to_index_sliceable(self):
        if isinstance(self.from_idx, int):
            self.from_idx = self.from_idx
            if isinstance(self.to_idx, int):
                self.to_idx = self.to_idx
            else:
                self.to_idx = self.from_idx + self.limit
        else:
            self.from_idx = 0
            if isinstance(self.to_idx, int):
                self.to_idx = self.to_idx
            else:
                self.to_idx = self.limit
        
    def get_spark(self):
        return ss.PySpark(driver_memory='32G', num_executors='4', executor_memory='4G', port='', yarn=False).spark
    
    def check_delta(self, input_path):
        list_file = ss.ls(input_path)
        for f in list_file:
            if '_delta_log' in f:
                if len(ss.ls(os.path.join(input_path, '_delta_log'))) > 0:
                    return True
        return False

    def generate_sql(self, columns):
        spark = self.get_spark()
        if self.check_delta(self.input_path):
            df = spark.sql(f"""select {columns} from delta.`{self.input_path}` """)
        else:
            df = spark.sql(f"""select {columns} from parquet.`{self.input_path}`""")
        return df
    
    
    def write_to_folder(self, row):
        if '.pcm' in row.path:
            data = np.frombuffer(row.audio, dtype = 'float64')
            from IPython.display import Audio, display
            self.output.append_display_data(Audio(data, rate=int(row['samplerate'])))
            
        elif '.wav' in row.path:
            from scipy.io import wavfile
            samplerate, data = wavfile.read(BytesIO(row.audio))
            from IPython.display import Audio, display
            self.output.append_display_data(Audio(data.T, rate=samplerate))
            
        elif 'mp3' in row.path:
            samplerate, data = read_mp3(BytesIO(row.audio))
            from IPython.display import Audio, display
            self.output.append_display_data(Audio(data.T, rate=samplerate))
            
    def displayAudio(self, ex):
        get_value = ex.description
        df = self.generate_sql("*").filter(f"path = '{get_value}'").limit(1)
        
        _ = [self.write_to_folder(row) for row in df.collect()]
        
        # df.foreach(self.write_to_folder)
        
        
    def _repr_html_(self):
        width = height = ''
        if self.width:
            width = ' width="%d"' % self.width
        if self.height:
            height = ' height="%d"' % self.height
            
        if isinstance(self.input_path, str):
            df_path = self.generate_sql("path")
        
            if self.from_idx:
                self.convert_to_index_sliceable()
                df_path = df_path[self.from_idx:self.to_idx]
        
        selection_box = widgets.VBox()
        selection_toggles = []
        selected_labels = {}
        
        layout = widgets.Layout(width=str(pd.options.display.max_colwidth*5)+'px', height='40px')
        
        for row in df_path.orderBy('path').collect():
            o = LoadedButton(description=row.path, value=row.path,layout=layout)
            o.on_click(self.displayAudio)
            selection_toggles.append(o)

        selection_box.children = selection_toggles
        self.output = widgets.Output()
        return display(selection_box, self.output)
    
    def __getitem__(self, key):
        _valid_types = (
            "integer, integer slice (START point is INCLUDED, END "
            "point is EXCLUDED), listlike of integers, boolean array"
        )
        
        from pandas.core.indexers import (check_array_indexer, is_list_like_indexer)
        
        if not isinstance(key, slice):
            raise ValueError("Invalid call for scalar access (getting)!")
        # if not is_list_like_indexer(key):
        #     raise ValueError(f"Can only index by location with a {key}]")
            
        
        self.from_idx = key.start
        self.to_idx = key.stop
        return self._repr_html_()
    
    def __repr__(self):
        return ""
    
    
def __repr__(self):
    return """If not display widget try copy this to your terminal
    pip install --proxy http://proxy.hcm.fpt.vn:80 ipywidgets
    jupyter nbextension enable --py --sys-prefix widgetsnbextension
    """