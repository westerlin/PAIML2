import re


class Node:

	def __init__(self,name="root",parent=None):
		self.children={}
		self.name=name
		self.parent=parent

	def __str__(self):
		return self.name

	def combi(self,keystring,prescenes=None):
		outscenes = []
		scene = {}
		if prescenes == None : prescenes = [{}]
		for scene in prescenes:
			keyparm = keystring
			for key,value in scene.items():
				keyparm = keystring.replace("["+key+"]",value)
			#keys = keyparm.split(".")
			pattern = r'([\.|\!]?)([\[|\{|\()]?\w+[\]|\}|\)]?)'
			keys = re.findall(pattern,keystring)
			scenes = []
			flag,newscenes = self.__xcombi(keys,scenes,scene)
			outscenes += newscenes
			#print(keys,newscenes,flag)
		return outscenes

	def __xcombi(self,keys,scenes,scene=None):
		flag = True
		key = keys[0][1]
		tag = keys[0][0]
		regex = r'\[(.+)\]'
		match = re.match(regex,key,flags=re.IGNORECASE)
		#print(key)
		if match:
			## IF THERE ARE PARAMETERS TO HARVEST
			parm = match.groups()[0]
			if tag == "!" and len(self.children) > 1 : return False,scenes
			for (childname,child) in self.children.items():
				scene[parm]=childname				
				#print(scene,scenes)
				if len(keys)>1:
					flag,scenes = child.__xcombi(keys[1:],scenes,scene)
				else:
					if flag : scenes.append(dict(scene))
		else:
			## IF PLAIN NODE - TRUE OR FALSE
			child = self.children.get(key)
			#print("\t",key,"??",flag, keys)
			if child != None:
				if tag == "!" and len(self.children) > 1 : return False,scenes
				if len(keys)>1:
					flag, scenes = child.__xcombi(keys[1:],scenes,scene)
				else:
					if flag : scenes.append(dict(scene))
			else:
				#print("FALSIFY:",key,child,list(self.children.keys()))
				return False,scenes
		return flag,scenes

	def output(self):
		level = 0
		self.__output(level)

	def __output(self,level):
		print("   "*level,self.name)
		level += 1
		for (key,child) in self.children.items():
			child.__output(level)

	def remove(self,keystring):
		removed = self.get(keystring)
		if removed == None : return 
		for childlabel in removed.children.keys():
			child = removed.children.get(childlabel)
			child.remove(childlabel)
		removed.children = {}	
		removed = None

	def add(self,keystring):
		pattern = r'([\.|\!]?)([\[|\{|\()]?[\w|\+|\-]+[\]|\}|\)]?)'
		keys = re.findall(pattern,keystring)
		#keys = keystring.split(".")
		#print("ADDING: ", keystring)
		return self.__add(keys)

	def __add(self,keys):
		key = keys[0][1]
		tag = keys[0][0]
		child = self.children.get(key)
		if child == None:
			child = Node(key,self)
			self.children[key] = child
		if tag == "!":
			self.children = {key:child}
		if len(keys)>1:
			return child.__add(keys[1:])
		return child

	def get(self,keystring):
		pattern = r'([\.|\!]?)([\[|\{|\()]?\w+[\]|\}|\)]?)'
		keys = re.findall(pattern,keystring)
		#keys = keystring.split(".")
		return self.__get(keys)

	def __get(self,keys):
		key = keys[0][1]
		tag = keys[0][0]
		child = self.children.get(key)
		if child != None:
			if tag == "!" and len(self.children) > 1 : return None
			if len(keys)>1:
				return child.__get(keys[1:])
			else:
				return child
		return None

