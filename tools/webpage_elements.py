import os
import sys
from argparse import ArgumentParser
from geomtypes import Size

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_ROOT = os.path.join(SCRIPT_DIR, '..')

sys.path.append(PROJECT_ROOT)

from utils import args_types
from utils.files import unexisted_file
from utils.browser import site_tags_images


def parse_args():
	parser = ArgumentParser(description='Tool for take a screenshots of the all site HTML tags')

	parser.add_argument('url',        type=str,                     help='Site URL')
	parser.add_argument('--save-to',  type=args_types.existed_dir,  help='Dir to store images (default is current working directory')
	parser.add_argument('--h-offset', type=float,                   help='Screenshot area vertical offset (related to an element height: 0.0 - inital area)')
	parser.add_argument('--w-offset', type=float,                   help='Screenshot area horizontal offset (related to an element width: 0.0 - inital area)')
	parser.add_argument('--min-size', type=args_types.size,         help='Tag min size')
	parser.add_argument('--max-size', type=args_types.size,         help='Tag max size')

	parser.set_defaults(save_to =os.getcwd(), 
		                h_offset=0.0, 
		                w_offset=0.0, 
		                min_size=Size(15, 15), 
		                max_size=Size.ever_biggest())

	return parser.parse_args()


if __name__ == '__main__':
	args = parse_args()

	tags = site_tags_images(url     =args.url, 
		                    h_offset=args.h_offset, 
		                    w_offset=args.w_offset,
		                    min_size=args.min_size,
		                    max_size=args.max_size)

	for tag in tags: 
		prefix = tag.name + '_' + tag.classes + '_'

		path = unexisted_file(args.save_to, '.png', prefix=prefix)
		tag.img.save(path)

