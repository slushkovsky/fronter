from enum import Enum

class CSSParamType(Enum):
	'''
		Enum for css tags types
	'''
	unknown = 0

	integer = 1
	percent = 2
	float_int = 3
	integer_px = 4

	color = 5

	decoration = 6
	font_style = 7
	font_family = 8

	complex_tag = 100


class CSSParam(object):
	'''This class describes some tag for web element'''
	def __init__(self, name: str, css_type: CSSParamType, values=None):
		'''
			Creates new CSSParam object

			@name <str> - name of tag
			@css_type <CSSParamType> - name of css_type
			@values <iterable or None> - values that can be for such tag
		'''

		assert isinstance(name, str)
		assert isinstance(css_type, CSSParamType)

		super().__init__()
		self.name = name
		self.css_type = css_type

		if values is None:
			values = CSSParam.get_standart_values(css_type)
		else:
			isinstance(values, list)

		self.values = values

	def get_values(self):
		'''
			Generator that returns all values of tag
		'''
		for v in self.values:
			yield v

	@staticmethod
	def get_standart_values(css_type: CSSParamType):
		'''
			Gets default values for specified tag

			@css_type <CSSParamType> - Type of tag
		'''

		assert isinstance(css_type, CSSParamType)

		# TODO: Convert all to generators i think
		if css_type == CSSParamType.integer or css_type == CSSParamType.integer_px:
			return list(range(72))
		elif css_type == CSSParamType.percent:
			return list(range(1, 100))
		elif css_type == CSSParamType.float_int:
			return [ 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1 ]
		elif css_type == CSSParamType.color:
			return [ 'black', 'red', 'green', 'white' ]
		elif css_type == CSSParamType.decoration:
			return [ 'none', 'underline', 'line-through' ]
		elif css_type == CSSParamType.font_style:
			return [ 'normal', 'italic' ]
		elif css_type == CSSParamType.font_family:
			return [ "'Times New Roman', Times, serif" ]
		elif css_type == CSSParamType.complex_tag:
			return None
		else:
			return None
