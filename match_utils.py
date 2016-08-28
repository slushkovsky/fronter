import os

import cv2
import numpy as np

from assert_utils import is_image, is_tuple, has_pixel_ch


EXCESS_ELEMENTS_COLOR = np.array([0, 0, 255])
DEFICIT_ELEMENTS_COLOR = np.array([0, 255, 0])

def mismatch_edges(sample, image):
    '''
    This is the function that aims to find elements, which are in sample, 
    but aren't in image

    Parameters
    ----------
    @sample  <cv2.image>  One-chanel image of edges
    @image   <cv2.image>  One-chanel image of edges 
    ----------
    Return   <cv2.image>  One-chanel image of mismatched elements
    '''
    assert is_image(sample) and is_image(image)
    s_h, s_w = sample.shape[0], sample.shape[1]
    i_h, i_w = image.shape[0], image.shape[1]
    assert s_h == i_h and s_w == i_w
    assert len(sample.shape) == 2 and len(image.shape) == 2
    
    for x in range(s_h):
        for y in range(s_w):
            sample[x][y] = max(0, int(sample[x][y]) - int(image[x][y]))
    return sample

def mismatch_edges_images(sample, image, tresholds=(150, 150)):
    '''
    This is the function that aims to find elements, which are in
    sample, but aren't in image

    Parameters
    ----------
    @sample  <cv2.image>  Sample
    @image   <cv2.image>  Image
    ----------
    Return   <cv2.image>  One-chanel image of mismatched elements
    '''
    assert is_image(sample) and is_image(image)
    assert is_tuple(tresholds, 2, int)
    
    h, w = sample.shape[0], sample.shape[1]
    image = cv2.resize(image, (w, h))
    treshold1, treshold2 = tresholds
    image_edges = cv2.Canny(image, treshold1, treshold2)
    sample_edges = cv2.Canny(sample, treshold1, treshold2)
    
    return mismatch_edges(sample_edges, image_edges)

def apply_mask(image, mask, color):
    '''
    This is the function that aims to color those pixels of image, which
    are white on the mask.  

    Parameters
    ----------
    @image   <cv2.image>  An image
    @mask    <cv2.image>  One-chanel image
    @color   <pixel>      Color
    ----------
    Return   <cv2.image>  Colorized image
    '''
    assert is_image(image) and is_image(mask)
    i_h, i_w = image.shape[0], image.shape[1]
    m_h, m_w = mask.shape[0], mask.shape[1]
    assert m_h == i_h and m_w == i_w
    assert len(mask.shape) == 2
    assert type(color) == type(image[0][0])
    
    for x in range(i_h):
        for y in range(i_w):
            if mask[x][y]:
                image[x][y] = color
    return image

def mismatch_mask(sample, image):
    '''
    This is the function that aims to find elements, which are in 
    sample, but aren't in image

    Parameters
    ----------
    @sample  <cv2.image>  Sample
    @image   <cv2.image>  Image
    ----------
    Return   <cv2.image>  Colorized image. 
                          Green - dificit elements
                          Red - excess elements
    
    '''
    assert is_image(sample) and is_image(image)
    excess = mismatch_edges_images(image, sample)
    deficit = mismatch_edges_images(sample, image)
    image = apply_mask(image, excess, EXCESS_ELEMENTS_COLOR)
    image = apply_mask(image, deficit, DEFICIT_ELEMENTS_COLOR)
    return image
