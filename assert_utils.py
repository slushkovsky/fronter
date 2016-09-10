import os
import inspect

import numpy as np
import cv2

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
    ''' 
    Check if object is an existed path
    
    Parameters
    ----------
    @obj <any_type>     An object
    ----------
    Return <bool>
    '''
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
    if isinstance(obj, (np.ndarray, list)):
        for ch in obj:
            if not isinstance(ch, (np.uint8, int, float)):
                return False
        return True
    return isinstance(obj, (np.uint8, int))

def is_list_of(obj, func=None, need_type=None):
    ''' 
    Check if object is a list of specifyed type. Also you can specify a 
    assert_utils function to check list objects. You shold specify type 
    or function!
    
    Parameters
    ----------
    @obj        <any_type>       An object
    @func       <function>       assert_utils function
    @need_type  <class type>     Type of elemets
    ----------
    Return <bool>
    '''
    assert inspect.isfunction(func) or func is None
    assert isinstance(need_type, type) or need_type is None
    assert (need_type == None) != (func == None)
    
    if isinstance(obj, (list, np.ndarray, np.array)):
        for ob in obj:
            if func != None:
                if not func(ob):
                    return False
            else:
                if not isinstance(ob, need_type):
                    return False
            return True
    return False

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

