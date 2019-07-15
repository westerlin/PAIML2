import re
from node import *
import copy

def mergeParameters(d1,d2):
	output = d1.copy()
	for k,v in d2.items():
		compare = output.get(k)
		if compare != None and compare !=v:
			return None
		else:
			output[k]=v
	return output

class Token:

	def __init__(self,path):
		self.path = path
		self.branches = self.__split(path)
		self.params = {}
		self.key = "".join([key for (tag,key) in self.branches])

	def __repr__(self):
		return self.path#+","+str(self.params)

	def __split(self,path):
		pattern = r'([\.|\!|\^]?)([\w|\*]+)'
		return re.findall(pattern,path)

	def label(self,level):
		if level >= len(self.branches): return None
		return self.branches[level][1]

	""" Create parameters when token wanders """
	def addParam(self,key,level):
		param = self.params.get(key)
		if param == None:
			self.params[key] = self.label(level)
			#print("created:",key,self.params)
			return True
		elif param == key:
			#print("DID find:",key,param,self.params)
			return True
		#print("DID not find:",key,param,self.params)
		return False

	def samePath(self,token):
		keyMin = min(len(self.key),len(token.key))
		return self.path[:keyMin] == token.path[:keyMin]


"""
	def key(self,level):
		level = min(level,len(self.branches)-1)
		output = "root"
		if level <0: return output
		for step in range(level):
			output += "."+self.branches[step][1]
		return output
	@classmethod
    def createToken(path):
    	self.__split(path)
"""

class Rule:

	def __init__(self,label,LHS,reteEngine=None):
		self.label = label
		self.LHS = LHS
		self.RHS = []
		self.active = False
		self.fired = False #for one time
		self.rete = reteEngine

	def fire(self,tokengroup):
		if self.rete != None: self.rete.fire(self.label,tokengroup)
		print("Rule %s was activated" %self.label)
		for condition in self.LHS:
			print(" "*5,"(+):",populate(condition,tokengroup.params))

	def revoke(self,tokengroup):
		if self.rete != None: self.rete.revoke(self.label,tokengroup)
		print("Rule %s was revoked" %self.label)
		for condition in self.LHS:
			print(" "*5,"(+):",populate(condition,tokengroup.params))

class TokenGroup:

	def __init__(self):
		#self.conditions = {}
		self.conditions = []
		self.params = {}
		self.posted = False

	def __str__(self):
		sign = "(-)"
		if self.posted: sign = "(+)"
		return sign+": "+str(self.conditions)+" "+str(self.params)

	def addToken(self,token,idx):
		#self.conditions[idx] = token.path
		self.conditions = [token]
		self.params = {**token.params}

	def samePath(self,otherTG):
		for condition in otherTG.conditions:
			if self.conditions[0].samePath(condition): 
				return True
		return False

	def key(self):
		hash_tuple = []
		for condition in self.conditions:
			hash_tuple.append(condition.key)
		for k,v in self.params.items():
			hash_tuple.append(k+v)
		return hash(tuple(hash_tuple))

	def merge(self,tokenGroup):
		mergeTG = TokenGroup()
		mergeTG.params = mergeParameters(self.params, tokenGroup.params)
		if mergeTG.params == None : return None
		#mergeTG.conditions = list(set(self.conditions + tokenGroup.conditions))
		mergeTG.conditions = self.conditions + tokenGroup.conditions
		#mergeTG.conditions = self.conditions + tokenGroup.conditions
		"""
		mergeTG.conditions = self.conditions.copy()
		for k,v in tokenGroup.conditions.items():
			if k in mergeTG.conditions:
				return None
			else:
				mergeTG.conditions[k]=v
		"""
		self.posted = True
		mergeTG.posted = True
		return mergeTG

class BetaNode:

	def __init__(self):
		self.buckets = [{},{}]
		self.betas = []
		self.rule = None
		self.signals = {}
		self.blocks = []
		self.level = -1

	def removeTokenGroup(self,idx,revokeTG):
		#self.buckets[idx].pop(newTG.key())
		print("   "*self.level," (%d) Removing:"%self.level,revokeTG)
		for bucket in self.buckets:
			deletions = []
			for key,TG in bucket.items():
				if revokeTG.samePath(TG): 
					print("  - found one for deletion:",TG)
					deletions.append((key,TG))
			for TGkey,TG in deletions:
				test = bucket.get(TGkey)
				if test != None:
					bucket.pop(TGkey)
		deletions = {}
		for key,TG in self.signals.items():
			if revokeTG.samePath(TG): 
				deletions[key]=TG
		#deletions = list(set(deletions))
		for key,TG in deletions.items():
			print("   "*self.level,"Revoking tokengroup:\n\t",key,"\n\t",TG)
			self.signals.pop(key)
			if self.rule != None : 
				self.rule.revoke(TG)
				print("   "*self.level,"remove rule at layer",self.level)
		for (idx,beta) in self.betas:
			beta.removeTokenGroup(idx,revokeTG)

	def addTokenGroup(self,idx,newTG):
		print("   "*self.level," (%d) Adding:" %self.level,newTG)
		self.buckets[idx][newTG.key()] = newTG
		for lKey,leftTG in self.buckets[0].items():
			for rKey, rightTG in self.buckets[1].items():
				if not leftTG.posted or not rightTG.posted:
#				for rKey, rightTG in self.buckets[1].items():
					outTG = leftTG.merge(rightTG)
					if outTG != None:
						leftTG.posted = True
						rightTG.posted = True
						if outTG.key() not in self.signals.keys():
							self.signals[outTG.key()]=outTG
							for (idx,beta) in self.betas:
								beta.addTokenGroup(idx,outTG)
							if self.rule != None : self.rule.fire(outTG)
					else:
						self.blocks.append((leftTG,rightTG))

	def output(self):
		idx = 1
		print("  -----------oooooOOOOOooooo-----------")

		if self.rule != None:
			print("(+) BetaNode for rule %s" % self.rule.label.capitalize())
		else:
			print("(+) BetaNode ")
		for bucket in self.buckets:
			print("  (+) %d Bucket:" %(idx))
			for key,tokengroup in bucket.items():
				print(" "*5," (+):",str(tokengroup))
			idx += 1
		print("  (+) Signals:")
		for key,tokengroup in self.signals.items():
			if tokengroup.posted:
				print(" "*5," (+):",str(tokengroup))
		print("  (+) Blockings:")
		for block in self.blocks:
			print("   (X) Block")
			for tokengroup in block:
				print(" "*5," (+):",str(tokengroup))
		print("  -----------oooooOOOOOooooo-----------")

class BetaNode1:

	def __init__(self,rule=None):
		self.sockets = []
		self.tokenGroups = []#[{"set":{}}]
		self.rule = rule
		self.actives = []

	def addsocket(self,socket):
		self.sockets.append(socket)


	def addToken(self,token,socket):
		idx = self.sockets.index(socket)
		print("\tRECEIVED:",token,token.params)
		#print("firing token %d" %idx,token)
		addOns = []
		flag = False
		#print("MERGING:",token.params,"for",len(self.tokenGroups),".")
		group = {idx:token,"set":{**token.params}}
		self.tokenGroups.append(group)
		for group in self.tokenGroups:
			#condition = group.get(idx)
			#if condition != None:
			#	group = {**group}
			#	addOns.append(group)
			mset = mergeParameters(token.params,group.get("set"))
			#print("mset:",mset)
			if mset != None:
				flag = True
				#print(". WAS MERGED FOR:",group.get("set"))
				group[idx]=token
				group["set"]=mset
			else:
				pass
				#group = {idx:token,"set":{**token.params}}
				#addOns.append(group)

		#self.tokenGroups += addOns
		if False:
			group = {idx:token,"set":{**token.params}}
			#print("COULD NOT MERGE - NEW",group)
			self.tokenGroups.append(group)
		#addOns.append(group)

		for group in self.tokenGroups:
			if (len(group)-1) == len(self.sockets):
				#print(group)
				#print(self.sockets)
				if self.rule != None: self.rule.fire(group["set"])
				self.actives.append(group)
				#print(self.actives)

		#self.tokenGroups += addOns
		#for tokenGroup in self.tokenGroups:
		#	print(tokenGroup)

	def removeToken(self,token,socket):
		idx = self.sockets.index(socket)
		removals = []
		for group in self.tokenGroups:
			tokenD = group.get(idx)
			if token.samePath(tokenD):
				group.pop(idx)
				if len(group): removals.append(group)
		for group in removals:
			self.tokenGroups.remove(group)
		

	def output(self):
		idx = 0
		print("  -----------oooooOOOOOooooo-----------")

		print("(+) BetaNode for rule %s" % self.rule.label.capitalize())
		for tokengroup in self.tokenGroups:
			print(" "*2,"(+) Group %d" %idx,"("+str(len(self.sockets)==len(tokengroup)-1)	+")")
			print(" "*5," ( ):",tokengroup["set"])
			for key,token in tokengroup.items():
				if key != "set":
					print(" "*5," (%d):"%key,token)
			idx += 1
		print("  -----------oooooOOOOOooooo-----------")

class ReteNode:

	# A Rete node is a link in an condition
	## A chain of Rete Nodes represents a condition
	## Several Rete Chains point to the same rule may fire rule at last
	## Rete nodes sends nodes on to next level as long as tokens meets ReteChain conditions
	## When token reaches a node with rules it will active the rules condition

	def __init__(self,label="root",tag=None):
		self.label = label
		self.children = {}
		self.tokens = {} # Collects tokens - for each rule
		self.betas = []
		self.alias = None
		self.level = 0
		self.tag = tag
		self.key = label


	def removeToken(self,token,leafNode=None):
		deleteTokens = [key for key,dtoken in self.tokens.items() if token.samePath(dtoken)]
		for tokenkey in deleteTokens:
			deletedToken = self.tokens.pop(tokenkey)
			for (idx,beta) in self.betas:
				newTG = TokenGroup()
				newTG.addToken(token,idx)
				beta.removeTokenGroup(idx,newTG) 
		for key,child in self.children.items():
			child.removeToken(token)
		return None

	def __removeall(self):
		for key,child in self.children.items():
			child.__removeall()
			child.tokens = {}

	def compare(self,token):
		for key,otoken in self.tokens.items():
			"""
			if not token.samePath(otoken) : 
				print(otoken.path,token.path)
				return False
			"""
			if token.label(self.level-1) != otoken.label(self.level-1) : 
				print(token.label(self.level-1) ,"vs" ,otoken.label(self.level-1)  )
				return False
		return True

	def runBeta(self):
		for key,token in self.tokens.items():
			for (idx,beta) in self.betas:
				newTG = TokenGroup()
				newTG.addToken(token,idx)
				beta.addTokenGroup(idx,newTG) 

	def addToken(self,token,adding=True,cutoff=None):
		#print(tokenkey,self.tokens)
		dublicate = copy.deepcopy(token)
		if self.tag == "!" and not self.compare(token):
			self.__removeall()
			self.tokens = {}
			return self
		if adding: 
			self.tokens[token.key]=token
			#if self.alias != None:
				#print(" (%d) ALISA NODE:" %self.level,token.key,self.tokens)
			for (idx,beta) in self.betas:
				newTG = TokenGroup()
				newTG.addToken(token,idx)
				beta.addTokenGroup(idx,newTG) 
		tokenkey = token.label(self.level)
		if tokenkey != None: 
			for key,child in self.children.items():
				token = copy.deepcopy(dublicate)
				#if child.alias != None:
				#	print("checking",key)
				# Central check
				if tokenkey == key:
					child.addToken(token,adding)
				if child.alias != None:
					#print(" (%d) ALIAS:" %self.level,child.alias,key,adding)
					if token.addParam(key[1:-1],self.level):
						#print("adding:",token,child.tokens,child.alias)
						child.addToken(token,adding)
		return self

	def addCondition(self,keys):
		tag = keys[0][0]
		key = keys[0][1]
		#print(tag,key)
		child = self.children.get(key)
		if child == None : 
			child = ReteNode(key,tag)
			parampattern = r'^([\[|\{\(]\w+[\]|\}\)])$'
			child.level = self.level+1
			if re.match(parampattern,key): child.alias=key[1:-1] #cuts front an back
			self.children[key] = child
			#print("adding",key)
			for key,token in self.tokens.items():
				self.addToken(token)
		if len(keys)>1:
			return child.addCondition(keys[1:])
		else:
			return child

	def output(self):
		output=""
		for key,token in self.tokens.items():
			output += str(token) + " "
		print("   "*self.level,"(+)",self.label,"\t(tokens:",len(self.tokens),"outputs:",len(self.betas),")")
		for key,token in self.tokens.items():
			print("   "*(self.level+1),"   -",str(token),str(token.params))

		for (key,child) in self.children.items():
			child.output()


class ReteEngine:

	def __init__(self):
		self.rules = []
		self.facts = []
		self.root = ReteNode()
		self.betas = []
		self.conflictset = {}

	def addFact(self,fact):
		print("  (+) adding:",fact)
		cleanPath = fact.split("!")
		if len(cleanPath)>1:
			token = Token(cleanPath[0])
			self.root.removeToken(token)
		token = Token(fact)
		self.root.addToken(token)

	def removeFact(self,fact):
		token = Token(fact)
		self.root.removeToken(token)

	def addRule(self,rule):
		#beta = BetaNode(rule)
		rule.rete = self
		self.conflictset[rule.label]={}
		conditions = []
		for path in rule.LHS:
			condition = self.addCondition(path)
			#beta.addsocket(condition)
			#condition.betas.append(beta)
			conditions.append(condition)
			self.rules.append(rule)
		#self.betas.append(beta)
		prev = conditions[0]
		level =0
		for condition in conditions:
			if condition != conditions[0]:
				beta = BetaNode()
				beta.level = level
				condition.betas.append((1,beta))
				prev.betas.append((0,beta))
				prev = beta
				self.betas.append(beta)
				level += 1
		print(" (-) ADDED %d level(s) til rule %s" %(level,rule.label))
		beta.rule = rule
		for condition in conditions:
			condition.runBeta()

	def addCondition(self,condition):
		pattern = r'([\.|\!|\^]?)([\[|\{|\()]?[\w|\*]+[\]|\}|\)]?)'
		keys = re.findall(pattern,condition)
		return self.root.addCondition(keys)

	def output(self):
		print("\n Rules in conflict set:")
		print(" ----------------------")
		for rule,tokengroups in self.conflictset.items():
			print("  Rule: ",rule.capitalize())
			for key, tokengroup in tokengroups.items():
				print("\t",tokengroup)
		#for beta in self.betas:
		#	if beta.rule != None and 1==1 : beta.output()

	def fire(self,rulelabel,tokengroup):
		self.conflictset[rulelabel][tokengroup.key()]=tokengroup

	def revoke(self,rulelabel,tokengroup):
		tg = self.conflictset[rulelabel].get(tokengroup.key())
		if tg != None:		
			self.conflictset[rulelabel].pop(tokengroup.key())
