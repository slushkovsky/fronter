from enum import Enum

class CSSParamType(Enum):
	'''
		Enum for css tags types
	'''
	unknown = 0

	integer = 1
	procent = 2
	float_int = 3
	integer_px = 4

	color = 5

	decoration = 6
	font_style = 7
	font_family = 8

	complex_tag = 100


class CSSParam(object):
	"""This class describes some tag for web element"""
	def __init__(self, name, tag_type, values=None):
		'''
			Creates new CSSParam object

			@name - name of tag
			@tag_type - name of tag_type
			@values - values that can be for such tag (If None will use default for tag_type)
		'''

		assert isinstance(name, str)
		assert isinstance(tag_type, CSSParamType)

		super(CSSParam, self).__init__()
		self.name = name
		self.tag_type = tag_type

		if values == None:
			values = CSSParam.get_standart_values(tag_type)

		self.values = values

	def get_values(self):
		'''
			Generator that returns all values of tag
		'''
		for v in self.values:
			yield v

	@staticmethod
	def get_standart_values(tag_type):
		'''
			Gets default values for specified tag

			@tag_type - Type of tag
		'''

		assert isinstance(tag_type, CSSParamType)

		# TODO: Convert all to generators i think
		if tag_type == CSSParamType.integer or tag_type == CSSParamType.integer_px:
			return list(range(72))
		elif tag_type == CSSParamType.procent:
			return list(range(1, 100))
		elif tag_type == CSSParamType.float_int:
			return [ 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1 ]
		elif tag_type == CSSParamType.color:
			return [ 'black', 'red', 'green', 'white' ]
		elif tag_type == CSSParamType.decoration:
			return [ 'none', 'underline', 'line-through' ]
		elif tag_type == CSSParamType.font_style:
			return [ 'normal', 'italic' ]
		elif tag_type == CSSParamType.font_family:
			return [ "'Times New Roman', Times, serif" ]
		elif tag_type == CSSParamType.complex_tag:
			return None
		else:
			return None

color_tag = CSSParam('color', CSSParamType.color)

opacity_tag = CSSParam('opacity', CSSParamType.float_int)
border_style_tag = CSSParam('border-style', CSSParamType.unknown, 
	[ 'none', 'hidden', 'dotted', 'dashed', 'solid', 'double', 'groove', 'ridge', 'inset', 'outset' ]
)
