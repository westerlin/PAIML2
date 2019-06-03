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


class DramaParser:

	def __init__(self, drama=None):
		self.commands = {
			"text": self.__text,
			"count" :self.__count,
			"spawn" :self.__spawn
		}
		self.drama = drama


	def execute(self,node):
		for child in node:
			command = self.commands.get(child.tag)
			if command != None:
				command(child)

	def __count(self,node):
		key = node.get("elements")
		if key != None:
			elements = drama.root.has(key)
			if elements != None:
				return str(len(elements))
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

	def __contextualize(self,text):
		#if self.context == None: return text
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
			self.drama.practices[newprocess.id()] = newprocess
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



class Drama:

	def __init__(self,ws=None):
		self.actors = {}
		self.practices = {}
		self.root = ws
		self.scenes = {}
		self.actions = []
		self.actors = {}
		self.beginning = ""
		self.dramaManager = DramaParser(self)
		self.currentScene = None
		self.logs = []

	def setWordState(self,state):
		self.root = state

	def play(self):
		if self.currentScene == None:
			self.currentScene = self.scenes[self.beginning]
			for event in self.currentScene.findall("implications"):
				self.dramaManager.execute(event)
				for log in self.logs:
					print(log)
		for practice_id in self.practices.keys():
			practice = self.practices.get(practice_id)
			practice.getAffordances()

		self.logs = []
		actorlabel = random.choice(list(self.actors.keys()))
		actor = self.actors.get(actorlabel)
		action = random.choice(actor.affordances)
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
				newactor = Actor()
				newactor.load(actor)
				self.actors[actor.get("name")] = newactor
				self.root.add("actors."+newactor.name)
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
					member.affordances.append(Action(action,self.drama))

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

	def __init__(self):
		self.beliefs = []
		self.wants = []
		self.quirks = {}
		self.name = "Nameless"
		self.affordances = []

	def load(self,branch):
		self.name = branch.get("name")
		for quirks in branch.findall("quirks"):
			for quirk in quirks:
				self.__getquirk(quirk)

	def __getquirk(self,quirk, preface=""):
		self.quirks[preface+""+quirk.tag] = quirk.text.strip()
		for subquirk in quirk:
			self.__getquirk(subquirk,preface+""+quirk.tag+".")


class Action:

	def __init__(self, node=None, drama=None):
		self.preconditions = {}
		self.root = node
		self.drama = drama
		self.parser = drama.dramaManager

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


RW.cls()
drama = Drama(test("utopia.json"))
drama.load("murdermystery.xml")
drama.play()

regex = r"\[actors\.(\w+)\.(.*?)\]"
test_str = "It was early morning with the sun slowly rising over the tree tops burning of morning mist. Grassy plains stretches onto the border of the forest. A hiking party was gathering in front of the old mansion. [actors.lydia.name.formel] and [actors.brown.name.formel] is here."
matches = re.findall(regex,test_str,flags=re.MULTILINE | re.DOTALL)
#print(matches)
