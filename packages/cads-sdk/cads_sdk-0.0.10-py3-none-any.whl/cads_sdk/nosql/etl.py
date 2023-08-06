import pydub
import numpy as np
import cv2

def read_mp3(f, normalized=False):
    """MP3 to numpy array"""
    
    a = pydub.AudioSegment.from_mp3(f)
    y = np.array(a.get_array_of_samples())
    if a.channels == 2:
        y = y.reshape((-1, 2))
    if normalized:
        return a.frame_rate, np.float32(y) / 2**15
    else:
        return a.frame_rate, y
    
    
        
def read_pcm(input_path, dtype='float64'):
    with open(input_path, 'rb') as file:
        y = file.read()
        y = np.frombuffer(y, dtype = 'int16')
        i = np.iinfo(y.dtype)
        abs_max = 2 ** (i.bits - 1)
        offset = i.min + abs_max
        y = (y.astype(dtype) - offset) / abs_max
    return 8000, y

def padding(img, expected_size, borderType=cv2.BORDER_CONSTANT, value=(255,255,255)):
    delta_width = expected_size[0] - img.shape[0]
    delta_height = expected_size[1] - img.shape[1]
    pad_width = delta_width // 2
    pad_height = delta_height // 2
    # padding = (pad_width, pad_height, delta_width - pad_width, delta_height - pad_height)

    return cv2.copyMakeBorder(img, pad_width, delta_width - pad_width, pad_height, delta_height - pad_height, borderType, value=value)