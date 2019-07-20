import re
from node import *
#import copy
from rwutility import *

debugging = False

def setDebugging(debugFlag):
	debugging = debugFlag

def replaceAliases(text):
	pattern = r'([\[][^\]]*[\]])'
	return re.sub(pattern,"*",text)

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

	def copy(self):
		newToken = Token(self.path)
		newToken.params = {**self.params}
		return newToken

	def cutOff(self,levels):
		newPath = ""
		for level in range(levels):
			newPath += self.branches[level][0]+self.branches[level][1]
		newToken = Token(newPath)
		newToken.params = {**self.params}
		return newToken

	def __split(self,path):
		pattern = r'([\.|\!|\^]?)([\w|\*|\[|\]]+)'
		return re.findall(pattern,path)

	def label(self,level):
		#if level >= len(self.branches): return None
		return self.branches[level][1]

	""" Create parameters when token wanders """
	def addParam(self,key,level):
		param = self.params.get(key)
		if param == None:
			self.params[key] = self.label(level)
			#print("created:",key,self.params)
			return True
		elif param == self.label(level):
			#print("DID find:",key,param,self.params)
			return True
		#print("DID not find:",key,param,self.params)
		return False

	def samePath(self,token,keyMin=-1):
		if keyMin < 0 : keyMin = min(len(self.branches),len(token.branches))	
		for idx in range(keyMin):
			if self.branches[idx][1] != token.branches[idx][1] and token.branches[idx][1] != "*":
				return False
		return True
		#return self.key[:keyMin] == token.key[:keyMin]

	def applyParams(self,params):
		#print("Changing::",self.path)
		self.path = populate(self.path,params)
		self.path = replaceAliases(self.path)
		self.branches = self.__split(self.path)
		self.key = "".join([key for (tag,key) in self.branches])
		#print("  To:",self.path)
		#print("    Branches:",self.branches)
		#print("    key:",self.key)


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
		self.betas = []

	def fire(self,tokengroup):
		if self.rete != None: self.rete.fire(self.label,tokengroup)
		if debugging : print(RAWU_FCGREEN,"Rule %s was activated" %self.label,RAWU_RESET)
		for condition in self.LHS:
			if debugging : print(" "*5,"(+):",populate(condition,tokengroup.params))

	def revoke(self,tokengroup):
		if self.rete != None: self.rete.revoke(self.label,tokengroup)
		if debugging : print(RAWU_FCRED,"Rule %s was revoked" %self.label,RAWU_RESET)
		for condition in self.LHS:
			if debugging : print(" "*5,"(+):",populate(condition,tokengroup.params))

	def output(self):
		print(RAWU_FCYELLOW,"\n Rule %s:" % self.label.capitalize(),RAWU_RESET)
		for beta in self.betas:
			beta.output()


class TokenGroup:

	def __init__(self):
		#self.conditions = {}
		self.conditions = []
		self.params = {}
		self.posted = False
		self.can_be_posted = True

	def __str__(self):
		sign = "(-)"
		if self.posted: sign = "(+)"
		return sign+": "+str(self.conditions)+" "+str(self.params)

	def output(self,inset=1):
		sign = "(-)"
		if self.posted: sign = "(+)"
		print(RAWU_RESET," "*inset,sign,str(self.params),RAWU_DIM)
		for condition in self.conditions:
			print(" "*(inset+2),"(*)",str(condition))
		print(RAWU_RESET,end="")


	def addToken(self,token,idx):
		#self.conditions[idx] = token.path
		self.conditions = [token]
		self.params = {**token.params}

	def samePath(self,otherTG):
		for condition in otherTG.conditions:
			#print(condition.key)

			#OtherTG skal fortolkes via PARAMS
			#condition.key = populate(condition.key,self.params)
			#for key,branch in condition.branches:
			#	branch = populate(branch,self.params)
			
			#print(condition.key)
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

		for condition in self.conditions:
			newToken = condition.copy()
			newToken.applyParams(mergeTG.params)
			#print(";;;;;",newToken)
			mergeTG.conditions.append(newToken)
		for condition in tokenGroup.conditions:
			newToken = condition.copy()
			newToken.applyParams(mergeTG.params)
			#print(";;;;;",newToken)
			mergeTG.conditions.append(newToken)


		#mergeTG.conditions = self.conditions + tokenGroup.conditions
		#mergeTG.conditions = self.conditions + tokenGroup.conditions
		"""
		mergeTG.conditions = self.conditions.copy()
		for k,v in tokenGroup.conditions.items():
			if k in mergeTG.conditions:
				return None
			else:
				mergeTG.conditions[k]=v
		"""
		#self.posted = self.can_be_posted
		#mergeTG.posted = mergeTG.can_be_posted
		return mergeTG

class BetaNode:

	def __init__(self):
		self.buckets = [{},{}]
		self.betas = []
		self.rule = None
		self.signals = {}
		self.blocks = []
		self.level = -1
		self.negation = [False,False]

	def setNegation(self,idx,path):
		if path[0] == "^":
			#path = replaceAliases(path)
			self.negation[idx] = True
			token = Token(path[1:])
			tokengroup = TokenGroup()
			tokengroup.addToken(token,idx)
			tokengroup.can_be_posted = False
			self.buckets[idx][tokengroup.key()]=tokengroup
			if debugging : print(RAWU_DIM,"  "*self.level," (-) Added negation:",idx,path,RAWU_RESET)

	def removeTokenGroup(self,idx,revokeTG,switch=True):
		#self.buckets[idx].pop(newTG.key())
		if self.negation[idx] and switch: 
			if debugging : print(RAWU_FCGREEN," (%d,%d) Remove tokengroup - but switching" %(idx,self.level),RAWU_RESET)
			self.addTokenGroup(idx,revokeTG,False)
			return None
		if debugging : 
			print(RAWU_FCRED,"   "*self.level," (%d) Removing tokengroup:"%self.level,RAWU_RESET)
			revokeTG.output(3*self.level+2)
		for bucket in self.buckets:
			deletions = []
			for key,TG in bucket.items():
				if revokeTG.samePath(TG): 
					if debugging : 
						print(RAWU_FCRED,"   "*self.level," (%d) Found one for deletion:"%self.level,RAWU_RESET)
						TG.output(self.level*3+2)
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
			if debugging : 
				print(RAWU_FCRED,"   "*(self.level),"    (-) Revoking Signal tokengroup:",hex(key),RAWU_RESET)
				#TG.output(5+self.level*3)
				#print("END OF REVOKE")
			#print("   "*self.level,"SIGNALPOPPING:",key)
			popped = self.signals.pop(key)
			if debugging: popped.output(5+self.level*2)
			if self.rule != None : 
				self.rule.revoke(TG)
				if debugging : print(RAWU_FCRED,"   "*self.level,"remove rule at layer",self.level,RAWU_RESET)
		for (idx,beta) in self.betas:
			beta.removeTokenGroup(idx,revokeTG)

	def addTokenGroup(self,idx,newTG,switch=True):
		if self.negation[idx] and switch: 
			if debugging : print(RAWU_FCYELLOW," (bckt:%d,lvl:%d) Adding tokengroup - but switching" %(idx,self.level),RAWU_BOLD)
			self.removeTokenGroup(idx,newTG,False)
			return None
		if debugging : 
			print(RAWU_FCGREEN,"   "*self.level," (%d) Adding tokengroup:" %self.level,RAWU_RESET)
			newTG.output(self.level*3+3)
		#newTG.posted = False
		self.buckets[idx][newTG.key()] = newTG
		for lKey,leftTG in self.buckets[0].items():
			for rKey, rightTG in self.buckets[1].items():
				if not leftTG.posted or not rightTG.posted:
#				for rKey, rightTG in self.buckets[1].items():
					outTG = leftTG.merge(rightTG)
					if outTG != None:
						leftTG.posted = leftTG.can_be_posted
						rightTG.posted = rightTG.can_be_posted
						if outTG.key() not in self.signals.keys():
							self.signals[outTG.key()]=outTG
							for (idx,beta) in self.betas:
								beta.addTokenGroup(idx,outTG)
							if self.rule != None : self.rule.fire(outTG)
						else:
							if False:
								print(RAWU_FCRED," Level %d"%self.level,"ERROR - signal already exposed.",RAWU_RESET)
								outTG.output(5)
								print(" "*4,"Composed of:")
								leftTG.output(5)
								print(" "*7,"was posted",leftTG.posted)
								rightTG.output(5)
								print(" "*7,"was posted",rightTG.posted)
					else:
						self.blocks.append((leftTG,rightTG))

	def output(self):
		idx = 1
		#print("  -----------oooooOOOOOooooo-----------")

		if self.rule != None:
			print(RAWU_FCYELLOW," (+) BetaNode for rule %s" % self.rule.label.capitalize(),RAWU_RESET)
		else:
			print(RAWU_FCYELLOW," (+) BetaNode ",RAWU_RESET)
		for bucket in self.buckets:
			print(RAWU_BOLD,"   (+) %d Bucket:" %(idx),RAWU_RESET)
			for key,tokengroup in bucket.items():
				tokengroup.output(4)
				#print(" "*4,str(tokengroup))
			idx += 1
		print(RAWU_BOLD,"   (+) Signals:",RAWU_RESET)
		for key,tokengroup in self.signals.items():
			if tokengroup.posted:
				tokengroup.output(4)
				#print(" "*4,str(tokengroup))
		if False:
			print(RAWU_BOLD,"  (+) Blockings:",RAWU_RESET)
			for block in self.blocks:
				print("   (X) Block")
				for tokengroup in block:
					tokengroup.output(5)
			#print("  -----------oooooOOOOOooooo-----------")
		print()

class AlphaNode:

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
		self.level = -1
		self.tag = tag
		self.key = label
		self.backup = None

	def backupBegin(self):
		self.backup = []
		for key,child in self.children.items():
			child.backupBegin()


	def unique(self,token,tag):
		if tag == "!":
			cutToken = token.cutOff(self.level)
			return [dtoken for key,dtoken in self.tokens.items() if cutToken.samePath(dtoken)]
		return []

	def removeToken3(self,token):
		flag = False
		if self.level < len(token.branches):
			if self.level == -1:
				flag = True
			elif self.alias != None:
				flag = token.addParam(self.alias,self.level)
			elif self.label == token.label(self.level):
				flag = True
			else:
				flag = False
		if not flag:
			deleteTokens = [dtoken for key,dtoken in self.tokens.items() if token.samePath(dtoken)]
			for dtoken in deleteTokens:
				self.__removeToken(dtoken)
		for key,child in self.children.items():
			child.removeToken(token)

	def removeToken(self,token):
		deleteTokens = [dtoken for key,dtoken in self.tokens.items() if token.samePath(dtoken)]

		for dtoken in deleteTokens:
			self.__removeToken(dtoken)
		for key,child in self.children.items():
			child.removeToken(token)
			unique = self.unique(token,child.tag)
			if len(unique)<=1: 
				for aToken in unique:
					self.tokens.pop(aToken.key)
					if child.alias != None:
						if aToken.addParam(child.alias,child.level):
							child.__addToken(aToken)
					else:
						child.__addToken(aToken)

	def removeToken2(self,token):
		deleteTokens = [dtoken for key,dtoken in self.tokens.items() if token.samePath(dtoken)]
		for dtoken in deleteTokens:
			self.__removeToken(dtoken)
		return deleteTokens

	def __removeToken(self,token):
		#print(token.key,self.tokens,self.level)
		self.tokens.pop(token.key)
		for (idx,beta) in self.betas:
			newTG = TokenGroup()
			newTG.addToken(token,idx)
			beta.removeTokenGroup(idx,newTG) 

	def __removeToken_addOn(self,token):
		for key,child in self.children.items():
			child.removeToken(token)
			unique = self.unique(token,child.tag)
			if len(unique)<=1: 
				for aToken in unique:
					self.tokens.pop(aToken.key)
					if child.alias != None:
						if aToken.addParam(child.alias,child.level):
							child.__addToken(aToken)
					else:
						child.__addToken(aToken)

	def hasToken(self,token):
		# Verifies that token has same Key as other tokens
		for key,otoken in self.tokens.items():
			#if token.label(self.level-1) != otoken.label(self.level-1) : 
			if token.label(self.level) != otoken.label(self.level): 
				return False
		return True

	def runBeta(self):
		for key,token in self.tokens.items():
			for (idx,beta) in self.betas:
				newTG = TokenGroup()
				newTG.addToken(token,idx)
				beta.addTokenGroup(idx,newTG) 


	def addToken(self,token):
		#Verifies that token path is not surpassed
		unqiue = []
		flag = False
		if self.level < len(token.branches):
			#print(self.level,len(token.branches))
			unique = self.unique(token,self.tag)
			if len(unique)>0:
				for dtoken in unique:
					self.__removeToken(dtoken)
			else:
				if self.alias != None:
					# If paramter node 
					# Adding any parameter to alias
					token = token.copy()
					if token.addParam(self.alias,self.level):
						self.__addToken(token)
						#flag = True
						return True,unique
				if self.level == -1:
					# Top node
					self.__addToken(token)
					#flag = True
					return True,unique
				if self.label == token.label(self.level):
					# Alternatively if key matches
					token = token.copy()
					self.__addToken(token)
					#flag = True
					return True,unique
		return flag,unique

	def __addToken(self,token):
		#Ensure that unique paths are unique
		#if self.tag == "!":
		#	cutToken = token.cuffOff(self.level)
		#	deletions = self.removeToken(cutToken)
		#	if len(deletions)>0: return deletions
		#Add token to token register
		#self.tokens[token.key]=token
		#Activate any beta nodes
		for (idx,beta) in self.betas:
			newTG = TokenGroup()
			newTG.addToken(token,idx)
			beta.addTokenGroup(idx,newTG) 
		#Add tokenss for any children
		added = False
		for key,child in self.children.items():
			#newtoken = token.copy()
			result,deleted = child.addToken(token)
			for delete in deleted:
				if child.alias != None and False:
					delete.params.pop(child.alias)
				self.tokens[delete.key]=delete
			added = added or result
		if not added:
			self.tokens[token.key]=token

	def __addToken2(self,token):
		#Ensure that unique paths are unique
		#if self.tag == "!":
		#	cutToken = token.cuffOff(self.level)
		#	deletions = self.removeToken(cutToken)
		#	if len(deletions)>0: return deletions
		#Add token to token register
		self.tokens[token.key]=token
		#Activate any beta nodes
		for (idx,beta) in self.betas:
			newTG = TokenGroup()
			newTG.addToken(token,idx)
			beta.addTokenGroup(idx,newTG) 
		#Add tokenss for any children
		added = False
		for key,child in self.children.items():
			child.addToken(token)

	def addToken2(self,token,adding=True,cutoff=None):
		#print(tokenkey,self.tokens)
		dublicate = token.copy()
		if self.tag == "!" and not self.hasToken(token):
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
			#We are not at the end - still branches to consider
			for key,child in self.children.items():
				token = dublicate.copy()
				# Central check: is there a match?
				if tokenkey == key:
					child.addToken(token,adding)
				# is there an Alias	
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
			child = AlphaNode(key,tag)
			parampattern = r'^([\[|\{\(]\w+[\]|\}\)])$'
			child.level = self.level+1
			if re.match(parampattern,key): child.alias=key[1:-1] #cuts front an back
			self.children[key] = child
			#print("adding",key)
			for key,token in self.tokens.items():
				child.addToken(token)
		if len(keys)>1:
			return child.addCondition(keys[1:])
		else:
			return child

	def output(self):
		print("\n Current Alpha Node Structure:")
		print(" -----------------------------")
		self.__output()

	def __output(self):
		output=""
		for key,token in self.tokens.items():
			output += str(token) + " "
		print(RAWU_FCYELLOW,"   "*self.level,"(+)",self.label,"  (tokens:",len(self.tokens),"outputs:",len(self.betas),"children:",len(self.children),")",RAWU_RESET)
		for key,token in self.tokens.items():
			print(RAWU_DIM,"   "*(self.level+1),"   -",str(token),str(token.params),RAWU_RESET)

		for (key,child) in self.children.items():
			child.__output()


class ReteEngine:

	def __init__(self):
		self.rules = []
		self.facts = []
		self.root = AlphaNode()
		self.facts = Node()
		self.betas = []
		self.conflictset = {}
		self.backup = []

	def backupBegin(self):
		self.backup = []

	def backupRevert(self):
		stepback = self.backup[::-1]
		for (cmd,path) in stepback:
			print(":::",cmd,path)
			if cmd == "add":
				self.addFact(path)
			if cmd == "remove":
				self.removeFact(path)
		self.backup=[]

	def addFact(self,fact):
		if debugging : print(RAWU_FCCYAN,"(+) Adding token:",fact,RAWU_RESET)
		cleanPath = fact.split("!")
		if len(cleanPath)>1:
			token = Token(cleanPath[0])
			self.root.removeToken(token)
			patterns = self.facts.match(cleanPath[0])
			#her skal vi har retur af deleted
			for pattern in patterns:
				self.backup.append(("add",pattern))
		token = Token(fact)
		self.facts.add(fact)
		self.root.addToken(token)
		self.backup.append(("remove",token.path))

	def removeFact(self,fact):
		if debugging : print(RAWU_FCMAGENTA,"(-) Removing token:",fact,RAWU_RESET)
		token = Token(fact)
		self.root.removeToken(token)
		self.facts.remove(fact)
		self.backup.append(("remove",token.path))

	def addRule(self,rule):
		#beta = BetaNode(rule)
		rule.rete = self
		self.conflictset[rule.label]={}
		conditions = []
		if debugging : print(RAWU_FCYELLOW,"(+) Added %d conditions for rule %s" %(len(rule.LHS),rule.label),RAWU_RESET)
		for path in rule.LHS:
			condition = self.addCondition(path)
			#beta.addsocket(condition)
			#condition.betas.append(beta)
			conditions.append((path,condition))
		self.rules.append(rule)
		#self.betas.append(beta)
		prev = conditions[0][1]
		level =0
		beta = BetaNode()
		beta.setNegation(0,conditions[0][0])
		for (path,condition) in conditions:
			if condition != conditions[0][1]:
				#beta = BetaNode()
				beta.setNegation(1,path)
				beta.level = level
				condition.betas.append((1,beta))
				prev.betas.append((0,beta))
				prev = beta
				self.betas.append(beta)
				rule.betas.append(beta)
				level += 1
				if condition != conditions[-1][1]: beta = BetaNode()
		if debugging : print(RAWU_DIM,"  (-) Added %d level(s) til rule %s" %(level,rule.label),RAWU_RESET)
		beta.rule = rule
		for (path,condition) in conditions:
			condition.runBeta()

	def addCondition(self,condition):
		pattern = r'([\.|\!|\^]?)([\[|\{|\()]?[\w|\*]+[\]|\}|\)]?)'
		keys = re.findall(pattern,condition)
		return self.root.addCondition(keys)

	def output(self):
		print(RAWU_FCYELLOW,"\n Rules in conflict set:")
		print(" ----------------------",RAWU_RESET)
		for rule,tokengroups in self.conflictset.items():
			print("  Rule: ",rule.capitalize())
			print(RAWU_DIM,end="")
			for key, tokengroup in tokengroups.items():
				tokengroup.output(4)
			print(RAWU_RESET,end="")
		if debugging:
			print("\n Rules:")
			print(" ----------------------")
			for rule in self.rules:
				rule.output()
		#for beta in self.betas:
		#	if beta.rule != None and 1==1 : beta.output()

	def fire(self,rulelabel,tokengroup):
		self.conflictset[rulelabel][tokengroup.key()]=tokengroup

	def revoke(self,rulelabel,tokengroup):
		tg = self.conflictset[rulelabel].get(tokengroup.key())
		if tg != None:		
			self.conflictset[rulelabel].pop(tokengroup.key())
