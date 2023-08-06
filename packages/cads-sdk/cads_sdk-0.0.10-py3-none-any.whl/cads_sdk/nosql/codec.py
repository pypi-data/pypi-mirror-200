from pyspark.sql.types import StructField, StructType, IntegerType, BinaryType, StringType, TimestampType, FloatType

from spark_sdk.utils import import_or_install
import_or_install("petastorm")
import petastorm
from petastorm.etl.dataset_metadata import materialize_dataset
from petastorm.codecs import ScalarCodec, NdarrayCodec #, CompressedImageCodec
from petastorm.unischema import dict_to_spark_row, Unischema, UnischemaField

from cads_sdk.nosql.etl import read_mp3,read_pcm
from zipfile import ZipFile

from abc import abstractmethod

import numpy as np
from io import BytesIO

try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    os.system("pip install --proxy http://proxy.hcm.fpt.vn:80 opencv-python")
    import cv2
    OPENCV_AVAILABLE = False
    
    
safe_modules = {'__builtin__',
 'builtins',
 'collections',
 'copy_reg',
 'decimal',
 'numpy',
 'petastorm',
 'pyspark',
 'cads_sdk',
 'spark_sdk'}
petastorm.etl.legacy.safe_modules = safe_modules


class DataframeColumnCodec(object):
    """The abstract base class of codecs."""

    @abstractmethod
    def encode(self, unischema_field, value):
        raise RuntimeError('Abstract method was called')

    @abstractmethod
    def decode(self, unischema_field, value):
        raise RuntimeError('Abstract method was called')

    @abstractmethod
    def spark_dtype(self):
        """Spark datatype to be used for underlying storage"""
        raise RuntimeError('Abstract method was called')

    @abstractmethod
    def __str__(self):
        """String representation sufficient to re-construct this Codec"""
        raise RuntimeError('Abstract method was called')
    

class CompressedImageCodec(DataframeColumnCodec):
    def __init__(self, image_codec='png', quality=95):
        """CompressedImageCodec would compress/encompress images.
        :param image_codec: any format string supported by opencv. e.g. ``png``, ``jpeg``
        :param quality: used when using ``jpeg`` lossy compression
        """
        assert OPENCV_AVAILABLE, "{} requires opencv-python to be installed".format(type(self).__name__)

        self._image_codec = '.' + image_codec
        self._quality = quality

    @property
    def image_codec(self):
        """Returns image_codec type use by the codec: png or jpeg."""
        return self._image_codec[1:]

    def encode(self, unischema_field, value):
        """Encodes the image using OpenCV."""
        if unischema_field.numpy_dtype != value.dtype:
            raise ValueError("Unexpected type of {} feature, expected {}, got {}".format(
                unischema_field.name, unischema_field.numpy_dtype, value.dtype
            ))

        if not _is_compliant_shape(value.shape, unischema_field.shape):
            raise ValueError("Unexpected dimensions of {} feature, expected {}, got {}".format(
                unischema_field.name, unischema_field.shape, value.shape
            ))

        if len(value.shape) == 2:
            # Greyscale image
            image_bgr_or_gray = value
        elif len(value.shape) == 3 and value.shape[2] == 3:
            # Convert RGB to BGR
            # image_bgr_or_gray = value[:, :, (2, 1, 0)]
            # Not convert, convert color for what?
            image_bgr_or_gray = value
        else:
            raise ValueError('Unexpected image dimensions. Supported dimensions are (H, W) or (H, W, 3). '
                             'Got {}'.format(value.shape))

        _, contents = cv2.imencode(self._image_codec,
                                   image_bgr_or_gray,
                                   [int(cv2.IMWRITE_JPEG_QUALITY), self._quality])
        return bytearray(contents)

    def decode(self, unischema_field, value):
        """Decodes the image using OpenCV."""
        # cv returns a BGR or grayscale image. Convert to RGB (unless a grayscale image).
        image_bgr_or_gray = cv2.imdecode(np.frombuffer(value, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        if len(image_bgr_or_gray.shape) == 2:
            # Greyscale image
            return image_bgr_or_gray
        elif len(image_bgr_or_gray.shape) == 3 and image_bgr_or_gray.shape[2] == 3:
            # Convert BGR to RGB (opencv assumes BGR)
            # why here convert back?
            # image_rgb = image_bgr_or_gray[:, :, (2, 1, 0)]
            return image_rgb
        else:
            raise ValueError('Unexpected image dimensions. Supported dimensions are (H, W) or (H, W, 3). '
                             'Got {}'.format(image_bgr_or_gray.shape))

    def spark_dtype(self):
        # Lazy loading pyspark to avoid creating pyspark dependency on data reading code path
        # (currently works only with make_batch_reader). We should move all pyspark related code into a separate module
        import pyspark.sql.types as sql_types

        return sql_types.BinaryType()

    def __str__(self):
        """Represent this as the following form:
        >>> CompressedImageCodec(image_codec, quality)
        """
        return f'{type(self).__name__}(\'{self.image_codec}\', {self._quality})'
    
    

                
class ImageZipCodec:
    """Encodes a scalar into a spark dataframe field."""

    def __init__(self, spark_type):
        """Constructs a codec.
        :param spark_type: an instance of a Type object from :mod:`pyspark.sql.types`
        """
        self._spark_type = spark_type

    def encode(self, unischema_field, value):
        # Lazy loading pyspark to avoid creating pyspark dependency on data reading code path
        # (currently works only with make_batch_reader). We should move all pyspark related code into a separate module
        import pyspark.sql.types as sql_types

        return bytearray(value)

    def decode(self, unischema_field, value):
        """Decodes the image using OpenCV."""
        # cv returns a BGR or grayscale image. Convert to RGB (unless a grayscale image).
        image_bgr_or_gray = cv2.imdecode(np.frombuffer(value, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        if len(image_bgr_or_gray.shape) == 2:
            # Greyscale image
            return image_bgr_or_gray
        elif len(image_bgr_or_gray.shape) == 3 and image_bgr_or_gray.shape[2] == 3:
            # Convert BGR to RGB (opencv assumes BGR)
            return image_bgr_or_gray
        else:
            raise ValueError('Unexpected image dimensions. Supported dimensions are (H, W) or (H, W, 3). '
                             'Got {}'.format(image_bgr_or_gray.shape))

    def spark_dtype(self):
        return self._spark_type

    def __str__(self):
        """Represent this as the following form:
        >>> ScalarCodec(spark_type)
        """
        return f'{type(self).__name__}({type(self._spark_type).__name__}())'


def _is_compliant_shape(a, b):
    """Compares the shapes of two arguments.
    If size of a dimensions is None, this dimension size is ignored.
    Example:
    >>> assert _is_compliant_shape((1, 2, 3), (1, 2, 3))
    >>> assert _is_compliant_shape((1, 2, 3), (1, None, 3))
    >>> assert not _is_compliant_shape((1, 2, 3), (1, 10, 3))
    >>> assert not _is_compliant_shape((1, 2), (1,))
    :return: True, if the shapes are compliant
    """
    if len(a) != len(b):
        return False
    for i in range(len(a)):
        if a[i] and b[i]:
            if a[i] != b[i]:
                return False
    return True


        
#---------------------------------#     
#------- VIDEO SESSION -----------#
#---------------------------------#

class DataframeColumnCodec(object):
    """The abstract base class of codecs."""

    @abstractmethod
    def encode(self, unischema_field, value):
        raise RuntimeError('Abstract method was called')

    @abstractmethod
    def decode(self, unischema_field, value):
        raise RuntimeError('Abstract method was called')

    @abstractmethod
    def spark_dtype(self):
        """Spark datatype to be used for underlying storage"""
        raise RuntimeError('Abstract method was called')

    @abstractmethod
    def __str__(self):
        """String representation sufficient to re-construct this Codec"""
        raise RuntimeError('Abstract method was called')
        
        
class VideoCodec(DataframeColumnCodec):
    """Encodes numpy ndarray into, or decodes an ndarray from, a spark dataframe field."""

    def encode(self, unischema_field, value):

        return bytearray(value)


    def decode(self, unischema_field, value):
        return unischema_field.numpy_dtype(value)

    def spark_dtype(self):
        # Lazy loading pyspark to avoid creating pyspark dependency on data reading code path
        # (currently works only with make_batch_reader). We should move all pyspark related code into a separate module
        import pyspark.sql.types as sql_types

        return sql_types.BinaryType()

    def __str__(self):
        """Represent this as the following form:
        >>> NdarrayCodec()
        """
        return f'{type(self).__name__}()'
    
petastorm.codecs.VideoCodec = VideoCodec


#---------------------------------#     
#------- AUDIO SESSION -----------#
#---------------------------------#

class AudioCodec(DataframeColumnCodec):
    """Encodes numpy ndarray into, or decodes an ndarray from, a spark dataframe field."""
    def __init__(self, _audio_codec='mp3'):
        """CompressedImageCodec would compress/encompress images.
        :param _audio_codec: any format string. e.g. ``mp3``, ``pcm``, ``wav``
        """

        self._audio_codec = _audio_codec
    def encode(self, unischema_field, value):
#         expected_dtype = unischema_field.numpy_dtype
#         if isinstance(value, np.ndarray):
#             expected_dtype = " ".join(re.findall("[a-zA-Z]+", str(expected_dtype)))
#             value_dtype = " ".join(re.findall("[a-zA-Z]+", str(value.dtype.type)))
#             if expected_dtype != value_dtype:
#                 raise ValueError('Unexpected type of {} feature. '
#                                  'Expected {}. Got {}'.format(unischema_field.name, expected_dtype, value.dtype))

#             expected_shape = unischema_field.shape
            # if not _is_compliant_shape(value.shape, expected_shape):
            #     raise ValueError('Unexpected dimensions of {} feature. '
            #                      'Expected {}. Got {}'.format(unischema_field.name, expected_shape, value.shape))
        # else:
        #     raise ValueError('Unexpected type of {} feature. '
        #                      'Expected ndarray of {}. Got {}'.format(unischema_field.name, expected_dtype, type(value)))

        # memfile = BytesIO()
        # np.save(memfile, value)
        # return bytearray(memfile.getvalue())
        return bytearray(value)


    def decode(self, unischema_field, value):
        if self._audio_codec == 'pcm':
            data = np.frombuffer(value, dtype = 'float64')
            return 8000, data
            
        elif self._audio_codec == 'wav':
            from scipy.io import wavfile
            samplerate, data = wavfile.read(BytesIO(value))
            return samplerate, data
            
        elif self._audio_codec == 'mp3':
            samplerate, data = read_mp3(BytesIO(value))
            return samplerate, data
        return unischema_field.numpy_dtype(value)

    def spark_dtype(self):
        # Lazy loading pyspark to avoid creating pyspark dependency on data reading code path
        # (currently works only with make_batch_reader). We should move all pyspark related code into a separate module
        import pyspark.sql.types as sql_types

        return sql_types.BinaryType()

    def __str__(self):
        """Represent this as the following form:
        >>> NdarrayCodec()
        """
        return f'{type(self).__name__}()'

petastorm.codecs.AudioCodec = AudioCodec
