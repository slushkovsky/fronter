import PIL
import numpy as np
from functools import wraps

image_descriptors = {}

def img_descriptor(name: str): 
	'''
	  Decorator
	'''

	assert isinstance(name, str)

	def decorator(f): 
		@wraps(f)
		def wrapper(img, **kw):
			assert PIL.Image.isImageType(img)

			return f(img, **kw)

		image_descriptors[name] = wrapper

		# exec('global {name}; {name} = wrapper'.format(name=name))

		return wrapper
	return decorator

from . import lbp
from . import symb_height
from . import symb_lbp