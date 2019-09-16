from rete import *
import random

DRAMA_ORDER=0
DRAMA_RANDOM=1
DRAMA_SELECTION=2
DRAMA_MAX=3

DRAMA_QUISIANCE=0
DRAMA_ALL_ONE=1
DRAMA_SINGLETON=2

NO_REPEAT_OF_RULE=True

class Drama:

	def __init__(self):
		self.rete = ReteEngine()
		self.schemas = {}
		self.log = []

	def log(self,text):
		self.log.append(text)

	def addRule(self,rule):
		self.rete.addRule(rule)

	def execute(self,label,method=DRAMA_ORDER,end=DRAMA_QUISIANCE):
		schema = self.schemas.get(label)
		if schema != None:	
			choiceMethod = self.__randomChoice
			if end==DRAMA_QUISIANCE:
				self.__quisiance(schema,choiceMethod)
		else:
			print("Error, no schema %s" %label)

	def __quisiance(self,schema,choiceMethod):
		ruletoken=choiceMethod(schema)
		while ruletoken != None:
			if NO_REPEAT_OF_RULE:
				self.rete.revoke(ruletoken[0],ruletoken[1])
			self.executeRule(ruletoken)
			ruletoken=choiceMethod(schema)

	def __randomChoice(self,schema):
		temp = schema.filter(self.rete.conflictset)
		if len(temp) >0: return random.choice(temp)
		return None

	def executeRule(self,ruletoken):
		print(" - Activating rule %s with %s " %(ruletoken[0],str(ruletoken[1].params)))
		## Here goes the Right-hand side of the rule

	def addSchema(self,schema):
		self.schemas[schema.label] = schema
		for key,rule in schema.rules.items():
			if rule not in self.rete.rules:
				self.rete.addRule(rule)

	def addFact(self,fact):
		self.rete.addFact(fact)

	def addRemove(self,fact):
		self.rete.removeFact(fact)

class Schema:

	def __init__(self, label=""):
		self.label = label
		self.rules = {}

	def addRule(self,rule):
		self.rules[rule.label] = rule

	def filter(self,conflictset):
		rules = []
		for key in self.rules.keys():
			rule = conflictset.get(key)
			if rule != None:
				for tkey, token in rule.items():
					rules.append((key,token))
		return rules


