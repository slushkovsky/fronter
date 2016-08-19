from tags_utils import iterate_tags

from web_tag import *

class MultiWebTag(WebTag):
	"""WebTag that has multiply tags inside (border as example)"""
	def __init__(self, name, *web_tags):
		'''
			Creates new MultiwebTag

			@name - Name of the tag
			@web_tags - Tags of the tag
		'''
		super(MultiWebTag, self).__init__(name, TagType.complex_tag)

		self.web_tags = web_tags

	def get_values(self):
		'''
			Generator that returns all values of tag
		'''
		for tags in iterate_tags(self.web_tags):
			yield ' '.join(str(t[1]) for t in tags)

shadow_tag = MultiWebTag(
	'box-shadow',
	WebTag('x', TagType.integer),
	WebTag('y', TagType.integer),
	WebTag('radius', TagType.integer_px),
	WebTag('stretching', TagType.integer),
	color_tag
)
border_tag = MultiWebTag(
	'border',
	WebTag('border-width', TagType.integer_px),
	border_style_tag,
	color_tag
)