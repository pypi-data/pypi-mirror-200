import spark_sdk as ss

from glob import glob
import logging
import tempfile
import os
from pathlib import Path, PurePath

import numpy as np
import pandas as pd

try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    os.system("pip install --proxy http://proxy.hcm.fpt.vn:80 opencv-python")
    import cv2
    OPENCV_AVAILABLE = False
    
    
from zipfile import ZipFile

from pyspark.sql.types import StructField, StructType, IntegerType, BinaryType, StringType, TimestampType, FloatType, LongType

from cads_sdk.nosql.codec import *
from cads_sdk.nosql.etl import read_mp3,read_pcm,padding

class ConvertFromFolderImage:
    """
    Create a parquet/delta file given local Image directory
    

    Parameters
    ----------
    input_path : unicode, str 
        The input filename include ``png``, ``jpeg`` image
        User can add system file pattern like *
        Examples:
        input_path="**/*.jpg"
        input_path="**/*.png"
        This pattern get all jpg in folder with different directory levels
        View https://docs.python.org/3/library/glob.html

    output_path : unicode
        Ouput directory location maybe file:/ (local file) or hdfs:/ (datalake path)
        Examples:
        output_path = "file:/home/username/"
        output_path = "hdfs:/user/username/"
        
    table_name : str
        Table_name store metadata
        User should input table_name follow dwh convention: img_abc, vid_abc, audio_abc
        Examples: img_abc
        
    database : str
        Database to store metadata
        User should input database follow dwh convention: default
        Examples: default
        

    repartition : bool 
        Default: False
        Data will be repartition to target file size
        
    numPartition : int
        Default None
        Number of part each user want to seperate parquet file into

    file_format : str
        Default: parquet
        File format user want to write parquet/delta
        
    compression: str 
        Default: zstd
        Compression method user want to compress parquet file
        Value: None, zstd, snappy
        See spark.sql.parquet.compression.codec
        https://spark.apache.org/docs/2.4.3/sql-data-sources-parquet.html
        
    image_type: str
        Default: jpg
        Value png or jpg
        
    image_color : int
        Default: 3
        Value 3, 2 or 1, shape of image have color is 3 or 1 if gray image
        
    size : List of Tuple
        Default: jpg
        List size user want to resize or padding
        Examples: size = [(320, 180), (500, 100)]
        
    resize_mode : str
        Default: None
        Value: None, padding, resize
        Mode of image user want to resize
        If in folder user have various size of image, 300, 400 500
        User will add size = 500:
        And resize_mode  = 'padding'
        Then function will convert all image 300, 400, 500 to shape of 500
    
    input_recursive : bool
        Default: True
        If True: 
        will loop through folder to get all pattern

    debug : bool
        If debug=True:
        Write log into sdk.log file and print more debug information


    Examples
    --------
    ::
        ```
        from cads_sdk.nosql.codec import ConvertFromFolderImage

        converter = ConvertFromFolderImage(
                      input_path="/home/username/image_storage/images/**/*.jpg",
                      input_recursive = True, # will loop through folder to get all pattern
                      #setting output
                      output_path = f"hdfs:/user/username/image/img_images_jpg.parquet",
                      table_name = 'img_images_jpg',
                      database = 'default',
                      file_format = 'parquet', # delta|parquet
                      compression = 'zstd', # |snappy
                      # setting converter
                      image_type = 'jpg',
                      image_color = 3,
                      resize_mode="padding", # |padding|resize
                      size = [(212,212),
                             (597, 597)],
                     )

        converter.execute()
        
        from cads_sdk.nosql.codec import ConvertFromFolderImage

        converter = ConvertFromFolderImage(
                      input_path="/home/username/image_storage/device_images/**/*.jpg",
                      input_recursive = True, # will loop through folder to get all pattern

                      #setting output
                      output_path = f"file:/home/username/image/img_user_device_jpg.delta",
                      table_name = 'img_user_device_jpg',
                      database = 'default',
                      file_format = 'delta', # |parquet
                      compression = 'zstd', # |snappy

                      # setting converter
                      image_type = 'jpg', # |'png'|('jpg', 'png')
                      image_color = 3,
                      resize_mode=None, # |padding|resize
                      size = [(212,212),
                             (597, 597)],
                     )

        converter.execute()
        ```
        
        Function will convert all Image in file:'/home/username/device_images/' to absolute directory file:/home/username/image/img_images_jpg.parquet
    """
   
    def __init__(
        self,
        input_path,
        output_path,
        table_name = '',
        database = '',
        repartition=False,
        numPartition=None,
        file_format = 'parquet',
        compression = 'zstd',
        
        image_type = 'jpg',
        image_color = 3,
        size=[(720,360)],
        resize_mode=None,
        input_recursive = False,
        
        debug=False
    ):
        
        self.input_path = input_path
        self.input_recursive = input_recursive
        self.output_path = output_path
        self.table_name = table_name
        self.database = database
        self.image_type = image_type
        self.image_color = image_color
        self.size = size
        self.resize_mode = resize_mode
        self.repartition = repartition
        self.numPartition = numPartition
        self.compression = compression
        self.file_format = file_format
        
        self.debug = debug
        
        if debug:
            self.temp_folder = tempfile.TemporaryDirectory(dir='./tmp_sdk')
            self.tmp_file = os.path.join(self.temp_folder.name, 'sdk.log')
            self.log_file = open(self.tmp_file, 'w+')
            logging.basicConfig(level=logging.DEBUG, filename=self.tmp_file, filemode='w+')
            
        else:
            logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
            
    def convert_to_hdfs_path(self, input_path):
        if "file:" in input_path:
            return input_path
        else:
            if "hdfs://hdfs-cluster.datalake.bigdata.local:8020" not in os.path.dirname(input_path):
                return "hdfs://hdfs-cluster.datalake.bigdata.local:8020" + os.path.abspath(input_path.replace("hdfs:", ""))
            else:
                return input_path

    
    def coalesce_dataframe(self, spark_df, numPartition):
        if numPartition:
            return spark_df.coalesce(numPartition)
        return spark_df
    
    def write_to_path(self, spark_df, output_path, table_name = '', database='', numPartition=8, compression='zstd'):
        if '.parquet' in output_path.lower():
            file_format = 'parquet'
        else:
            file_format = 'delta'
            
        if "file:" in output_path:
            self.coalesce_dataframe(spark_df, numPartition).write \
                .format(file_format) \
                .option('compression', compression) \
                .mode('overwrite') \
                .option("path", output_path) \
                .save()
        else:
            if table_name == '' or database == '':
                raise ValueError("You must add table_name and database")
            self.coalesce_dataframe(spark_df, numPartition).write \
                .format(file_format) \
                .option('compression', compression) \
                .mode('overwrite') \
                .option("path", output_path) \
                .saveAsTable(database + '.' + table_name)
          
    
    def row_generator(self, partitionData):
        """Returns a dict of row input to rdd spark dataframe"""
        for row in partitionData:
            path = row.path
            if self.debug:
                print(f"Convert Image {path}") #, file=self.log_file)
                
            img = cv2.imread(path)
            if self.resize_mode == 'padding':
                row_dict = {
                    'path': path,
                    'size': f"{img.shape[0]}, {img.shape[1]}",
                    'image': padding(img, (self.s[0], self.s[1]))
                }

                yield dict_to_spark_row(self.unischema, row_dict)
            elif self.resize_mode == 'resize':
                row_dict = {
                    'path': path,
                    'size': f"{img.shape[0]}, {img.shape[1]}",
                    'image': cv2.resize(img, (self.s[0], self.s[1]))
                }

                yield dict_to_spark_row(self.unischema, row_dict)
            else:
                row_dict = {
                    'path': path,
                    'size': f"{img.shape[0]}, {img.shape[1]}",
                    'image': open(path, 'rb').read()
                }

                yield dict_to_spark_row(self.unischema, row_dict)

                
    def create_dataframe(self, 
                         spark, 
                         Schema, 
                         input_files,
                         size):
        

        self.unischema = Schema
        self.s = size
        
        
        spark_df = spark.createDataFrame(pd.DataFrame(input_files, columns=['path']))
        if not self.resize_mode:
            logging.warning(f"Not resize image, If get size error try to turn resize_mode='padding' or resize_mode='resize'")
        return spark.createDataFrame(spark_df.rdd.mapPartitions(self.row_generator), Schema.as_spark_schema())
                
                    
    def create_image_schema(self, size, image_type, image_color):
        """
        :param size: Image size, schema need to be consistency
        :param image_type: Image type is compress JPG or PNG
        :param image_color: 3 dimention color or 1 dimention colors
        """
        if self.resize_mode:
            return Unischema('ImageSchema', [
            UnischemaField('path', np.str_, (), ScalarCodec(StringType()), False),
            UnischemaField('size', np.str_, (), ScalarCodec(StringType()), False),
            UnischemaField('image', np.uint8, (size[0], size[1], image_color), CompressedImageCodec(self.image_type, quality=95), False)
        ])
        
        else:
            return Unischema('ImageSchema', [
            UnischemaField('path', np.str_, (), ScalarCodec(StringType()), False),
            UnischemaField('size', np.str_, (), ScalarCodec(StringType()), False),
            UnischemaField('image', np.bytes_, (size[0], size[1], image_color), ImageZipCodec(BinaryType()), False)
        ])
    
    
    
    def get_spark(self):
        return ss.PySpark(driver_memory='32G', num_executors='8', executor_memory='4G', port='', yarn=False).spark
    
    
    def check_size(self, img, list_size):
        for s in list_size:
            if img.shape[0] <= s[0] and img.shape[1] <= s[1]:
                return s
        self.size.append(s)
        self.dict_image[(img.shape[0], img.shape[1])] = []
        return a
        #return (img.shape[0], img.shape[1])
    
    
    def execute(self):
        self.dict_image = {}
        ROWGROUP_SIZE_MB = 128
        
        for s in self.size:
            self.dict_image[s] = []
        
        if self.resize_mode and len(self.size) > 1:
            for p in sorted(glob(self.input_path, recursive=self.input_recursive)):
                img = cv2.imread(p)
                self.dict_image[self.check_size(img, self.size)].append(p)
        else:
            self.dict_image[self.size[0]] = sorted(glob(self.input_path, recursive=self.input_recursive))

        for s in self.size:
            self.output_path = self.convert_to_hdfs_path(self.output_path)
            if "." + self.file_format in self.output_path:
                output_path = self.output_path.replace("." + self.file_format, "_{s0}_{s1}.{file_format}".format(s0=str(s[0]), s1=str(s[1]), file_format=self.file_format))
            else:
                output_path = self.output_path + "_{s0}_{s1}.{file_format}".format(s0=str(s[0]), s1=str(s[1]), file_format=self.file_format)
            
            if self.table_name:
                table_name = self.table_name + "_{s0}_{s1}".format(s0=str(s[0]), s1=str(s[1]))
            else:
                table_name = ''
            
            spark = self.get_spark()

            Schema = self.create_image_schema(s, self.image_type, self.image_color)
            if self.dict_image[s]:
                logging.info(f"Write at path: {output_path}")
                logging.info(f"Save metadata at: {table_name}")
                with materialize_dataset(spark, output_path, Schema, ROWGROUP_SIZE_MB):
                    self.write_to_path(spark_df = self.create_dataframe(spark=spark,
                                          Schema=Schema,
                                          input_files=self.dict_image[s],
                                          size=s),

                                    output_path = output_path,
                                    table_name = table_name, 
                                    database = self.database,
                                    numPartition = self.numPartition,
                                    compression = self.compression)
        total_image = 0
        for s in self.size:
            total_image += len(self.dict_image[s])
            if total_image==0:
                logging.warn("No files were found, check your input_path")
                
        logging.info("Convert complete")
                
class ConvertFromZipImage:
    """
    Create a parquet/delta file given local Image directory
    

    Parameters
    ----------
    input_path : unicode, str 
        The input ZIP directory include ``png``, ``jpeg`` image
        User can add system file pattern like *
        Examples:
        input_path="/path/to/MOT17.zip"
        This pattern get all jpg in folder with different directory levels
        View https://docs.python.org/3/library/glob.html

    output_path : unicode
        Ouput directory location maybe file:/ (local file) or hdfs:/ (datalake path)
        Examples:
        output_path = "file:/home/username/"
        output_path = "hdfs:/user/username/"
        
    table_name : str
        Table_name store metadata
        User should input table_name follow dwh convention: img_abc, vid_abc, audio_abc
        Examples: img_abc
        
    database : str
        Database to store metadata
        User should input database follow dwh convention: default
        Examples: default
        

    repartition : bool 
        Default: False
        Data will be repartition to target file size
        
    numPartition : int
        Default None
        Number of part each user want to seperate parquet file into

    file_format : str
        Default: parquet
        File format user want to write parquet/delta
        
    compression: str 
        Default: zstd
        Compression method user want to compress parquet file
        Value: None, zstd, snappy
        See spark.sql.parquet.compression.codec
        https://spark.apache.org/docs/2.4.3/sql-data-sources-parquet.html
        
    image_type : str
        Default: jpg
        Value png or jpg
        
    image_color : int
        Default: 3
        Value 3, 2 or 1, shape of image have color is 3 or 1 if gray image
        
    size : List of Tuple
        Default: jpg
        List size user want to resize or padding
        Examples: size = [(320, 180), (500, 100)]
        
    resize_mode : str
        Default: None
        Value: None, padding, resize
        Mode of image user want to resize
        If in folder user have various size of image, 300, 400 500
        User will add size = 500:
        And resize_mode  = 'padding'
        Then function will convert all image 300, 400, 500 to shape of 500

    debug : bool
        If debug=True:
        Write log into sdk.log file and print more debug information


    Examples
    --------
    ::
        ```
        from cads_sdk.nosql.codec import ConvertFromZipImage

        converter = ConvertFromZipImage(
                      input_path="/home/username/image_storage/MOT17.zip",
                      
                      #setting output
                      output_path = f"hdfs:/user/username/image/img_images_jpg.parquet",
                      table_name = 'img_images_jpg',
                      database = 'default',
                      file_format = 'parquet', # delta|parquet
                      compression = 'zstd', # |snappy
                      # setting converter
                      image_type = 'jpg', # |'png'|('jpg', 'png')
                      image_color = 3,
                      resize_mode=None, # |padding|resize
                      size = [(212,212)],
                      
                      input_recursive = True, # will loop through folder to get all pattern
                     )

        converter.execute()
        ```
        
        Function will convert all Image in file:'/home/username/image_storage/MOT17.zip' to absolute directory hdfs:/user/username/image/img_images_jpg.parquet
    """
   
        
    def __init__(
        self,
        input_path,
        output_path,
        table_name = '',
        database = '',
        repartition=False,
        numPartition=None,
        file_format = 'parquet',
        compression = 'zstd',
        
        image_type = 'jpg',
        image_color = 3,
        size=[(720,360)],
        resize_mode=None,
        input_recursive = False,
        
        debug=False
    ):
        
        self.input_path = input_path
        self.input_recursive = input_recursive
        self.output_path = output_path
        self.table_name = table_name
        self.database = database
        self.image_type = image_type
        self.image_color = image_color
        self.size = size
        self.resize_mode = resize_mode
        self.repartition = repartition
        self.numPartition = numPartition
        self.compression = compression
        self.file_format = file_format
        
        self.debug = debug
        
        if debug:
            self.temp_folder = tempfile.TemporaryDirectory(dir='./tmp_sdk')
            self.tmp_file = os.path.join(self.temp_folder.name, 'sdk.log')
            self.log_file = open(self.tmp_file, 'w+')
            logging.basicConfig(level=logging.DEBUG, filename=self.tmp_file, filemode='w+')
            
        else:
            logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
            
    def convert_to_hdfs_path(self, input_path):
        if "file:" in input_path:
            return input_path
        else:
            if "hdfs://hdfs-cluster.datalake.bigdata.local:8020" not in os.path.dirname(input_path):
                return "hdfs://hdfs-cluster.datalake.bigdata.local:8020" + os.path.abspath(input_path.replace("hdfs:", ""))
            else:
                return input_path
        
    
    
    def coalesce_dataframe(self, spark_df, numPartition):
        if numPartition:
            return spark_df.coalesce(numPartition)
        return spark_df
    
    def write_to_path(self, spark_df, output_path, table_name = '', database='', numPartition=8, compression='zstd'):
        if '.parquet' in output_path.lower():
            file_format = 'parquet'
        else:
            file_format = 'delta'
            
        if "file:" in output_path:
            self.coalesce_dataframe(spark_df, numPartition).write \
                .format(file_format) \
                .option('compression', compression) \
                .mode('overwrite') \
                .option("path", output_path) \
                .save()
        else:
            if table_name == '' or database == '':
                raise ValueError("You must add table_name and database")
            self.coalesce_dataframe(spark_df, numPartition).write \
                .format(file_format) \
                .option('compression', compression) \
                .mode('overwrite') \
                .option("path", output_path) \
                .saveAsTable(database + '.' + table_name)
            
            
    def row_generator(self, partitionData):
        """Returns a dict of row input to rdd spark dataframe"""          
        for row in partitionData:
            path = row.path
            if self.debug:
                print(f"Convert Image {path}") #, file=self.log_file)
                
            with ZipFile(self.input_path, 'r') as zipObj:
                img = cv2.imdecode(np.frombuffer(zipObj.read(path), dtype=np.uint8), cv2.IMREAD_UNCHANGED)
                if self.resize_mode == 'padding':
                    if img.shape[0] < self.s[0]:
                        row_dict = {
                            'path': path,
                            'size': f"{img.shape[0]}, {img.shape[1]}",
                            'image': padding(img, (self.s[0], self.s[1]))
                        }
                        yield dict_to_spark_row(self.unischema, row_dict)
                    else:
                        row_dict = {
                            'path': path,
                            'size': f"{img.shape[0]}, {img.shape[1]}",
                            'image': img
                        }
                        yield dict_to_spark_row(self.unischema, row_dict)

                elif self.resize_mode == 'resize':
                    if img.shape[0] < self.s[0]:
                        row_dict = {
                            'path': path,
                            'size': f"{img.shape[0]}, {img.shape[1]}",
                            'image': cv2.resize(img, (self.s[0], self.s[1]))
                        }
                        yield dict_to_spark_row(self.unischema, row_dict)
                    else:
                        row_dict = {
                            'path': path,
                            'size': f"{img.shape[0]}, {img.shape[1]}",
                            'image': img
                        }
                        yield dict_to_spark_row(self.unischema, row_dict)

                else:
                    row_dict = {
                        'path': path,
                        'size': f"{img.shape[0]}, {img.shape[1]}",
                        'image': zipObj.read(path)
                    }
                    yield dict_to_spark_row(self.unischema, row_dict)


    def create_dataframe(self, 
                         spark, 
                         Schema, 
                         input_files,
                         size):
        
        self.unischema = Schema
        self.s = size
        
        # with materialize_dataset(spark, output_path, ImageSchema, ROWGROUP_SIZE_MB):
        spark_df = spark.createDataFrame(pd.DataFrame(input_files, columns=['path']))
        if not self.resize_mode:
            logging.warning(f"Not resize image, If get size error try to turn resize_mode='padding' or resize_mode='resize'")
        return spark.createDataFrame(spark_df.rdd.mapPartitions(self.row_generator), Schema.as_spark_schema())
                
                    
    def create_image_schema(self, size, image_type, image_color):
        """
        :param size: Image size, schema need to be consistency
        :param image_type: Image type is compress JPG or PNG
        :param image_color: 3 dimention color or 1 dimention colors
        """
        if self.resize_mode:
            return Unischema('ImageSchema', [
            UnischemaField('path', np.str_, (), ScalarCodec(StringType()), False),
            UnischemaField('size', np.str_, (), ScalarCodec(StringType()), False),
            UnischemaField('image', np.uint8, (size[0], size[1], image_color), CompressedImageCodec(self.image_type, quality=95), False)
        ])
        
        else:
            return Unischema('ImageSchema', [
            UnischemaField('path', np.str_, (), ScalarCodec(StringType()), False),
            UnischemaField('size', np.str_, (), ScalarCodec(StringType()), False),
            UnischemaField('image', np.bytes_, (size[0], size[1], image_color), ImageZipCodec(BinaryType()), False)
        ])
    
    
    
    def get_spark(self):
        return ss.PySpark(driver_memory='16G', num_executors='8', executor_memory='4G', port='', yarn=False).spark
    
    
    def check_size(self, img, list_size):
        for s in list_size:
            if img.shape[0] <= s[0] and img.shape[1] <= s[1]:
                return s
        self.size.append(s)
        self.dict_image[(img.shape[0], img.shape[1])] = []
        return a
        #return (img.shape[0], img.shape[1])
    
    
    def execute(self):
        self.dict_image = {}
        ROWGROUP_SIZE_MB = 128
        
        with ZipFile(self.input_path, 'r') as zipObj:
            self.input_files = zipObj.namelist()
        logging.info(f"Total file in zip: {len(self.input_files)}")
        
        for s in self.size:
            self.dict_image[s] = []
        
        for i in self.input_files:
            if isinstance(self.image_type, str):
                if i.endswith('.'+self.image_type):
                    self.dict_image[self.size[0]].append(i)
            elif isinstance(self.image_type, (list, tuple)):
                for t in self.image_type:
                    if '.'+t in i:
                        self.dict_image[self.size[0]].append(i)
        
        for s in self.size:
            if self.dict_image[s]:
                self.output_path = self.convert_to_hdfs_path(self.output_path)
                if "." + self.file_format in self.output_path:
                    output_path = self.output_path.replace("." + self.file_format, "_{s0}_{s1}.{file_format}".format(s0=str(s[0]), s1=str(s[1]), file_format=self.file_format))
                else:
                    output_path = self.output_path + "_{s0}_{s1}.{file_format}".format(s0=str(s[0]), s1=str(s[1]), file_format=self.file_format)

                if self.table_name:
                    table_name = self.table_name + "_{s0}_{s1}".format(s0=str(s[0]), s1=str(s[1]))
                else:
                    table_name = ''

                spark = self.get_spark()

                Schema = self.create_image_schema(s, self.image_type, self.image_color)
                # if self.dict_image[s]:
                logging.info(f"Write at path: {output_path}")
                logging.info(f"Save metadata at: {table_name}")
                with materialize_dataset(spark, output_path, Schema, ROWGROUP_SIZE_MB):
                    self.write_to_path(spark_df = self.create_dataframe(spark=spark,
                                          Schema=Schema,
                                          input_files=self.dict_image[s],
                                          size=s),

                                    output_path = output_path,
                                    table_name = table_name, 
                                    database = self.database,
                                    numPartition = self.numPartition,
                                    compression = self.compression)
                
        total_image = 0
        for s in self.size:
            total_image += len(self.dict_image[s])
            if total_image==0:
                logging.warn("No files were found, check your input_path or image_type")
                
        logging.info("Convert complete")
        
        
class ConvertToFolderImage:
    """
    Create a folder Image given hdfs_path/local_path or pyspark.sql.dataframe.DataFrame
    

    Parameters
    ----------
    data : unicode, str or pyspark.sql.dataframe.DataFrame
        The input (parquet) filename or dataframe include Image
        Example: df, 'file:/absolute/path/to/file.parquet'

    input_path : unicode
        Path to a local file (parquet) or hdfs file containing the Image.
        Example: df, 'file:/absolute/path/to/file.parquet'
        
    output_path : unicode
        Path to a local file that function execute() will convert parquet/delta back to a Image file (jpg, png)
        Examples:
        output_path = "/home/username/tmp"

    write_mode : str
        Default: 'recovery'
        Specify the write_mode user want to
        If write_mode = 'recovery' 
        Function will convert Image to a multiple level of directory base on column path
        If write_mode != 'recovery'
        Function will convert all Image in parquet/hdfs file to one directory (output_path)

    raw_input_path : str
    
        Glob path that user input when use ConvertFromFolderVideo function
        For example: "/home/username/image_storage/images/**/*.jpg"
        When output it will replace '/home/username/image_storage/images/'  by ''
        That turn column path from absolute path to relative path
        
    keep_origin_jpg: bool | default False
        JPG is a lossly format when cv2 read jpg convert to array cv2.imread()
        And write back to jpg cv2.imwrite() it will cause 2 array 29% different
        If user want to keep origin array turn it on, but the image after convert will bigger than 400% compare with origin image

    debug : bool
        If debug=True:
        Write log into sdk.log file and print more debug information


    Examples
    --------
    ::
        ```
        from cads_sdk.nosql.codec import ConvertToFolderImage

        converter = ConvertToFolderImage(
            input_path = '/user/username/image/img_user_device_jpg_212_212.parquet',
            raw_input_path = "/home/username/image_storage/device_images/**/*.jpg",
            output_path = '/home/username/image_storage/abc/',
            debug = False
        )

        converter.execute()
        ```
        
        Function will convert all Image in hdfs:'/user/username/image/img_user_device_jpg_212_212.parquet' to absolute directory /home/username/image_storage/abc/
    """
    def __init__(
        self,
        data = None,
        input_path:str=None,
        output_path:str='./output',
        write_mode = "recovery",
        raw_input_path = "",
        debug = False
    ):
        from pyspark.sql.dataframe import DataFrame
        
        if debug:
            logging.basicConfig(level=logging.DEBUG, filename='sdk.log', filemode='w')
        else:
            logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
            
        check_parent_path = raw_input_path.split('*')
        if len(check_parent_path) > 1:
            raw_input_path = check_parent_path[0]
            
        if isinstance(data, (Path, PurePath)):
            input_path = str(data)
            data = None
        elif data is not None and isinstance(data, str):
            if ss.exists(data):
                input_path = data
                data = None
        elif isinstance(data, DataFrame):
            self.input_path = input_path
            self.output_path = output_path
            self.write_mode = write_mode
            self.raw_input_path = raw_input_path
            self.data = data

            self.debug = debug
            write_to_folder = ConvertToFolderImage(write_mode=write_mode, raw_input_path=raw_input_path, output_path=output_path, debug=debug).write_to_folder
            self.write_abtract = write_to_folder #data.foreach(write_to_folder)

            
        self.input_path = input_path
        self.output_path = output_path
        self.write_mode = write_mode
        self.raw_input_path = raw_input_path
        self.data = data
        
        self.debug = debug
        

    def convert_to_hdfs_path(self, input_path):
        if "file:" in input_path:
            return input_path
        else:
            if "hdfs://hdfs-cluster.datalake.bigdata.local:8020" not in os.path.dirname(input_path):
                return "hdfs://hdfs-cluster.datalake.bigdata.local:8020" + os.path.abspath(self.input_path.replace("hdfs:", ""))
            else:
                return input_path
            
    def check_delta(self, input_path):
        list_file = ss.ls(input_path)
        for f in list_file:
            if '_delta_log' in f:
                return True
        return False
        
    def mkdir_folder(self, output_path):
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            
    def get_spark(self):
        return ss.PySpark(driver_memory='32G', num_executors='8', executor_memory='4G', port='', yarn=False).spark
            
    def write_to_folder(self, row):
        if self.write_mode == "recovery":
            output_path = os.path.join(self.output_path, row.path.replace(self.raw_input_path, ""))
        else:
            base_path = os.path.basename(str(row.path))
            output_path = os.path.join(self.output_path, base_path)
        
        if self.debug:
            logging.debug("image_path: {}, row.image: {row.image}")
            
        self.mkdir_folder(os.path.dirname(output_path))
        with open(output_path, 'wb') as f:
            f.write(row.image)
            
        # if self.keep_origin_jpg:
        #     with open(output_path, 'wb') as f:
        #         f.write(row.image)
        # else:
        #     img = cv2.imdecode(np.frombuffer(row.image, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        #     # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #     cv2.imwrite(output_path, img)
            
            
    def execute(self):
        self.mkdir_folder(os.path.dirname(self.output_path))
        spark = self.get_spark()
        if self.data:
            self.data.foreach(self.write_abtract)
        else:
            if self.check_delta(self.input_path):
                logging.info("Detect Delta File")
                df = ss.sql(f"""select * from delta.`{self.input_path}`""")
            else:
                df = ss.sql(f"""select * from parquet.`{self.input_path}`""")
            df.foreach(self.write_to_folder)
        logging.info("Convert complete")
            
            
#---------------------------------#     
#------- VIDEO SESSION -----------#
#---------------------------------#
from abc import abstractmethod
from io import BytesIO
import logging

import numpy as np
import zlib

class ConvertFromFolderVideo:
    def __init__(
        self,
        input_path,
        output_path,
        table_name = '',
        database = '',
        repartition=True,
        numPartition=None,
        file_format = 'parquet',
        compression = 'zstd',
        input_recursive = True,
        thumbnail_width = 256,
        thumbnail_height = 144,

        
        debug=False
    ):
        
        self.input_path = input_path
        self.output_path = output_path
        self.table_name = table_name
        self.database = database
        self.input_recursive = input_recursive
        self.repartition = repartition
        self.numPartition = numPartition
        self.compression = compression
        self.file_format = file_format
        
        self.thumbnail_width = thumbnail_width
        self.thumbnail_height = thumbnail_height
        
        self.debug = debug
        
        if debug:
            self.temp_folder = tempfile.TemporaryDirectory(dir='./tmp_sdk')
            self.tmp_file = os.path.join(self.temp_folder.name, 'sdk.log')
            self.log_file = open(self.tmp_file, 'w+')
            logging.basicConfig(level=logging.DEBUG, filename=self.tmp_file, filemode='w+')
        else:
            logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
            
            
    def convert_to_hdfs_path(self, input_path):
        if "file:" in input_path:
            return input_path
        else:
            if "hdfs://hdfs-cluster.datalake.bigdata.local:8020" not in os.path.dirname(input_path):
                return "hdfs://hdfs-cluster.datalake.bigdata.local:8020" + os.path.abspath(input_path.replace("hdfs:", ""))
            else:
                return input_path

    def coalesce_dataframe(self, spark_df, numPartition):
        if numPartition:
            return spark_df.coalesce(numPartition)
        return spark_df
    
    def write_to_path(self, spark_df, output_path, table_name = '', database='', numPartition=8, compression='zstd'):
        if '.parquet' in output_path.lower():
            file_format = 'parquet'
        else:
            file_format = 'delta'
            
        if "file:" in output_path:
            self.coalesce_dataframe(spark_df, numPartition).write \
                .format(file_format) \
                .option('compression', compression) \
                .mode('overwrite') \
                .option("path", output_path) \
                .save()
        else:
            if table_name == '' or database == '':
                raise ValueError("You must add table_name and database")
            self.coalesce_dataframe(spark_df, numPartition).write \
                .format(file_format) \
                .option('compression', compression) \
                .mode('overwrite') \
                .option("path", output_path) \
                .saveAsTable(database + '.' + table_name)
            
            #     pass
            # spark_df.coalesce(numPartition) \
            #         .write \
            #         .format(file_format) \
            #         .option('compression', compression) \
            #         .mode('overwrite') \
            #         .option("path", output_path) \
            #         .save()
               


            
    def row_generator(self, partitionData):
        """Returns a dict of row input to rdd spark dataframe"""
        for row in partitionData:
            path = row.path
            if self.debug:
                print(f"Convert video {path}")#, file=self.log_file)

            cap = cv2.VideoCapture(path)
            frame_size = (int(cap.get(3)), int(cap.get(4)))
            frame_number = cap.get(cv2.CAP_PROP_FRAME_COUNT) / 2
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number-1)
            res, frame = cap.read()
            frame = cv2.resize(frame, (self.thumbnail_width, self.thumbnail_height))
            # frame = frame[:, :, (2, 1, 0)]
            duration = cap.get(cv2.CAP_PROP_FRAME_COUNT)/cap.get(cv2.CAP_PROP_FPS)
            
            row_dict = {
                'path': path,
                'thumbnail': frame,
                'duration': duration,
                'frame_size': str(frame_size),
                'video': open(path, "rb").read()}
            
            yield dict_to_spark_row(self.unischema, row_dict)
    
    def create_dataframe(self, spark, Schema, input_files):
        spark_df = spark.createDataFrame(pd.DataFrame(input_files, columns=['path']))
        self.unischema = Schema
        return spark.createDataFrame(spark_df.rdd.mapPartitions(self.row_generator), Schema.as_spark_schema())
        
    def get_spark(self):
        return ss.PySpark(driver_memory='32G', num_executors='4', executor_memory='4G', port='', yarn=False).spark
    
    def get_schema(self):
        return Unischema('VideoShema', [
            UnischemaField('path', np.str_, (), ScalarCodec(StringType()), False),
            UnischemaField('thumbnail', np.uint8, (self.thumbnail_height, self.thumbnail_width, 3), CompressedImageCodec('.jpg'), False),
            UnischemaField('duration', np.float_, (), ScalarCodec(FloatType()), False),
            UnischemaField('frame_size', np.str_, (), ScalarCodec(StringType()), False),
            UnischemaField('video', np.bytes_, (), petastorm.codecs.VideoCodec(), False)
        ])
    
    def execute(self):
        ROWGROUP_SIZE_MB = 256
        input_files = sorted(glob(self.input_path, recursive=self.input_recursive))
        self.output_path = self.convert_to_hdfs_path(self.output_path)
        
        spark = self.get_spark()
        Schema = self.get_schema()
        
        if input_files:
            logging.info(f"Write at path: {self.output_path}")
            logging.info(f"Save metadata at: {self.table_name}")
            
            with materialize_dataset(spark, self.output_path, Schema, ROWGROUP_SIZE_MB):
                self.write_to_path(spark_df = self.create_dataframe(spark=spark,
                                      Schema=Schema,
                                      input_files=input_files),

                                output_path = self.output_path,
                                table_name = self.table_name, 
                                database = self.database,
                                numPartition = self.numPartition,
                                compression = self.compression)
        else:
            logging.warn("No files were found, check your input_path")
            
        logging.info("Convert complete")
            

class ConvertFromVideo2Image:
    """
    Create a parquet/delta file given local Video file
    

    Parameters
    ----------
    input_path : unicode, str 
        The input filename include ``mp4``
        Just only 1 video at the time
        Examples:
        input_path="**/*.mp4"

    output_path : unicode
        Ouput directory location maybe file:/ (local file) or hdfs:/ (datalake path)
        Examples:
        output_path = "file:/home/username/"
        output_path = "hdfs:/user/username/"
        
    table_name : str
        Table_name store metadata
        User should input table_name follow dwh convention: img_abc, vid_abc, audio_abc
        Examples: img_abc
        
    database : str
        Database to store metadata
        User should input database follow dwh convention: default
        Examples: default
        

    repartition : bool 
        Default: False
        Data will be repartition to target file size
        
    numPartition : int
        Default None
        Number of part each user want to seperate parquet file into

    file_format : str
        Default: parquet
        File format user want to write parquet/delta
        
    compression: str 
        Default: zstd
        Compression method user want to compress parquet file
        Value: None, zstd, snappy
        See spark.sql.parquet.compression.codec
        https://spark.apache.org/docs/2.4.3/sql-data-sources-parquet.html
        
    image_type: str
        Default: jpg
        Value png or jpg
        
    image_color : int
        Default: 3
        Value 3, 2 or 1, shape of image have color is 3 or 1 if gray image
        
    size : List of Tuple
        Default: jpg
        List size user want to resize or padding
        Examples: size = [(320, 180), (500, 100)]
        
    resize_mode : str
        Default: None
        Value: None, padding, resize
        Mode of image user want to resize
        If in folder user have various size of image, 300, 400 500
        User will add size = 500:
        And resize_mode  = 'padding'
        Then function will convert all image 300, 400, 500 to shape of 500
    
    input_recursive : bool
        Default: True
        If True: 
        will loop through folder to get all pattern

    debug : bool
        If debug=True:
        Write log into sdk.log file and print more debug information


    Examples
    --------
    from cads_sdk.nosql.converter import ConvertFromVideo2Image
    converter = ConvertFromVideo2Image(
                  input_path='/home/username/image_storage/vid/palawan1.mp4',
                  input_recursive = False,
                  output_path = f"file:/home/username/image_storage/vid_image.parquet",
                 )

    converter.execute()
    
    """
    def __init__(
        self,
        input_path,
        output_path,
        table_name = '',
        database = '',
        repartition=True,
        numPartition=None,
        file_format = 'parquet',
        compression = 'zstd',
        input_recursive = False,
        thumbnail_width = 1280,
        thumbnail_height = 720,

        
        debug=False
    ):
        
        self.input_path = input_path
        self.output_path = output_path
        self.table_name = table_name
        self.database = database
        self.input_recursive = input_recursive
        self.repartition = repartition
        self.numPartition = numPartition
        self.compression = compression
        self.file_format = file_format
        
        self.thumbnail_width = thumbnail_width
        self.thumbnail_height = thumbnail_height
        
        self.debug = debug
        
        if debug:
            self.temp_folder = tempfile.TemporaryDirectory(dir='./tmp_sdk')
            self.tmp_file = os.path.join(self.temp_folder.name, 'sdk.log')
            self.log_file = open(self.tmp_file, 'w+')
            logging.basicConfig(level=logging.DEBUG, filename=self.tmp_file, filemode='w+')
        else:
            logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
            
            
    def convert_to_hdfs_path(self, input_path):
        if "file:" in input_path:
            return input_path
        else:
            if "hdfs://hdfs-cluster.datalake.bigdata.local:8020" not in os.path.dirname(input_path):
                return "hdfs://hdfs-cluster.datalake.bigdata.local:8020" + os.path.abspath(input_path.replace("hdfs:", ""))
            else:
                return input_path

    def coalesce_dataframe(self, spark_df, numPartition):
        if numPartition:
            return spark_df.coalesce(numPartition)
        return spark_df
    
    def write_to_path(self, spark_df, output_path, table_name = '', database='', numPartition=8, compression='zstd'):
        if '.parquet' in output_path.lower():
            file_format = 'parquet'
        else:
            file_format = 'delta'
            
        if "file:" in output_path:
            self.coalesce_dataframe(spark_df, numPartition).write \
                .format(file_format) \
                .option('compression', compression) \
                .mode('overwrite') \
                .option("path", output_path) \
                .save()
        else:
            if table_name == '' or database == '':
                raise ValueError("You must add table_name and database")
            self.coalesce_dataframe(spark_df, numPartition).write \
                .format(file_format) \
                .option('compression', compression) \
                .mode('overwrite') \
                .option("path", output_path) \
                .saveAsTable(database + '.' + table_name)
            
            #     pass
            # spark_df.coalesce(numPartition) \
            #         .write \
            #         .format(file_format) \
            #         .option('compression', compression) \
            #         .mode('overwrite') \
            #         .option("path", output_path) \
            #         .save()
               


            
    def row_generator(self, partitionData):
        """Returns a dict of row input to rdd spark dataframe"""
        for row in partitionData:
            frame_id = row.frame_id
            if self.debug:
                print(f"Convert video {path}")#, file=self.log_file)
                
            cap = cv2.VideoCapture(row.path)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id-1)
            res, frame = cap.read()
            # frame = cv2.resize(frame, (self.thumbnail_width, self.thumbnail_height))
            # frame = frame[:, :, (2, 1, 0)]
            
            row_dict = {
                'frame_id': row.frame_id,
                'path': row.path,
                'duration': row.duration,
                'frame_size': row.frame_size,
                'total_frame': row.total_frame,
                'frame': frame
            }
            
            yield dict_to_spark_row(self.unischema, row_dict)
    
    def create_dataframe(self, spark, Schema, input_files):
        path = input_files
        cap = cv2.VideoCapture(path)
        frame_size = (int(cap.get(3)), int(cap.get(4)))
        duration = cap.get(cv2.CAP_PROP_FRAME_COUNT)/cap.get(cv2.CAP_PROP_FPS)
        total_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)

        pdf = pd.DataFrame(range(int(total_frame)), columns = ['frame_id'])
        pdf['path'] = path
        pdf['duration'] = duration
        pdf['frame_size'] = str(frame_size)
        pdf['total_frame'] = total_frame
        
        spark_df = spark.createDataFrame(pdf)
        self.unischema = Schema
        
        self.thumbnail_width = frame_size[0]
        self.thumbnail_height = frame_size[1]
        
        return spark.createDataFrame(spark_df.rdd.mapPartitions(self.row_generator), Schema.as_spark_schema())
        
    def get_spark(self):
        return ss.PySpark(driver_memory='32G', num_executors='4', executor_memory='4G', port='', yarn=False).spark
    
#     def get_schema(self):
#         return Unischema('VideoShema', [
#             UnischemaField('path', np.str_, (), ScalarCodec(StringType()), False),
#             UnischemaField('thumbnail', np.uint8, (self.thumbnail_height, self.thumbnail_width, 3), CompressedImageCodec('.jpg'), False),
#             UnischemaField('duration', np.float_, (), ScalarCodec(FloatType()), False),
#             UnischemaField('frame_size', np.str_, (), ScalarCodec(StringType()), False),
#             UnischemaField('video', np.bytes_, (), petastorm.codecs.VideoCodec(), False)
#         ])
    
    def get_schema(self):
        return Unischema('VideoImage', [
            UnischemaField('frame_id', np.int, (), ScalarCodec(IntegerType()), False),
            UnischemaField('path', np.str_, (), ScalarCodec(StringType()), False),
            UnischemaField('duration', np.float_, (), ScalarCodec(FloatType()), False),
            UnischemaField('frame_size', np.str_, (), ScalarCodec(StringType()), False),
            UnischemaField('total_frame', np.str_, (), ScalarCodec(FloatType()), False),
            UnischemaField('frame', np.uint8, (self.thumbnail_height, self.thumbnail_width, 3), CompressedImageCodec('.jpg'), False),
        ])
    
    def execute(self):
        ROWGROUP_SIZE_MB = 256
        input_files = self.input_path #sorted(glob(self.input_path, recursive=self.input_recursive))
        self.output_path = self.convert_to_hdfs_path(self.output_path)
        
        spark = self.get_spark()
        Schema = self.get_schema()


        
        if input_files:
            logging.info(f"Write at path: {self.output_path}")
            logging.info(f"Save metadata at: {self.table_name}")
            
            with materialize_dataset(spark, self.output_path, Schema, ROWGROUP_SIZE_MB):
                self.write_to_path(spark_df = self.create_dataframe(spark=spark,
                                      Schema=Schema,
                                      input_files=input_files),

                                output_path = self.output_path,
                                table_name = self.table_name, 
                                database = self.database,
                                numPartition = self.numPartition,
                                compression = self.compression)
        else:
            logging.warn("No files were found, check your input_path")
            
        logging.info("Convert complete")
        

class ConvertToFolderVideo:
    """
    Create a folder Video given hdfs_path/local_path or pyspark.sql.dataframe.DataFrame
    

    Parameters
    ----------
    data : unicode, str or pyspark.sql.dataframe.DataFrame
        The input filename to load video or dataframe include video

    input_path : unicode
        Path to a local file or hdfs file containing the video.
        
    output_path : unicode
        Path to a local file that function execute() will convert parquet/delta back to a video file (mp4, ts...) 

    write_mode : str
        Specify the write_mode user want to
        If write_mode = 'recovery' 
        Function will convert video to a multiple level of directory base on column path
        If write_mode != 'recovery'
        Function will convert all video in parquet/hdfs file to one directory (output_path)

    raw_input_path : str
        Glob path that user input when use ConvertFromFolderVideo function
        For example: "/home/username/image_storage/audio_mp3/*.mp3"
        When output it will replace '/home/username/image_storage/audio_mp3/'  by ''
        That turn column path from absolute path to relative path

    debug : bool
        If debug=True:
        Write log into sdk.log file and print more debug information


    Examples
    --------
    ::
        ```
        converter = ConvertToFolderVideo(
        input_path = 'file:/home/username/image_storage/vid.parquet',
        output_path = './abc'
        )

        converter.execute()
        ```
        
        Function will convert all video in file:/home/username/image_storage/vid.parquet to relative directory ./abc
    """

    def __init__(
        self,
        data = None,
        input_path:str=None,
        output_path:str='./output',
        write_mode = "recovery",
        raw_input_path = "",
        debug = False
    ):
        from pyspark.sql.dataframe import DataFrame
        
        if debug:
            logging.basicConfig(level=logging.DEBUG, filename='sdk.log', filemode='w')
        else:
            logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
            
        check_parent_path = raw_input_path.split('*')
        if len(check_parent_path) > 1:
            raw_input_path = check_parent_path[0]
            
        if isinstance(data, (Path, PurePath)):
            input_path = str(data)
            data = None
        elif data is not None and isinstance(data, str):
            if ss.exists(data):
                input_path = data
                data = None
        elif isinstance(data, DataFrame):
            self.input_path = input_path
            self.output_path = output_path
            self.write_mode = write_mode
            self.raw_input_path = raw_input_path
            self.data = data

            self.debug = debug
            write_to_folder = ConvertToFolderAudio(write_mode=write_mode, raw_input_path=raw_input_path, output_path=output_path, debug=debug).write_to_folder
            self.write_abtract = write_to_folder #data.foreach(write_to_folder)

            
        self.input_path = input_path
        self.output_path = output_path
        self.write_mode = write_mode
        self.raw_input_path = raw_input_path
        self.data = data
        
        self.debug = debug
        

    def convert_to_hdfs_path(self, input_path):
        if "file:" in input_path:
            return input_path
        else:
            if "hdfs://hdfs-cluster.datalake.bigdata.local:8020" not in os.path.dirname(input_path):
                return "hdfs://hdfs-cluster.datalake.bigdata.local:8020" + os.path.abspath(self.input_path.replace("hdfs:", ""))
            else:
                return input_path
            
    def check_delta(self, input_path):
        list_file = ss.ls(input_path)
        for f in list_file:
            if '_delta_log' in f:
                return True
        return False
        
    def mkdir_folder(self, output_path):
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            
    def get_spark(self):
        return ss.PySpark(driver_memory='32G', num_executors='8', executor_memory='4G', port='', yarn=False).spark
            
    def write_to_folder(self, row=None):
        if self.write_mode == "recovery":
            output_path = os.path.join(self.output_path, row.path.replace(self.raw_input_path, ""))
        else:
            base_path = os.path.basename(str(row.path))
            output_path = os.path.join(self.output_path, base_path)
        if self.debug:
            logging.info(output_path)
        with open(output_path, 'wb') as wfile:
            wfile.write(row.video)
            
            
    def execute(self):
        self.mkdir_folder(os.path.dirname(self.output_path))
        spark = self.get_spark()
        if self.data:
            self.data.foreach(self.write_abtract)
        else:
            if self.check_delta(self.input_path):
                logging.info("Detect Delta File")
                df = ss.sql(f"""select * from delta.`{self.input_path}`""")
            else:
                df = ss.sql(f"""select * from parquet.`{self.input_path}`""")
            df.foreach(self.write_to_folder)
        logging.info("Convert complete")
        
        
#---------------------------------#     
#------- AUDIO SESSION -----------#
#---------------------------------#

import_or_install("pydub")
import pydub
import_or_install("scipy")
from scipy.io import wavfile        
        
    
class ConvertFromFolderAudio:
    """
    Create a parquet/delta file given local Image directory
    

    Parameters
    ----------
    input_path : unicode, str 
        The input filename include ``png``, ``jpeg`` image
        User can add system file pattern like *
        Examples:
        input_path="**/*.jpg"
        input_path="**/*.png"
        This pattern get all jpg in folder with different directory levels
        View https://docs.python.org/3/library/glob.html

    output_path : unicode
        Ouput directory location maybe file:/ (local file) or hdfs:/ (datalake path)
        Examples:
        output_path = "file:/home/username/"
        output_path = "hdfs:/user/username/"
        
    table_name : str
        Table_name store metadata
        User should input table_name follow dwh convention: img_abc, vid_abc, audio_abc
        Examples: img_abc
        
    database : str
        Database to store metadata
        User should input database follow dwh convention: default
        Examples: default
        

    repartition : bool 
        Default: False
        Data will be repartition to target file size
        
    numPartition : int
        Default None
        Number of part each user want to seperate parquet file into

    file_format : str
        Default: parquet
        File format user want to write parquet/delta
        
    compression: str 
        Default: zstd
        Compression method user want to compress parquet file
        Value: None, zstd, snappy
        See spark.sql.parquet.compression.codec
        https://spark.apache.org/docs/2.4.3/sql-data-sources-parquet.html
        
    
    input_recursive : bool
        Default: True
        If True: 
        will loop through folder to get all pattern

    debug : bool
        If debug=True:
        Write log into sdk.log file and print more debug information


    Examples
    --------
    ::
        ```
        from cads_sdk.nosql.converter import ConvertFromFolderAudio
        # Test case 1, write with mp3 audio:
        converter = ConvertFromFolderAudio(
                      input_path='./audio_mp3/*.mp3',
                      input_recursive = False,
                      output_path = f"file:/home/username/image_storage/audio_mp3.parquet",
                     )
        converter.execute()

        # Test case 2, write with PCM audio:
        converter = ConvertFromFolderAudio(
                      input_path='./audio_pcm/*.pcm',
                      input_recursive = False,
                      output_path = f"file:/home/username/image_storage/audio_pcm.parquet",
                     )

        converter.execute()

        # Test case 3, write with Wav audio:
        converter = ConvertFromFolderAudio(
                      input_path='./audio_wav/*.wav',
                      input_recursive = False,
                      output_path = f"file:/home/username/image_storage/audio_wav.parquet",
                     )

        converter.execute()
        ```
    """
    
    def __init__(
        self,
        input_path,
        output_path,
        table_name = '',
        database = '',
        repartition=False,
        numPartition=None,
        file_format = 'parquet',
        compression = 'zstd',
        input_recursive = False,

        debug=False
       
    ):
        
        self.input_path = input_path
        self.output_path = output_path
        self.table_name = table_name
        self.database = database
        self.input_recursive = input_recursive
        self.repartition = repartition
        self.numPartition = numPartition
        self.compression = compression
        self.file_format = file_format
        self.debug = debug
        
        if debug:
            self.temp_folder = tempfile.TemporaryDirectory(dir='./tmp_sdk')
            self.tmp_file = os.path.join(self.temp_folder.name, 'sdk.log')
            self.log_file = open(self.tmp_file, 'w+')
            logging.basicConfig(level=logging.DEBUG, filename=self.tmp_file, filemode='w+')
        else:
            logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
            
    def guess_type(self, input_path):
        dict_type = {
            'wav': np.float64,
            'pcm': np.float64,
            'mp3': np.int16,
            'mp4': np.bytes_,
            'jpg': np.uint8,
            'png': np.uint8
        }
        
        for t in dict_type.keys():
            if "." + t in input_path:
                return t
            
    def numpy_map_type(self, input_path):
        dict_type = {
            'wav': np.bytes_,
            'pcm': np.bytes_,
            'mp3': np.bytes_,
            'mp4': np.bytes_,
            'jpg': np.uint8,
            'png': np.uint8
        }
        
        return dict_type[self.guess_type(input_path)]
    
    
    def coalesce_dataframe(self, spark_df, numPartition):
        if numPartition:
            return spark_df.coalesce(numPartition)
        return spark_df
    
    def write_to_path(self, spark_df, output_path, table_name = '', database='', numPartition=8, compression='zstd'):
        if '.parquet' in output_path.lower():
            file_format = 'parquet'
        else:
            file_format = 'delta'
            
        if "file:" in output_path:
            self.coalesce_dataframe(spark_df, numPartition).write \
                .format(file_format) \
                .option('compression', compression) \
                .mode('overwrite') \
                .option("path", output_path) \
                .save()
        else:
            if table_name == '' or database == '':
                raise ValueError("You must add table_name and database")
            self.coalesce_dataframe(spark_df, numPartition).write \
                .format(file_format) \
                .option('compression', compression) \
                .mode('overwrite') \
                .option("path", output_path) \
                .saveAsTable(database + '.' + table_name)

            
    def row_generator(self, partitionData):
        """Returns a single entry in the generated dataset. Return a bunch of random values as an example."""
        for row in partitionData:
            path = row.path
            if self.debug:
                logging.debug(f"Convert audio {path}")

            if self.guess_type(path) == 'pcm':
                samplerate, data = read_pcm(path)
                channels = 1

                data = data.tobytes()

            elif self.guess_type(path) == 'wav':
                samplerate, data = wavfile.read(path)
                if len(data.shape) == 2:
                    data = data.T
                    channels = 2
                else:
                    channels = 1

                with open(path, 'rb') as file:
                    data = file.read()

            if self.guess_type(path) == 'pcm':
                samplerate, data = self.read_pcm(path)
                channels = 1

            elif self.guess_type(path) == 'mp3':
                samplerate, data = read_mp3(path)
                if len(data.shape) == 2:
                    data = data.T
                    channels = 2
                else:
                    channels = 1

                with open(path, 'rb') as file:
                    data = file.read()

            row_dict = {'path': path,
                    'samplerate': samplerate,
                    'channels': channels,
                    'audio': data}

            yield dict_to_spark_row(self.unischema, row_dict)
    
    def convert_to_hdfs_path(self, input_path):
        if "file:" in input_path:
            return input_path
        else:
            if "hdfs://hdfs-cluster.datalake.bigdata.local:8020" not in os.path.dirname(input_path):
                return "hdfs://hdfs-cluster.datalake.bigdata.local:8020" + os.path.abspath(self.input_path.replace("hdfs:", ""))
            else:
                return input_path
            
    def create_dataframe(self, spark, Schema, input_files):
        
        
        spark_df = spark.createDataFrame(pd.DataFrame(input_files, columns=['path']))
        self.unischema = Schema
        return spark.createDataFrame(spark_df.rdd.mapPartitions(self.row_generator), Schema.as_spark_schema())
        
    def get_spark(self):
        return ss.PySpark(driver_memory='32G', num_executors='8', executor_memory='4G', port='', yarn=False).spark
    
    def get_schema(self):
        return Unischema('Audio', [
            UnischemaField('path', np.str_, (), ScalarCodec(StringType()), False),
            UnischemaField('samplerate', np.int_, (), ScalarCodec(IntegerType()), False),
            UnischemaField('channels', np.int_, (), ScalarCodec(IntegerType()), False),
            UnischemaField('audio', self.numpy_map_type(self.input_path), (1000,), petastorm.codecs.AudioCodec(self.guess_type(self.input_path)), False)
        ])
    
    def execute(self):
        ROWGROUP_SIZE_MB = 256
        input_files = sorted(glob(self.input_path, recursive=self.input_recursive))
        self.output_path = self.convert_to_hdfs_path(self.output_path)
        
        spark = self.get_spark()
        Schema = self.get_schema()
        
        if input_files:
            logging.info(f"Write at path: {self.output_path}")
            logging.info(f"Save metadata at: {self.table_name}")
            
            with materialize_dataset(spark, self.output_path, Schema, ROWGROUP_SIZE_MB):
                self.write_to_path(spark_df = self.create_dataframe(spark=spark,
                                      Schema=Schema,
                                      input_files=input_files),

                                output_path = self.output_path,
                                table_name = self.table_name, 
                                database = self.database,
                                numPartition = self.numPartition,
                                compression = self.compression)
        else:
            logging.warn("No files were found, check your input_path")
            
        logging.info("Convert complete")
                
#             self.create_dataframe(spark=spark,
#                                   Schema=Schema,
#                                   input_files=input_files,
#                                   output_path=self.output_path,
#                                   table_name = self.table_name, 
#                                   database=self.database,
#                                   numPartition=self.numPartition,
#                                   compression=self.compression)
            
            
            
class ConvertToFolderAudio:
    """
    Create a folder Audio given hdfs_path/local_path or pyspark.sql.dataframe.DataFrame
    

    Parameters
    ----------
    data : unicode, str or pyspark.sql.dataframe.DataFrame
        The input filename to load Audio or dataframe include Audio

    input_path : unicode
        Path to a local file or hdfs file containing the audio.
        
    output_path : unicode
        Path to a local file that function execute() will convert parquet/delta back to a video file (pcm, mp3, wav...) 

    write_mode : str
        Specify the write_mode user want to
        If write_mode = 'recovery' 
        Function will convert audio to a multiple level of directory base on column path
        If write_mode != 'recovery'
        Function will convert all audio in parquet/hdfs file to one directory (output_path)

    raw_input_path : str
        Glob path that user input when use ConvertToFolderAudio function
        For example: "/home/username/image_storage/audio_mp3/*.mp3"
        When output it will replace '/home/username/image_storage/audio_mp3/'  by ''
        That turn column path from absolute path to relative path

    debug : bool
        If debug=True:
        Write log into sdk.log file and print more debug information


    Examples
    --------
    ::
        ```
        converter = ConvertToFolderAudio(
        input_path = 'file:/home/username/image_storage/audio_mp3.parquet',
        raw_input_path = '/home/username/image_storage/audio_mp3/*.mp3',
        output_path = './abc',
        write_mode = "recovery"
        )

        converter.execute()
        ```
        
        Function will convert all audio in file:/home/username/image_storage/audio_mp3.parquet to relative directory abc
    """
    def __init__(
        self,
        data = None,
        input_path:str=None,
        output_path:str='./output',
        write_mode = "recovery",
        raw_input_path = "",
        debug = False
    ):
        from pyspark.sql.dataframe import DataFrame
        
        if debug:
            logging.basicConfig(level=logging.DEBUG, filename='sdk.log', filemode='w')
        else:
            logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
            
        check_parent_path = raw_input_path.split('*')
        if len(check_parent_path) > 1:
            raw_input_path = check_parent_path[0]
            
        if isinstance(data, (Path, PurePath)):
            input_path = str(data)
            data = None
        elif data is not None and isinstance(data, str):
            if ss.exists(data):
                input_path = data
                data = None
        elif isinstance(data, DataFrame):
            self.input_path = input_path
            self.output_path = output_path
            self.write_mode = write_mode
            self.raw_input_path = raw_input_path
            self.data = data

            self.debug = debug
            write_to_folder = ConvertToFolderAudio(write_mode=write_mode, raw_input_path=raw_input_path, output_path=output_path, debug=debug).write_to_folder
            self.write_abtract = write_to_folder #data.foreach(write_to_folder)

            
        self.input_path = input_path
        self.output_path = output_path
        self.write_mode = write_mode
        self.raw_input_path = raw_input_path
        self.data = data
        
        self.debug = debug
        

    def convert_to_hdfs_path(self, input_path):
        if "file:" in input_path:
            return input_path
        else:
            if "hdfs://hdfs-cluster.datalake.bigdata.local:8020" not in os.path.dirname(input_path):
                return "hdfs://hdfs-cluster.datalake.bigdata.local:8020" + os.path.abspath(self.input_path.replace("hdfs:", ""))
            else:
                return input_path
            
    def check_delta(self, input_path):
        list_file = ss.ls(input_path)
        for f in list_file:
            if '_delta_log' in f:
                return True
        return False
        
    def mkdir_folder(self, output_path):
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            
    def get_spark(self):
        return ss.PySpark(driver_memory='32G', num_executors='8', executor_memory='4G', port='', yarn=False).spark
            
    def write_to_folder(self, row=None):
        if self.write_mode == "recovery":
            output_path = os.path.join(self.output_path, row.path.replace(self.raw_input_path, ""))
        else:
            base_path = os.path.basename(str(row.path))
            output_path = os.path.join(self.output_path, base_path)
        if self.debug:
            logging.info(output_path)
        with open(output_path, 'wb') as wfile:
            wfile.write(row.audio)
            
            
    def execute(self):
        self.mkdir_folder(os.path.dirname(self.output_path))
        spark = self.get_spark()
        if self.data:
            self.data.foreach(self.write_abtract)
        else:
            if self.check_delta(self.input_path):
                logging.info("Detect Delta File")
                df = ss.sql(f"""select * from delta.`{self.input_path}`""")
            else:
                df = ss.sql(f"""select * from parquet.`{self.input_path}`""")
            df.foreach(self.write_to_folder)
        logging.info("Convert complete")