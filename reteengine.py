

class ReteToken:

		def __init__(self,path):
		self.path = path
		self.branches = self.__split(path)
		self.params = {}

		