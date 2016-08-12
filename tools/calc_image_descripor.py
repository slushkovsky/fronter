import os
import sys
import csv
from PIL import Image
from argparse import ArgumentParser

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_ROOT = os.path.join(SCRIPT_DIR, '..')

sys.path.append(PROJECT_ROOT)

from utils import args_types
from ml.descriptors import image_descriptors


def parse_args():
    parser = ArgumentParser('Tool for calculate image descriptor')

    parser.add_argument('image',   type=args_types.existed_file,       help='Image')
    parser.add_argument('--descr', choices=image_descriptors.keys(),  help='Descriptor (default: LBP)')
    parser.add_argument('--csv_path', type=str, help='Output csv path')

    parser.set_defaults(descr='LBP')

    return parser.parse_args()

if __name__  == '__main__':
    args = parse_args()

    img = Image.open(args.image)
    descr = image_descriptors[args.descr](img)
 
    if args.csv_path:
        with open(args.csv_path, "a") as csv_file:
            writer = csv.writer(csv_file)
            data = [args.image]
            data += list(descr[0])
            writer.writerow(data)
    else: 
        print(descr)

