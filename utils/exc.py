class DirNotEixstsError(Exception): 
	
	def __init__(self, dir): 
		self.dir = dir

	def __str__(self): 
		return 'Directory {!r} not exists'.format(self.dir)