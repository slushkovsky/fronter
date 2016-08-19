from web_element import color

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

		yield css_src, element_src


def iterate_tags(tags):
	if len(tags) == 0:
		yield [ ]
	else:
		tag = tags[0]
		for val in tag.get_values():
			for othet_tags in iterate_tags(tags[1:]):
				yield [ [ tag.name, val ] ] + othet_tags

if __name__ == '__main__':
	for css_src, elem_src in generate_elements(color):
		print(css_src, '\n' * 3, elem_src)