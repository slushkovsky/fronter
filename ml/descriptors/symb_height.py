#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 18:40:31 2016

@author: chernov
"""

import PIL.Image

import numpy as np

from ml.descriptors import img_descriptor
from ocr.tesseract import tess_run

@img_descriptor('SYMB_HEIGHT')
def symb_height(img:        PIL.Image,
        bins:       int        = 10) -> (np.array, np.array):
    '''
      Calculate symbols height histogramms  
    '''
    
    np_img = np.asarray(img)
    text, boxes = tess_run(np_img)
    
    if len(boxes) == 0:
        raise Exception("No symbols found on image")
    
    heights = np.array([abs(box[1][1] - box[2][1]) for box in boxes])
    
    hist, bins = np.histogram(heights.ravel(), bins)
    hist = hist / hist.max()    
    
    return hist, bins