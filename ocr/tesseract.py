#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 16:03:44 2016

@author: chernov
"""

import sys
import csv
import json
import codecs
import time
from os import system, path, remove
from argparse import ArgumentParser

import cv2
import numpy as np

main_dir = path.dirname(path.dirname(__file__))
if not main_dir in sys.path: sys.path.append(main_dir)

from utils import args_types   
    
def resize_img(img, min_h=100) -> (np.ndarray, float):
    if min_h == -1 or img.shape[0] > min_h:
        return img, 1
    else:
        scale = min_h / img.shape[0]
        new_size = tuple((np.array(img.shape[0:2][::-1])*scale).astype(np.int))
        return cv2.resize(img, new_size), scale
    
    
def tess_run(img, temp_file="/tmp/tess_temp", image_min_h=400):
    temp_unique_stamp = hex(int(time.time()*10**7))[2:]
    temp_file += temp_unique_stamp
    img_path = temp_file + ".png"
    
    img, scale = resize_img(img, min_h=image_min_h)
    cv2.imwrite(img_path, img)
    
    system('tesseract "%s" %s '  
           '-c tessedit_create_boxfile=1 '
           '-c tessedit_create_txt=1'%(img_path, temp_file))
    
    text_file =temp_file + ".txt"
    text = open(text_file).read()
    remove(text_file)
    
    boxes = None
    box_file = temp_file + ".box"
    with open(box_file) as csvfile:
        boxreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        boxes = [[row[0], (int(float(row[1])/scale),
                           int((img.shape[0] - float(row[2]))/scale)),
                          (int(float(row[3])/scale),
                           int((img.shape[0] - float(row[4]))/scale))]
                 for row in boxreader]
    remove(box_file)
    return text, boxes
    
    
def parse_args():
    parser = ArgumentParser()

    parser.add_argument('image',
                        type=args_types.existed_file,
                        help='Image path')
    parser.add_argument('--tempfile', default="/tmp/tess_temp",
                        help='Temporary file path')
    parser.add_argument('--min_h', default=400,
                        help='Minimal imahe height for internal '
                        'ocr processing. -1 for disable resize '
                        '(default - 400)')
    return parser.parse_args()
    
    
if __name__ == "__main__":
    args = parse_args()
    
    image = args.image
    
    image_dir = path.abspath(path.dirname(args.image))
    img = cv2.imread(args.image, cv2.IMREAD_UNCHANGED)
    text, boxes = tess_run(img, args.tempfile, args.min_h)
    print(text)
    
    img = cv2.imread(image, cv2.IMREAD_UNCHANGED)
    img, scale = resize_img(img, min_h=args.min_h)
    for box in boxes:
        pt1 = tuple((np.array(box[1])*scale).astype(np.int))
        pt2 = tuple((np.array(box[2])*scale).astype(np.int))
        cv2.rectangle(img, pt1, pt2, (0,0,255, 255))

    img_out = "test.png"
    cv2.imwrite(img_out, img)
    system("xdg-open %s"%(img_out))
    