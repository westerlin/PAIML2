import json
import xml.etree.ElementTree as ET
import rwutility as RW
import re
import random

def trim(text):
	lines = text.split("\n")
	output = ""
	for line in lines:
		line = line.strip()
		if line != "":
			output += line + " \n"
	return output

def exchange(text,dictionary):
	for category in dictionary.keys():
		member = random.choice(list(dictionary.get(category)))
		text = text.replace("["+category+"]",member)
	return text


class DramaParser:

	def __init__(self, drama=None):
		self.commands = {
			"text": self.__text,
			"count" :self.__count,
			"spawn" :self.__spawn,
			"add" : self.__addtag,
			"remove" : self.__removetag,
			"li": self.__li,
			"condition": self.__condition,
			"random": self.__random
		}
		self.drama = drama
		self.roles = {}

	def execute(self,node):
		for child in node:
			command = self.commands.get(child.tag)
			if command != None:
				command(child)

	def __random(self,node):
		while True:
			child = random.choice(node)
			command = self.commands.get(child.tag)
			if command != None:
				return command(child)

	def __addtag(self,node):
		if node.text != "": 
			self.drama.ws.add(self.__contextualize(node.text.strip()))
		for child in node:
			command = self.commands.get(child.tag)
			if command != None:
				result = command(child)
				if result != "":
					self.drama.ws.add(self.__contextualize(result.strip()))
		return ""

	def __removetag(self,node):
		if node.text != "": 
			self.drama.ws.remove(self.__contextualize(node.text.strip()))
		for child in node:
			command = self.commands.get(child.tag)
			if command != None:
				result = command(child)
				if result != "":
					self.drama.ws.remove(self.__contextualize(result.strip()))
		return ""

	def __condition(self,node):
		attrib = node.get("is")
		if attrib != None:
			exists = self.drama.ws.get(self.__contextualize(attrib))
			if exists != None:
				return self.__li(node)
			else:
				return ""
		attrib = node.get("not")
		if attrib != None:
			exists = self.drama.ws.get(self.__contextualize(attrib))
			if exists == None:
				return self.__li(node)
			else:
				return ""
		return self.__li(node)

	def __li(self,node):
		output = ""
		if node.text != None : output += node.text
		for child in node:
			command = self.commands.get(child.tag)
			if command != None:
				output += command(child)
		return output

	def __count(self,node):
		key = node.get("elements")
		if key != None:
			elements = drama.ws.get(key)
			if elements != None:
				return str(len(elements.children.keys()))
		return "none"

	def __text(self,node):
		response = ""
		if node.text != None: response += node.text
		for children in node:
			command =  self.commands.get(children.tag)
			if command != None:
				response += command(children)
			if children.tail != None: response += children.tail
		response = self.__contextualize(trim(response))
		if drama != None: drama.logs.append(response)
		return ""

	def __insertRoles(self,text):
		return exchange(text,self.roles)

	def __contextualize(self,text):
		#if self.context == None: return text
		text = self.__insertRoles(text)
		regex = r"\[(.*?)\]"
		regex = r"\[actors\.(\w+)\.(.*?)\]"
		matches = re.findall(regex,text,flags=re.IGNORECASE)
		for match in matches:
			actor = self.drama.actors[match[0]]
			key = "[actors."+match[0]+"."+match[1]+"]"
			value = actor.quirks[match[1]]
			text = text.replace(key,value)
		return text

	def __spawn(self,node):
		for process in node.findall("practice"):
			newprocess = self.__spawnprocess(process)
			self.roles = {}
			self.drama.practices[newprocess.id()] = newprocess
			for role in newprocess.roles.keys():
				members = newprocess.roles[role]
				membertags = []
				for member in members:
					membertags.append("actors."+member.name)
				self.roles[role] = membertags
			newprocess.execute()
		return ""


	def __spawnprocess(self,node):
		newprocess = SocialPractice(node,self.drama)
		#newprocess.name = node.get("name")
		#newprocess.root = self.drama.treeroot.find("practices/practice[@name='"+newprocess.name+"']")
		#print(ET.tostring(newprocess.root).decode())
		for roles in node.findall("roles"):
			for role in roles:
				for entities in role.findall("actor"):
					actor = self.drama.getActor(entities.get("name"))
					newprocess.addRole(role.tag,actor)
		return newprocess


def rotate(l):
	l.append(l.pop(0))
	return l
	#return l[1:]+[l[0]]

class Drama:

	def __init__(self,ws=None):
		self.actors = {}
		self.practices = {}
		self.ws = ws
		self.scenes = {}
		self.actions = []
		self.actors = {}
		self.beginning = ""
		self.dramaManager = DramaParser(self)
		self.currentScene = None
		self.logs = []
		self.ws.add("actors")
		self.ws.add("practices")

	def setWordState(self,state):
		self.ws = state

	def play(self):
		if self.currentScene == None:
			self.currentScene = self.scenes[self.beginning]
			for event in self.currentScene.findall("implications"):
				self.dramaManager.execute(event)
				for log in self.logs:
					print(log)
			self.agentlist = list(self.actors.keys())
		for practice_id in self.practices.keys():
			practice = self.practices.get(practice_id)
			practice.getAffordances()

		self.logs = []
		#actorlabel = random.choice(list(self.actors.keys()))
		self.agentlist = rotate(self.agentlist)
		actorlabel = self.agentlist[0]
		actor = self.actors.get(actorlabel)
		self.dramaManager.roles = {}
		self.dramaManager.roles["AGENT"] = ["actors."+actor.name]
		action = random.choice(actor.affordances)
		self.dramaManager.roles["PARENT"] = [action.parent.id()]
		#print(action.parent.roles)
		for role in action.parent.roles.keys():
			members = action.parent.roles[role]
			membertags = []
			for member in members:
				membertags.append("actors."+member.name)
			self.dramaManager.roles[role] = membertags


		action.execute()
		for log in self.logs:
			print(log)


		#for actorlabel in self.actors.keys():
			#actor = self.actors.get(actorlabel)
			#print(actor.affordances)



	def getActor(self,actorname):
		return self.actors.get(actorname)


	def loadActors(self,node):
		pass

	def load(self,filename):
		tree = ET.parse(filename)
		self.treeroot = tree.getroot()
		if self.treeroot.tag.lower() == "drama":
			for scene in self.treeroot.findall("scenes/scene"):
				#print(ET.tostring(scene).decode())
				#self.scenes.append(scene)
				self.scenes[scene.get("name")] = scene
				if self.beginning == "" : self.beginning = scene.get("name")
			for action in self.treeroot.findall("practices/practice/action"):
				self.actions.append(action)
			for actor in self.treeroot.findall("actors/actor"):
				newactor = Actor(self.ws.get("actors"))
				newactor.load(actor)
				self.actors[actor.get("name")] = newactor
				#self.ws.add("actors."+newactor.name)
				#print(newactor.quirks)
				#print(ET.tostring(action).decode())

	def __contextualize(self,text):
		regex = r"\[(.*?)\]"
		regex = r"\[actors\.(\w+)\.(.*?)\]"
		matches = re.findall(regex,text,flags=re.IGNORECASE)
		for match in matches:
			actor = self.actors[match[0]]
			key = "[actors."+match[0]+"."+match[1]+"]"
			value = actor.quirks[match[1]]
			text = text.replace(key,value)
		return text


class Node:

	def __init__(self,name="root",parent=None):
		self.children={}
		self.name=name
		self.parent=parent


	def __str__(self):
		return self.name

	def remove(self,keystring):
		removed = self.get(keystring)
		if removed == None : return 
		for childlabel in removed.children.keys():
			child = removed.children.get(childlabel)
			child.remove(childlabel)
		removed = None

	def add(self,keystring):
		keys = keystring.split(".")
		#print("ADDING: ", keystring)
		self.__add(keys)

	def __add(self,keys):
		child = self.children.get(keys[0])
		if child == None:
			child = Node(keys[0],self)
			self.children[keys[0]] = child
		if len(keys)>1:
			child.__add(keys[1:])

	def get(self,keystring):
		keys = keystring.split(".")
		return self.__get(keys)

	def __get(self,keys):
		child = self.children.get(keys[0])
		if child != None:
			if len(keys)>1:
				return child.__get(keys[1:])
			else:
				return child
		return None



class WorldState:

	def __init__(self,world = {}):
		self.root = world

	def has(self,text):
		elements = text.split(".")
		return self.__has(self.root,elements)

	def add(self,branch):
		branches = branch.split(".")
		return self.__add(self.root,branches)

	def __add(self,tree,branches):
		branch = tree.get(branches[0])
		if branch == None:
			branch = {}
			tree[branches[0]] = branch
		if len(branches) >1:
			self.__add(branch,branches[1:])

	def __has(self,tree,elements):
		branch = tree.get(elements[0])
		if branch == None:
			return branch
		else:
			if len(elements)>2:
				return self.__has(branch,elements[1:])
			else:
				return branch

class SocialPractice:

	def __init__(self, node=None, drama=None):
		self.roles = {} #dict over rolenames and actors associated
		self.actions = {} #dict over actions labels and the actions 
		self.name = node.get("name")
		self.root = drama.treeroot.find("practices/practice[@name='"+self.name+"']")
		self.drama = drama
		self.parser = drama.dramaManager

	def getAffordances(self):
		#print("Running %s" %self)
		for role in self.roles.keys():
			members = self.roles.get(role)
			for member in members:
				for action in self.root.findall("action"):
					member.affordances.append(Action(action,self))

	def addRole(self,role,actor):
		rolekey = self.roles.get(role)
		if rolekey == None : self.roles[role] = []
		self.roles[role].append(actor)

	def execute(self):
		for event in self.root.findall("spawn"):
			self.parser.execute(event)

	def __str__(self):
		return self.id()

	def id(self):
		output = self.name 
		for role in self.roles.keys():
			output += "." + role
			members = self.roles.get(role)
			for member in members:
				output += "." + member.name
		return output

class Actor:

	def __init__(self,ws=Node()):
		self.beliefs = []
		self.wants = []
		self.quirks = {}
		self.name = "Nameless"
		self.ws = ws
		self.affordances = []

	def load(self,branch):
		self.name = branch.get("name")
		self.ws.add(self.name)
		for quirks in branch.findall("quirks"):
			for quirk in quirks:
				self.__getquirk(quirk)

	def __getquirk(self,quirk, preface=""):
		self.quirks[preface+""+quirk.tag] = quirk.text.strip()
		for subquirk in quirk:
			self.__getquirk(subquirk,preface+""+quirk.tag+".")


class Action:

	def __init__(self, node=None, practice=None):
		self.preconditions = {}
		self.root = node
		self.drama = practice.drama
		self.parser = practice.drama.dramaManager
		self.parent = practice

	def execute(self):
		for event in self.root.findall("implications"):
			self.parser.execute(event)


	def load(self,file,branch):
		pass

def test(filename):
	if filename:
		with open(filename, 'r') as f:
			utopiaGenesis = json.load(f)
	utopia = WorldState(utopiaGenesis)
	#print(utopia.has("locations.green_forest.spring_of_life"))
	#print(utopia.has("locations.pink_clouds.eternal_breeze"))
	utopia.add("locations.pink_clouds.eternal_breeze")
	utopia.add("locations.old_barn")
	utopia.add("locations.old_windmill")
	#print(utopia.has("locations.pink_clouds.eternal_breeze"))
	#print(utopia.has("locations.green_forest.spring_of_life"))
	#print(utopia.has("locations"))
	return utopia



myroot = Node()
myroot.add("locations.castle")
myroot.add("locations.dungeon")
myroot.add("locations.forest")
print(myroot.get("locations.forest"))
print(myroot.get("locations"))

RW.cls()
drama = Drama(myroot)
drama.load("murdermystery.xml")
drama.play()
drama.play()
drama.play()
drama.play()
drama.play()

#regex = r"\[actors\.(\w+)\.(.*?)\]"
#test_str = "It was early morning with the sun slowly rising over the tree tops burning of morning mist. Grassy plains stretches onto the border of the forest. A hiking party was gathering in front of the old mansion. [actors.lydia.name.formel] and [actors.brown.name.formel] is here."
#matches = re.findall(regex,test_str,flags=re.MULTILINE | re.DOTALL)
#print(matches)


#print(myroot.get("actors.brown"))