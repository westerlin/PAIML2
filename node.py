import re
import random

cards_ranking = ["One","Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten","Jack","Queen","King","Ace"]

pronouns = [
			"pronouns.male.subject!he",
			"pronouns.female.subject!she",
			"pronouns.male.object!him",
			"pronouns.female.object!her",
			"pronouns.male.adjective!his",
			"pronouns.female.adjective!her",
			"pronouns.male.possesive!his",
			"pronouns.female.possesive!hers",
			"pronouns.male.reflexive!himself",
			"pronouns.female.reflexive!herself"
			]


def cap(match):
    return(match.group().capitalize())

def Capitalize(text):
	p = re.compile(r'(?<=[\.\?!]\s)(\w+)')
	p2 = re.compile(r'^\w+')
	return p2.sub(cap,p.sub(cap, text))


def isUniquePath(path):
		pattern = r'^([\.|\!|\?|\^]?\w+)+$'
		return re.match(pattern,path)

def isVarPath(path):
		pattern = r'^([\.|\!|\?|\^]?[\[|\{|\()]?\w+[\]|\}|\)]?)+$'
		return re.match(pattern,path)

def createRanking(prefix,ranking):
	output = []
	for rank1 in range(len(ranking)):
		for rank2 in range(len(ranking)):
			if rank1 < rank2:
				output.append(prefix+ranking[rank1]+".less."+ranking[rank2])
			if rank1 == rank2:
				output.append(prefix+ranking[rank1]+".equal."+ranking[rank2])
			if rank1 <= rank2:
				output.append(prefix+ranking[rank1]+".less_or_equal."+ranking[rank2])
	return output

def createCycle(prefix,elements):
	output = []
	for idx in range(len(elements)):
		if idx > 0:
			output.append(prefix+elements[idx-1]+".next."+elements[idx])
	output.append(prefix+"."+elements[len(elements)-1]+".next."+elements[0])
	return output

def createList(prefix,elements):
	output = []
	for element in elements:
		output.append(prefix+element)
	return output

def createDifference(prefix,elements):
	output = []
	for element in elements:
		for other in elements:
			if element != other:
				output.append(prefix+element+"."+other)
	return output

def populate(path,parms):
	adjusted = ""
	while path != adjusted:
		adjusted = path
		for key,item in parms.items():
			adjusted = path
			path = adjusted.replace("["+key+"]",item)
	return path


class Node:

	def __init__(self,name="root",parent=None):
		self.children={}
		self.name=name
		self.parent=parent

	def __str__(self):
		return self.name

	def __repr__(self):
		return str(self)

	def __addChild(self,child,key,tag):
		child = Node(key,self)
		self.children[key] = child
		if tag == "!":
			self.children = {key:child}
		return child

	def match(self,initpath):
		node = self.get(initpath)
		if node != None:
			paths = []
			for key,child in node.children.items():
				paths += child.__match()
			return [initpath+"."+path for path in paths]
		return []

	def __match(self):
		output = [self.name]
		for key,child in self.children.items():
			branches = child.__match()
			for branch in branches:
				output.append(self.name+"."+branch)
		return output 

	def combi(self,keystring,prescenes=None):
		outscenes = []
		scene = {}
		if prescenes == None : prescenes = [{}]
		for scene in prescenes:
			keyparm = keystring
			#print("before:",keyparm)
			#for key,value in scene.items():
				#keyparm = keystring.replace("["+key+"]",value)
			keyparm = populate(keystring,scene)
				#print(value,keyparm)
			#print("after:",keyparm)
			#keys = keyparm.split(".")
			pattern = r'([\.|\!|\?|\^]?)([\[|\{|\()]?\w+[\]|\}|\)]?)'
			keys = re.findall(pattern,keyparm)
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
			if tag == "?":
				if len(self.children) == 0: return False,scenes
				childname = random.choice(list(self.children.keys()))
				child = self.children[childname]
				scene[parm]=childname
				if len(keys)>1:
					flag,scenes = child.__xcombi(keys[1:],scenes,scene)
				else:
					if flag : scenes.append(dict(scene))
			else:
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

	def delete(self,keystring):
		pattern = r'([\.|\!]?)([\[|\{|\()]?[\w|\+|\-]+[\]|\}|\)]?)'
		keys = re.findall(pattern,keystring)
		self.__delete(keys)

	def __delete(self,keys):
		key = keys[0][1]
		tag = keys[0][0]
		child = self.children.get(key)
		if child != None:
			if len(keys)>1:
				if child.__delete(keys[1:]):
					if len(child.children.keys())<1:
						self.children.pop(key)
						return True
					return False
				return False
			else:
				self.children.pop(key)
				return True
		return False


	def addList(self,branches):
		for branch in branches:
			self.add(branch)

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
			child = self.__addChild(child,key,tag)
		if len(keys)>1:
			return child.__add(keys[1:])
		return child

	def get(self,keystring):
		pattern = r'([\.|\!|\^]?)([\[|\{|\()]?[\w|\*]+[\]|\}|\)]?)'
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
				if keys[1][1] == "*" and len(keys)==2: 
					return [childs for key,childs in child.children.items()]
				return child.__get(keys[1:])
			else:
				return child
		return None

