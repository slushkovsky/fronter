from style_utils import iterate_styles

from css_param import *

class MultiCSSParam(CSSParam):
	"""CSSParam that has multiply tags inside (border as example)"""
	def __init__(self, name, *css_params):
		'''
			Creates new MultiCSSParam

			@name - Name of the tag
			@css_params - Tags of the tag
		'''
		super(MultiCSSParam, self).__init__(name, CSSParamType.complex_tag)

		self.css_params = css_params

	def get_values(self):
		'''
			Generator that returns all values of tag
		'''
		for tags in iterate_styles(self.css_params):
			yield ' '.join(str(t[1]) for t in tags)

shadow_tag = MultiCSSParam(
	'box-shadow',
	CSSParam('x', CSSParamType.integer),
	CSSParam('y', CSSParamType.integer),
	CSSParam('radius', CSSParamType.integer_px),
	CSSParam('stretching', CSSParamType.integer),
	color_tag
)
border_tag = MultiCSSParam(
	'border',
	CSSParam('border-width', CSSParamType.integer_px),
	border_style_tag,
	color_tag
)