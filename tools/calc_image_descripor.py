import os
import sys
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

	parser.set_defaults(descr='LBP')

	return parser.parse_args()

if __name__  == '__main__':
	args = parse_args()

	img = Image.open(args.image)
	descr = image_descriptors[args.descr](img)

	print(descr)

