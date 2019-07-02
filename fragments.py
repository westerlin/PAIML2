import random
import re

class Fragment:

	def __init__(self, faces=[], conditions=[]):
		self.faces = faces #Alternatively Editions
		self.conditions = conditions

	def active(self,worldstate):
		





class FragmentManager:

	def __init__(self,fragments={}, worldstate=None):
		self.fragments = fragments
		self.ws = worldstate

	def evaluateFragment(fragmentkey):
		fragment = self.fragments.get(fragmentkey)
		if fragment != None:
			if self.__fragmentConditionOK(fragment):
				return self.__getFragmentFace()
		return ""





