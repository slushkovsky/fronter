import version_check
from psd_tools import PSDImage
from psd_tools.user_api import psd_image
import sys
import warnings

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

    psd = PSDImage.load(filename)
    images = []

    for layers in psd.layers :

        if (isinstance(layers, psd_image.Layer) or merge_group) :
            images.append(layers.as_PIL())

        else :
            for layer in layers.layers :
                images.append(layer.as_PIL())                

    yield images