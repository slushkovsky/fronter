import os
import sys
from argparse import ArgumentParser

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(CURRENT_DIR, '..'))

import utils


def parse_args(): 
	parser = ArgumentParser(description='Tool for save webpage screenshot')

	parser.add_argument('url',   help='URL of webpage to be parsed')
	parser.add_argument('--out', help='Path to save screenshot. If not specified - it will the be random unexisted file in current working directory')

	return parser.parse_args()


if __name__ == '__main__': 
	args = parse_args()
	warn_on_overwrite = True

	if args.out is not None: 
		if os.path.exists(args.out): 
			question = 'File {!r} always exists - overwrite?'.format(args.out)
			confirmed = utils.shell.ask_yes_no(question=question, default=True)

			if confirmed: 
				warn_on_overwrite = False
			else: 
				sys.exit()

	else: 
		args.out = utils.files.unexisted_file(os.getcwd(), '.png')


	utils.browser.site_screenshot(url=args.url).save(args.out)