import os
import sys
from argparse import ArgumentParser

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

from utils.psd import psd_to_images

def args_pars() :
    parser = ArgumentParser(description='It takes .psd file and save all layers as images.')
    parser.add_argument('path', type=str,
                        help='path and name of .psd file')
    parser.add_argument('-d', metavar='destination', type=str, default='',
                        help='destionation of saving images')
    parser.add_argument('-w', action="store_false", default=True,
                        help='if is on all images in layer group save separately')
    parser.add_argument('-p', metavar='prefix', type=str, default='',
                        help='file prefix')

    args = parser.parse_args()

    return (args.path, args.w, args.d, args.p)



path, wrap, dest, prefix = args_pars()

if (not dest == '' and not dest.endswith('/')) :
    dest += '/'

if (not dest == '' and not os.path.exists(dest)) :
    os.makedirs(dest)

images = psd_to_images(path, wrap)

count = 0

for image in images :
    image.save(dest + prefix + str(count) + ".png", "PNG")
    count += 1