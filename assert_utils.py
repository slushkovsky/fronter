import os

import numpy as np

def is_image(obj):
    ''' 
    Check if object is an opencv image 
    
    Parameters
    ----------
    @obj <any_type>     An object
    ----------
    Return <bool>
    '''
    if isinstance(obj, np.ndarray):
        return len(obj.shape) in [2, 3]
    else:
        return False

def is_existed_path(obj):
    if isinstance(obj, str):
        return os.path.exists(obj)
    return False

def is_pixel(obj):
    ''' 
    Check if object is a pixel (opencv in particular) 
    
    Parameters
    ----------
    @obj <any_type>     An object
    ----------
    Return <bool>
    '''
    if isinstance(obj, np.ndarray):
        for ch in obj:
            if not isinstance(ch, np.uint8):
                return False
        return True
    return isinstance(obj, np.uint8)

def is_tuple(obj, need_len, need_type):
    ''' 
    Check if object is a tuple, with specifyed length and 
    type of elements. 
    
    Parameters
    ----------
    @obj        <any_type>      An object
    @need_len   <int>           Length of typle
    @need_type  <class type>    Type of elements
    ----------
    Return <bool>
    '''
    assert isinstance(need_len, int)
    assert isinstance(need_type, type)
    if isinstance(obj, tuple):
        if len(obj) == need_len:
            return all([isinstance(v, need_type) for v in obj])
    return False

def has_pixel_ch(pixel):
    ''' 
    Check if pixel has a few chanels. This function doesn't check if
    argument is a pixel.
    
    Parameters
    ----------
    @pixel <any_type> 
    ----------
    Return <bool>
    '''
    return isinstance(pixel, (np.ndarray, list))

