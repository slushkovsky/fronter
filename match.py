import argparse
import os

import cv2

from match_utils import mismatch_mask
from function_wrappers import img_path


WAITING_TIME = 100000 #miliseconds

def existed_file_type(value):
    if not os.path.exists(value): 
        raise argparse.ArgumentError()
    return value

def arguments():
    parser = argparse.ArgumentParser(description ='This script allows' +
                            ' you to match two images')

    parser.add_argument('path1', type = existed_file_type
            , help = 'Enter path to the first image')
    parser.add_argument('path2', type = existed_file_type
                             , help = 'Enter path to the second image')

    return parser.parse_args()
    
if __name__ == '__main__':
    try:
        args = arguments()
        cv2.imshow('Match', img_path(args.path1, args.path2
                                               , mismatch_mask))
        cv2.waitKey(WAITING_TIME)
        
    except KeyboardInterrupt:
        print('\nExiting')
