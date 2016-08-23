from itertools import product

def iterate_styles(styles: list):
	'''
		Generates all values fot speciefed array of styles

		@styles <list> - list of web styles
	'''

	# Generates list for product

	pr = [ tag.get_values() for tag in styles ]
	l = len(pr)

	for p in product(*pr):
		yield [ [ styles[i].name, p[i] ] for i in range(l) ]
