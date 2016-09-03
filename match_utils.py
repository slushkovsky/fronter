import os
from math import sqrt

import cv2
import numpy as np

from assert_utils import is_image, is_tuple, has_pixel_ch

EXCESS_ELEMENTS_COLOR = np.array([0, 0, 255])
DEFICIT_ELEMENTS_COLOR = np.array([0, 255, 0])
SHIFTED_ELEMENTS_COLOR = (53, 167, 255)

MAX_DETECT_RADIUS = 100 #pixels
MIN_DETECT_RADIUS = 5 #pixels

DEFAULT_TRESHOLDS = (75, 75)

def mismatch_edges(sample, image):
    '''
    This is the function that aims to find elements, which are in sample, 
    but aren't in image

    Parameters
    ----------
    @sample  <cv2.image>  Binary image of edges
    @image   <cv2.image>  Binary image of edges 
    ----------
    Return   <cv2.image>  Binary image of mismatched elements
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

def mismatch_edges_images(sample, image, tresholds=DEFAULT_TRESHOLDS):
    '''
    This is the function that aims to find elements, which are in
    sample, but aren't in image

    Parameters
    ----------
    @sample  <cv2.image>  Sample
    @image   <cv2.image>  Image
    ----------
    Return   <cv2.image>  Binary image of mismatched elements
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
    @mask    <cv2.image>  Binary image
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

def cv_match(img1, img2, good_match=0.5, neiberhoods=2):
    '''
    Detect matching between two images.

    Parameters
    ----------
    @img1        <cv2.image>  First image
    @img2        <cv2.image>  Second image
    @good_match  <float>      Determines what matchings are good
    ----------
    Return       <list[cv2.KeyPoint], list[cv2.KeyPoint]
                                                    , list[cv2.DMatch]> 
                 Lists of key points of the first image, key point of 
                 the second image and the matching list. 
    '''
    assert is_image(img1) and is_image(img2)
    assert isinstance(good_match, float)
    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    # BFMatcher with default params
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2, k=neiberhoods)

    # Apply ratio test
    good = []
    for m, n in matches:
        if m.distance < good_match * n.distance:
            good.append(m)
    return kp1, kp2, good


def shift_detector(img1, img2, max_radius=MAX_DETECT_RADIUS
                              , min_radius=MIN_DETECT_RADIUS):
    '''
    Detect matching between two images and choose only shifted.

    Parameters
    ----------
    @img1        <cv2.image>  First image
    @img2        <cv2.image>  Second image
    @max_radius  <int>        Matching with a larger radius are ignored
    @min_radius  <int>        Matching with a smaller radius are ignored
    ----------
    Return       <list[tuple(tuple(int, int), tuple(int, int))]>       
                                    List of tuple of matching points. 
    '''
    assert is_image(img1) and is_image(img2)
    assert isinstance(max_radius, int) and isinstance(min_radius, int)

    kp1, kp2, match = cv_match(img1, img2)
    
    #delete matching elements, which has the same coordinates
    shifted = []
    for m in match:
        point1, point2 = kp1[m.queryIdx], kp2[m.trainIdx]   #in doubt
        x1, y1 = point1.pt 
        x2, y2 = point2.pt
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        dist = sqrt((x1 - x2)**2 + (y1 - y2)**2)
        if dist >= min_radius and dist <= max_radius:
            shifted.append(((x1, y1), (x2, y2)))

    return shifted

def mismatch_mask(sample, image, tresholds=DEFAULT_TRESHOLDS):
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

    excess = mismatch_edges_images(image, sample, tresholds)
    deficit = mismatch_edges_images(sample, image, tresholds)
    sample_edge = cv2.Canny(sample, tresholds[0], tresholds[1])
    image_edge = cv2.Canny(image, tresholds[0], tresholds[1])
    shift = shift_detector(sample_edge, image_edge)

    out = apply_mask(image, excess, EXCESS_ELEMENTS_COLOR)
    out = apply_mask(out, deficit, DEFICIT_ELEMENTS_COLOR)
    for p1, p2 in shift:
        cv2.line(out, p1, p2, SHIFTED_ELEMENTS_COLOR)
    return out
