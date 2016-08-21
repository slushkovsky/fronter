#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 19:37:17 2016

@author: chernov
"""

import PIL.Image

import cv2
import numpy as np
from skimage.feature import local_binary_pattern

from ml.descriptors import img_descriptor
from ocr.tesseract import tess_run

@img_descriptor('SYMB_LBP')
def symb_lbp(img:        PIL.Image, 
        dimensions: int        = 8, 
        radius:     int        = 8, 
        bins:       int        = 40) -> (np.array, np.array):
    '''
      Calculate lbp descriptors for symbol boxes 
    '''
    
    np_img = np.asarray(img)
    text, boxes = tess_run(np_img)
    
    if len(boxes) == 0:
        raise Exception("No symbols found on image")
    
    gray = img.convert('L')    
    lbp = local_binary_pattern(gray, dimensions, radius)
    
    np_gray = np.asarray(lbp)
    symb_lbps = np.array(())
    for box in boxes:
        x1 = min(box[1][0], box[2][0])
        x2 = max(box[1][0], box[2][0])
        y1 = min(box[1][1], box[2][1])
        y2 = max(box[1][1], box[2][1])
        symb_lbps = np.append(symb_lbps, np_gray[y1:y2, x1:x2].ravel())
    
    hist, bins = np.histogram(symb_lbps, bins)
    hist = hist/hist.max() 
    
    return hist, bins