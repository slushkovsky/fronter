import utils.version_check

import sys
import warnings

from psd_tools import PSDImage
from psd_tools.user_api import psd_image
from psd_tools.exceptions import Error as psd_error

from utils import exc

def psd_to_images(filename, merge_group=True) :
    '''
    parses .psd file

    @param  filename        <str>   is a file directory + file name
    @param  merge_group     <bool>  when True all images merge in group

    @return list of PIL.images

    '''

    assert (isinstance(filename, str)), "File name isn't string"

    if (not filename.endswith(".psd")) :
        warnings.warn("Wrong file extention")

    try :
        psd = PSDImage.load(filename)

    except FileNotFoundError :
        raise 

    except psd_error :
        raise
    
    images = []

    for layers in psd.layers :

        if (isinstance(layers, psd_image.Layer) or merge_group) :
            yield layers.as_PIL()

        else :
            for layer in layers.layers :
                  yield layer.as_PIL()