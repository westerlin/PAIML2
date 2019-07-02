from node import *
import random

def implement(command,world):
	cmd,parm = command
	if cmd == "text":
		print("\t",parm)
	if cmd == "add":
		world.add(parm)
		#print("\t"*4,"adding:",parm)
	if cmd == "remove":
		world.remove(parm)
		#print("\t"*4,"removing:",parm)
	return world

def populate(path,parms):
	adjusted = ""
	while path != adjusted:
		adjusted = path
		for key,item in parms.items():
			adjusted = path
			path = adjusted.replace("["+key+"]",item)
	return path

class Action:

	def __init__(self,scene=None):
		self.post = []
		self.prec = []
		self.scene = scene
		self.name = "unnamed"

	def instantiate(self,post):
		cmd,parm = post
		#print("ac:",self.scene,parm)
		parm = populate(parm,self.scene)
		#print("ac:",self.scene,parm)
		return (cmd,parm)

class SocialPractice:

	def __init__(self, global_state=None, parms=None):
		self.actions = {}
		self.gs = global_state
		self.parms = parms
		self.participants = []
		self.init = []

	def spawn(self, actions=None):
		if actions == None: actions = {"all":[]}
		for key,action in self.actions.items():
			scenarios = self.active(action)
			for scenario in scenarios:
				newAction = Action()
				newAction.precs = action.precs.copy()
				newAction.post = action.post.copy()
				newAction.name = key
				#newAction.scene = {**action.scene, **scenario}
				newAction.scene = {**scenario,**self.parms}
				agent = scenario.get("AGENT")
				if agent == None:
					actions["all"].append(newAction)
				else:
					if actions.get(agent) == None : actions[agent] = []
					actions[agent].append(newAction)
		return actions

	def active(self,action):
		scenarios = [{}]
		for condition in action.precs:
			#print(condition,self.parms)
			condition = populate(condition,self.parms)
			#print(condition,self.parms)
			scenarios = self.gs.combi(condition,scenarios)
			#print(scenarios)
		return scenarios

	def progress(self):
		exec_queue = self.spawn()
		flag = False
		for key,queue in exec_queue.items():
			#for action in queue:
				#print("\t"*8,action.name,":",action.scene)
			if len(queue) > 0:
				action = random.choice(queue)
				print("\t"*8,action.name,"performed by",key)
				for command in action.post:
					flag = True
					#print("bf:",command)
					command = action.instantiate(command)
					#print("af:",command,action.scene)
					self.gs = implement(command,self.gs)
		if not flag : print ("\n\t The end ...\n")
		return flag




"""
class Drama:

	def __init__(self, gs=None,ls=None):
		self.practices = {}
		self.gs = gs
		self.ls = ls

	def progress(self)
		for practice in self.gs.get("practices"):
			pass 
"""