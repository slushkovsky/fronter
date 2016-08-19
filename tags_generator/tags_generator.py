from tags_utils import iterate_tags
from web_element import color_element

from designed_element import DesignedElement

def generate_elements(webelement):
	element_src = ''

	if webelement.content:
		element_src = '<{0}>{1}</{0}>'
	else:
		element_src = '<{0}/>'

	element_src = element_src.format(webelement.name, webelement.content)

	for tags in iterate_tags(webelement.webtags):
		css_src = '{\n'
		for tag in tags:
			css_src += '\t{0}: {1};\n'.format(tag[0], tag[1])
		css_src += '}'

		yield DesignedElement(css_src, element_src)

if __name__ == '__main__':
	for css_src, elem_src in generate_elements(color_element):
		print(css_src, '\n' * 3, elem_src)