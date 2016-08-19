from web_tag import *
from multi_web_tag import *

class WebElement(object):
	"""This class describes, which arguments iterate and how"""
	def __init__(self, name, content, *webtags):
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
