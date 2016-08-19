from web_tag import *

class WebElement(object):
	"""This class describes, which arguments iterate and how"""
	def __init__(self, name, content, *webtags):
		super(WebElement, self).__init__()

		self.name = name
		self.content = content
		self.webtags = webtags
		
color = WebElement(
		'body',
		None,
		WebTag('opacity', TagType.float_int),
		WebTag('border', TagType.integer)
	)