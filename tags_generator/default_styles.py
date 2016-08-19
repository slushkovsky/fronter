from css_param import CSSParam
from css_param import CSSParamType
from multi_css_param import MultiCSSParam

color_tag = CSSParam('color', CSSParamType.color)

opacity_tag = CSSParam('opacity', CSSParamType.float_int)
border_style_tag = CSSParam('border-style', CSSParamType.unknown, 
	[ 'none', 'hidden', 'dotted', 'dashed', 'solid', 'double', 'groove', 'ridge', 'inset', 'outset' ]
)

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