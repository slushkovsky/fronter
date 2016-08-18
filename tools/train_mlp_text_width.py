#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 19:29:33 2016

@author: chernov
"""

import sys
import csv
import json
import codecs
from os import path, listdir
from PIL import Image
from argparse import ArgumentParser

main_dir = path.dirname(path.dirname(__file__))
if not main_dir in sys.path: sys.path.append(main_dir)

from ml.train_utils import train_mlp_float
from utils import args_types
from ml.descriptors import image_descriptors

def parse_args():
    parser = ArgumentParser('Tool for calculate image descriptor')

    parser.add_argument('--raw_dataset',
                        type=args_types.existed_dir,
                        help='Raw dataset path')
    parser.add_argument('--csv', default="dataset.csv",
                        help='Output dataset file')
    parser.add_argument('--descr', choices=image_descriptors.keys(),
                        help='Descriptor (default: LBP)')
    parser.add_argument('--output', default="mlp_out.xml",
                        help='Trained MLP output path')
    parser.set_defaults(descr='LBP')

    return parser.parse_args()

if __name__  == '__main__':
    args = parse_args()
    
    if args.raw_dataset:
        with open(args.csv, "w") as csv_file:
            csv_rows = []
            for file in listdir(args.raw_dataset):
                img = None
                try:  
                    img = Image.open(path.join(args.raw_dataset, file))
                except OSError:
                    continue
                
                css_filename = path.splitext(path.basename(file))[0] + ".css.json"
                css_filepath = path.join(args.raw_dataset, css_filename)
                css = json.load(codecs.open(css_filepath, "r", "utf-8-sig"))
                
                font_size = float(css["fontSize"].replace("px", ""))
                
                class_ = font_size
                descr = image_descriptors[args.descr](img)[0]
                cur_row = [class_] + list(descr)
                csv_rows.append(cur_row)

            writer = csv.writer(csv_file)
            writer.writerows(csv_rows)
    
    train_mlp_float(args.csv, args.output)
    