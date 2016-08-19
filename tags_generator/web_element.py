from default_styles import *

class WebElement(object):
	"""This class describes, which arguments iterate and how"""
	def __init__(self, name: str, content: str, *webtags):
		'''
			Creates new WebElement

			@name <str> - name of web element
			@content <str> - content of element (Can be None or string)
			@webtags <list> - css tags of element
		'''
		assert isinstance(name, str)
		assert isinstance(content, str) or content == None

		super(WebElement, self).__init__()

		self.name = name
		self.content = content
		self.webtags = webtags
		
color_element = WebElement(
		'body',
		None,
		opacity_tag,
		border_tag
	)
