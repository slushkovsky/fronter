#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 16:54:53 2016

@author: chernov
"""

    
from argparse import ArgumentParser
from os import path

import cv2
import numpy as np
from skimage import feature

__DEBUG__ = False

def get_descriptors(img, dimensions=8, radius=8, bins=40):

    lbp = feature.local_binary_pattern(img, dimensions, radius)
    
    if __DEBUG__:
        lbp_bytes = lbp.astype(np.float)/lbp.max()
        lbp_bytes = (lbp_bytes * 255).astype(np.uint8)
        cv2.imshow("LBP Features", lbp_bytes)
    
    hist, bins = np.histogram(lbp.ravel(), bins)
    hist = hist/hist.max()
    
    return hist, bins
    

def parse_args():
    def file_arg(value): 
        if not path.exists(value):
            if not path.exists(value):
                raise Exception() 
        return value
        
    parser = ArgumentParser()
    parser.add_argument('image', type=file_arg,
                        help="Path to image with name")
    parser.add_argument('--debug', action='store_true',
                        help="Debug mod")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    
    if args.debug:
        __DEBUG__ = True
    
    img = cv2.imread(args.image, 0)
    hist, bins = get_descriptors(img)
    print(hist)
    
    if __DEBUG__:
        cv2.waitKey()
        cv2.destroyAllWindows()
