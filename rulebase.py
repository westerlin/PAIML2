from node import *
from rwutility import *
import copy

RULESch = [	"1","2","3","4","5","6","7","8","9","a","b","c","d",
			"e","f","g","h","i","j","k","l","m","n","o","p","q","r",
			"s","t","v","w,","x","y","z"]


STAGES_EXECUTE_REACT_RANDOM=0
STAGES_EXECUTE_REACT_ORDER=1
STAGES_EXECUTE_ACT=2

def firstkey(val):
	return val[0]

def zipzap(dic1,dic2):
	for key,obj in dic2.items():
		dest = dic1.get(key)
		if dest != None:
			dest+=obj
		else:
			dic1[key] = obj
	return dic1

class Rule:

	def __init__(self,LHS=[],RHS=[],name="No name",scene={},debug=False,label="technical rule"):
		self.LHS = LHS
		self.RHS = RHS
		self.assessments = []
		self.name = name
		self.scene = scene
		self.debug = debug
		self.label = populate(label,scene)

	def __repr__(self):
		output = ""
		i =0
		if self.assessments == []: self.assessments = [None for condition in self.LHS]
		for condition in self.LHS:
			output += "\t"+str(self.assessments[i])+" "+condition+"\n"
			i +=1
		if output =="" : output="NO CONDUTIONS!"
		return ">>"+str(self.name)+":"+str(self.scene)+"\n"+str(output)

	def isActive(self,assertions):
		self.assessments = []
		output = True
		for condition in self.LHS:
			assessment = True
			node = assertions.get(condition)
			if node == None : 
				if condition[0] != "^":
					assessment = False
			else:
				if condition[0] == "^":
					assessment = False
			self.assessments.append(assessment)
			output = output and assessment
		if self.debug: 
			print(self)
		return output

	def execute(self,assertions,silent=False):
		for cmd,impact in self.RHS:
			if cmd == "add":
				assertions.add(impact)
			elif cmd == "remove":
				assertions.delete(impact)
			elif cmd == "text":
				if not silent: print("\t",Capitalize(impact))
			else:
				print("Error - unknow command:",cmd,"(",impact,")")


class Generic:

	def __init__(self,LHS=[],RHS=[],name="Unnamed",debug=False,label="technical rule"):
		self.LHS = LHS
		self.RHS = RHS
		self.name = name
		self.debug = debug
		self.label = label
		self.unique = True
		for condition in self.LHS:
			self.unique = self.unique and isUniquePath(condition)

	def spawnReacts(self,assertions):
		if self.unique : 
			if self.debug: print(self.name,"spawns one rule")
			return [Rule(self.LHS,self.RHS,self.name,{},self.debug,self.label)]
		scenes=[{}]

		for condition in self.LHS:
			if condition[0] != "^":
				scenes = assertions.combi(condition,scenes)
				if self.debug: 
					print(self.name,condition,scenes)

		rules = []
		for scene in scenes:
			LHS=[]
			RHS=[]
			for node in self.LHS:
				LHS.append(populate(node,scene))
			for cmd,node in self.RHS:
				RHS.append((cmd,populate(node,scene)))
			newrule = Rule(LHS,RHS,self.name,scene,self.debug,self.label)
			rules.append(newrule)
		if self.debug: print(self.name,"spawns %d rule(s)" %len(rules))
		return rules

	def spawnActors(self,assertions,keyword="ACTOR"):
		if self.unique : return {"all":[Rule(self.LHS,self.RHS,self.name,{},self.debug,self.label)]}

		for condition in self.LHS:
			if condition[0] != "^":
				scenes = assertions.combi(condition,scenes)

		rules = {"default":[]}
		for scene in scenes:
			for key,actor in scene:
				if key==keyword:
					rules[actor]=[]

		for scene in scenes:
			LHS=[]
			RHS=[]
			label = scene.get(keyword)
			if label == None:
				label = "default"
			for node in self.LHS:
				LHS.append(populate(node,scene))
			for cmd,node in self.RHS:
				RHS.append((cmd,populate(node,scene)))
			rules[label].append(Rule(LHS,RHS,self.name,scene,self.debug,self.label))

		return rules

	def spawnrules(self,assertions):
		if self.unique : return {"all":[Rule(self.LHS,self.RHS,self.name,{},self.debug,self.label)]}

		scenes=[{}]
		if self.debug : print(self.name)
		for condition in self.LHS:
			if condition[0] != "^":
				scenes = assertions.combi(condition,scenes)
				if self.debug: 
					print(" << : ",condition)
					print(" << : ",scenes)
		if self.debug: print(">>:"+self.name+":",scenes)

		output = {"all":[]}
		for scene in scenes:
			LHS=[]
			RHS=[]
			action = scene.get("ACTOR")
			if action != None:
				label = action
			else:
				label = "all"
			for condition in self.LHS:
				LHS.append(populate(condition,scene))
			for cmd,condition in self.RHS:
				RHS.append((cmd,populate(condition,scene)))

			if output.get(label) == None: 
				output[label]=[Rule(LHS,RHS,self.name,scene,self.debug,self.label)]
			else:
				output[label].append(Rule(LHS,RHS,self.name,scene,self.debug,self.label))

		return output


class Stage:

	def __init__(self,name="Default",qtype=STAGES_EXECUTE_REACT_RANDOM,quiescence=""):
		self.name = name
		self.generics = []
		self.quiescence = quiescence
		self.type = qtype

	def addRule(self,name,precs, posts,debug=False,label="No Label"):
		newrule = Generic(LHS=precs,RHS=posts,name=name,debug=debug,label=label)
		self.generics.append(newrule)

	def __repr__(self):
		return self.name + "("+str(len(self.generics))+" rules)"

class Rules:

	def __init__(self,assertions):
		self.ws=assertions
		self.generics = []
		self.players=[]
		self.userinput = Userinput()
		self.stages = {}
		self.logging = False

	def evaluate(self,key,ws):
		return 0

	def execute(self,stageName):
		stage = self.stages.get(stageName)
		if self.logging : print("running .... ",stageName)
		quiescence = False
		while not quiescence:
			quiescence = self.executeStage(stage)
		return stage.quiescence

	def executeStage(self,stage):
		if stage.type != STAGES_EXECUTE_ACT:
			return self.__react(stage)
		else:
			return self.__act(stage)

	def __react(self,stage):
		rules = []
		for generic in stage.generics:
			rules += generic.spawnReacts(self.ws)
		conflict_set = [rule for rule in rules if rule.isActive(self.ws)]
		quiescence = True
		if conflict_set != []:
			if stage.type == STAGES_EXECUTE_REACT_RANDOM:
				random.shuffle(conflict_set)
			for rule in conflict_set:
				if rule.isActive(self.ws):
					quiescence = False
					rule.execute(self.ws)
		else:
			if self.logging : print("No conflict set for",stage)
		return quiescence


	def __npcActions(self):
		strategy = []
		for affordance in affordances:
			bk = copy.deepcopy(self.ws)
			affordance.execute(bk,silent=True)
			strategy.append((self.evaluate(key,bk),affordance))
		strategy.sort(key=firstkey)
		random.shuffle(strategy)
		strategy[0][1].execute(self.ws)

	def __playerActions(self):
		idx = 0
		print("\n Please choose from the following")
		for affordance in affordances:
			print("\t"+RULESch[idx]+". "+affordance.label)
			idx +=1
		ptn1 = '&'
		choice = -1
		while choice==-1:
			ptn1 = self.userinput.get()
			if ptn1==rw_ESC : return False
			try:
				choice = RULESch.index(ptn1)
			except:
				choice = -1
			if choice > len(affordances)-1: choice = -1
		act = affordances[choice]
		print()
		act.execute(self.ws)


	def __act(self,stage):
		rules = {}
		for generic in stage.generics:
			rules = zipzap(rules,generic.spawnrules(self.ws))

		for key,obj in rules.items():
			affordances = [rule for rule in obj if rule.isActive(self.ws)]
			if affordances != []:
				if key not in self.players:
					self.__npcActions()
				else:
					self.__playerActions()
		return True


	def execute2(self):
		rules = {}
		for generic in self.generics:
			rules = zipzap(rules,generic.spawnrules(self.ws))
		output = False

		rules_all = rules.get("all")
		if rules_all != None:
			conflict_set = [rule for rule in rules["all"] if rule.isActive(self.ws)]
			while conflict_set != []:
				random.shuffle(conflict_set)
				for rule in conflict_set:
					if rule.isActive(self.ws):
						#print(rule)
						rule.execute(self.ws)
						output = True
				rules = {}
				for generic in self.generics:
					rules = zipzap(rules,generic.spawnrules(self.ws))
				output = False
				conflict_set = [rule for rule in rules["all"] if rule.isActive(self.ws)]

			rules.pop("all")

		if 1==0:
			for key,obj in rules.items():
				affordances = [rule for rule in obj if rule.isActive(self.ws)]
				if affordances != []:
					print ("ACTOR:",key,end="{")
					for rule in affordances:
						if rule != affordances[-1]:
							print(rule.name,end=", ")
						else:
							print(rule.name,end="")
					print("}")
		for key,obj in rules.items():
			affordances = [rule for rule in obj if rule.isActive(self.ws)]
			if affordances != []:
				output=True
				if key not in self.players:
					strategy = []
					for affordance in affordances:
						bk = copy.deepcopy(self.ws)
						affordance.execute(bk,silent=True)
						strategy.append((self.evaluate(key,bk),affordance))
					strategy.sort(key=firstkey)
					random.shuffle(strategy)
					#act = random.choice(affordances)
					#print()
					strategy[0][1].execute(self.ws)
				else:
					idx = 0
					print("\n Please choose from the following")
					for affordance in affordances:
						print("\t"+RULESch[idx]+". "+affordance.label)
						idx +=1
					ptn1 = '&'
					choice = -1
					while choice==-1:
						ptn1 = self.userinput.get()
						if ptn1==rw_ESC : return False
						try:
							choice = RULESch.index(ptn1)
						except:
							choice = -1
						if choice > len(affordances)-1: choice = -1
					act = affordances[choice]
					print()
					act.execute(self.ws)
		return output


	def addRule(self,name,precs, posts,debug=False,label="No Label"):
		newrule = Generic(LHS=precs,RHS=posts,name=name,debug=debug,label=label)
		self.generics.append(newrule)

	def addStage(self,stage):
		self.stages[stage.name]=stage