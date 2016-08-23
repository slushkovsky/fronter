class DesignedElement(object):
	'''Stores css and element code for some designed'''
	def __init__(self, css_src: str, element_src: str):
		'''
			Creates new DesignedElement

			@css_src <str> - css string of document
			@element_src <str> - source of html element
		'''

		assert isinstance(css_src, str)
		assert isinstance(element_src, str)
		
		self.css_src = css_src
		self.element_src = element_src
		