def iterate_tags(tags):
	if len(tags) == 0:
		yield [ ]
	else:
		tag = tags[0]
		for val in tag.get_values():
			for othet_tags in iterate_tags(tags[1:]):
				yield [ [ tag.name, val ] ] + othet_tags