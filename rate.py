import os

import argparse
import cv2

from rate_utils import img_pixel_comparise, img_edges_comparise \
                                          , compare_img_with_html


def existed_file_type(value):
    if not os.path.exists(value): 
        raise argparse.ArgumentError()
    return value

def arguments():
    parser = argparse.ArgumentParser(description ='This script allows' +
                            ' you to download scrinshot of web page')

    parser.add_argument('html_path', type = str
            , help = 'Enter path to html code of page to comparise.' +
                'It should be absolut path, like the url in browser')
    parser.add_argument('sample_path', type = existed_file_type
                             , help = 'Enter path to sample screenshot')

    return parser.parse_args()

if __name__ == '__main__':
    try:
        args = arguments()
        print('Pixel compare : %f' % compare_img_with_html(
                 args.sample_path, args.html_path, img_pixel_comparise))
        print('Edges compare : %f' % compare_img_with_html(
                 args.sample_path, args.html_path, img_edges_comparise))

    except KeyboardInterrupt:
        print('\nExiting')
