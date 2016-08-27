from math import fabs

from assert_utils import is_pixel, has_pixel_ch

def max_diff_func_color(sample_pixel, img_pixel):
    ''' 
    Compute the maximum pixels difference 
    
    Parameters
    ----------
    @sample_pixel <pixel>     A pixel of sample image
    @img_pixel    <pixel>     A pixel of image
    ----------
    Return <int>    Maximum pixels difference 
    '''
    assert is_pixel(sample_pixel) and is_pixel(img_pixel)
    assert has_pixel_ch(sample_pixel) == has_pixel_ch(img_pixel)
    max_diff = 0
    if has_pixel_ch(sample_pixel):
        for c in range(len(sample_pixel)):
            max_diff += max(255 - int(sample_pixel[c])
                                , int(sample_pixel[c]))
    else:
        max_diff = max(255 - int(sample_pixel), int(sample_pixel))
    return max_diff

def diff_func_color(sample_pixel, img_pixel):
    ''' 
    Compute pixels difference 
    
    Parameters
    ----------
    @sample_pixel <pixel>     A pixel of sample image
    @img_pixel    <pixel>     A pixel of image
    ----------
    Return <int>    Pixels difference 
    '''
    assert is_pixel(sample_pixel) and is_pixel(img_pixel)
    assert has_pixel_ch(sample_pixel) == has_pixel_ch(img_pixel)
    diff = 0.0
    if has_pixel_ch(sample_pixel):
        for c in range(len(sample_pixel)):
            diff += fabs(int(sample_pixel[c]) - int(img_pixel[c]))
    else:
        diff = fabs(int(sample_pixel) - int(img_pixel))
    return diff

def max_diff_func_edges(sample_pixel, img_pixel):
    ''' 
    Compute the maximum pixels difference 
    
    Parameters
    ----------
    @sample_pixel <pixel>     A pixel of sample image
    @img_pixel    <pixel>     A pixel of image
    ----------
    Return <int>    Maximum pixels difference 
    '''
    assert is_pixel(sample_pixel) and is_pixel(img_pixel)
    assert has_pixel_ch(sample_pixel) == has_pixel_ch(img_pixel)
    max_diff = 0
    if has_pixel_ch(sample_pixel):
        for c in range(len(sample_pixel)):
            max_diff += max(int(sample_pixel[c]), int(img_pixel[c]))
    else:
        max_diff = max(int(sample_pixel), int(img_pixel))
    return max_diff
