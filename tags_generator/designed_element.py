class DesignedElement(object):
	"""Stores css and element code for some designed element"""
	def __init__(self, css_src, element_src):
		'''
			Creates new DesignedElement

			@css_src - css string of document
			@element_src - source of html element
		'''

		assert isinstance(css_src, str)
		assert isinstance(element_src, str)
		
		self.css_src = css_src
		self.element_src = element_src
		