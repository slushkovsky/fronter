from css_param import *
from multi_css_param import *

class WebElement(object):
	"""This class describes, which arguments iterate and how"""
	def __init__(self, name, content, *webtags):
		'''
			Creates new WebElement

			@name - name of web element
			@content - content of element (Can be None or string)
			@webtags - css tags of element
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
