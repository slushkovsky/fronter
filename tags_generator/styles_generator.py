from style_utils import iterate_styles

from web_element import WebElement
from web_element import color_element

from designed_element import DesignedElement

def generate_elements(webelement):
	'''
		Generates designed elements from webelement template

		@webelement - Template of web element
	'''

	assert isinstance(webelement, WebElement)

	element_src = ''

	if webelement.content:
		element_src = '<{0}>{1}</{0}>'
	else:
		element_src = '<{0}/>'

	element_src = element_src.format(webelement.name, webelement.content)

	for tags in iterate_styles(webelement.webtags):
		css_src = '{\n'
		for tag in tags:
			css_src += '\t{0}: {1};\n'.format(tag[0], tag[1])
		css_src += '}'

		yield DesignedElement(css_src, element_src)

if __name__ == '__main__':
	for element in generate_elements(color_element):
		pass