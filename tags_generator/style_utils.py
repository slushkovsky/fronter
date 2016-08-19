def iterate_styles(styles):
	'''
		Generates all values fot speciefed array of styles

		@styles - list of web styles
	'''

	if len(styles) == 0:
		yield [ ]
	else:
		tag = styles[0]
		for val in tag.get_values():
			for othet_styles in iterate_styles(styles[1:]):
				yield [ [ tag.name, val ] ] + othet_styles