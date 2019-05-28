import xml.etree.ElementTree as ET
import random
import re

def safeRetriveDefault(dictionary,label, default):
	leaf = dictionary.get(label)
	if leaf == None:
		return default
	else: 
		return leaf

def getInnerXML(node):
	#output = ET.tostring(node).decode()
	#output = output.replace("<"+node.tag+">\n","**")
	#output = output.replace("\n</"+node.tag+">","**")
	#return output
	output = node.text
	for child in node:
		#print(child.text,child.tail,ET.tostring(child).decode(),child.tag, child.attrib)
		output += ET.tostring(child).decode()
	return output

class Category:
    
	def __init__(self):
		self.patterns = []
		self.templates = []
		self.res = None

	def addPattern(self,pattern):
		pattern = re.sub(r'[\*]',r'(.*)',pattern)
		#print(pattern)
		self.patterns.append(pattern)
        
	def addTemplate(self,template):
		#print(template)
		#template = template.replace("<star />","{params[1]}")
		#template = template.replace("<star index=\"1\" />","{params[2]}")
		#template = template.replace("<star index=\"2\" />","{params[3]}")
		#print(template)
		self.templates.append(template)
        
	def matchPattern(self,userinput):
		for pattern in self.patterns:
			self.res = re.match(pattern,userinput,flags=re.IGNORECASE)
			if self.res != None:
				#print(self.res.groups())
				return True
		return False    

	def process(self,userinput):
		if self.matchPattern(userinput):
			response = random.choice(self.templates)
			return response
		return None
    
	def normalization(self,text):
		#Remove punctuation
		#Expand contractions
		#Correct a few common spelling mistakes
		#Ensure one space between words
		return text

class AIML:

	def __init__(self):
		self.label = "nameless"
		self.defaultresponse = "Sorry, I don't know about that"
		#self.ontology = {}
		#self.setOntology("colors",["red","green","yellow","blue"])
		self.categories = []
		self.knowledge = {}
		self.commands = {
			"command" : self.__someCommand,
			"template" : self.__template,
			"li" : self.__template,
			"star" : self.__star,
			"srai" : self.__srai,
			"random" : self.__random,
			"set" : self.__setparam,
			"get" : self.__getparam,
			"condition" : self.__condition,
			"think" : self.__think
		}

		self.params = None

	def setOntology(self,label,elements):
		self.ontology[label] = elements 

	def loadPersona(self,aimlfile):
		self.tree = ET.parse(aimlfile)
		self.root = self.tree.getroot()
		self.source = aimlfile
		if self.root.tag.lower() == "aiml":
			version = safeRetriveDefault(self.root.attrib,"version","1.0")
			for category in self.root.findall("category"):
				cat = Category()
				for pattern in category.findall("pattern"):
					cat.addPattern(pattern.text)
				for template in category.findall("template"):
					cat.addTemplate(template)
				self.categories.append(cat)
		else:
			raise Exception('Error loading {}. Missing AIML tag.'.format(aimlfile))

	def __someCommand(self):
		print ("Testing command")

	def process(self,sentence):
		response = self.__processSentence(sentence)
		if response == None : return self.defaultresponse
		return response.replace("\n","").strip().replace("\t","")
        
	def __processSentence(self,sentence):
		for category in self.categories:
			template = category.process(sentence)
			if template != None: 
				self.params = category.res
				return self.commands[template.tag](template)
		return None		


	def __template(self, node):
		response = ""
		if node.text != None: response += node.text
		for children in node:
			response += self.commands[children.tag](children)
			if children.tail != None: response += children.tail
			#response += "*"+children.tail
		return response

	def __star(self,node):
		if node.attrib == {}:
			if self.params != None:
				return self.params[1]
			else:
				raise Exception("Error finding first 'star' parameter")
		else:
			return self.params[int(node.attrib["index"])+1]				

	def __srai(self,node):
		response = self.__template(node)
		return self.__processSentence(response)

	def __random(self,node):
		affordances = []
		for children in node:
			affordances.append(self.__template(children))
		return random.choice(affordances)

	def __getparam(self,node):
		return self.knowledge[node.attrib["name"]] + self.__template(node)

	def __setparam(self,node):
		value = self.__template(node)
		self.knowledge[node.attrib["name"]] = value
		return value

	def __condition(self,node):
		fact = node.attrib.get("name")
		value = node.attrib.get("value")
		if fact != None and value != None:
			exists = safeRetriveDefault(self.knowledge,fact,"__undefined__")
			if exists == value:
				return self.__template(node)
			else:
				return ""
		elif fact != None:
			exists = safeRetriveDefault(self.knowledge,fact,"__undefined__")
			if exists != "__undefined__":
				return self.__template(node)
		return ""

	def __think(self,node):
		self.__template(node)
		return ""