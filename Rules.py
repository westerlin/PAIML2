from node import *
from rwutility import *


def zipzap(dic1,dic2):
	for key,obj in dic2.items():
		dest = dic1.get(key)
		if dest != None:
			dest+=obj
		else:
			dic1[key] = obj
	return dic1

class Rule:

	def __init__(self,LHS=[],RHS=[]):
		self.LHS = LHS
		self.RHS = RHS

	def __repr__(self):
		return "\n"+str(self.LHS)

	def isActive(self,assertions):
		for condition in self.LHS:
			node = assertions.get(condition)
			if node == None : 
				return False
		return True

	def execute(self,assertions):
		for cmd,impact in self.RHS:
			if cmd == "add":
				assertions.add(impact)
			elif cmd == "remove":
				assertions.delete(impact)
			elif cmd == "text":
				print("\t"*2,impact,"\n")
			else:
				print("Error - unknow command:",cmd,"(",impact,")")

class Generic:

	def __init__(self,LHS=[],RHS=[]):
		self.LHS = LHS
		self.RHS = RHS


	def spawnrules(self,assertions):
		scenes=[{}]
		for condition in self.LHS:
			scenes = assertions.combi(condition,scenes)

		if scenes == {} : return {"all":[Rule(self.LHS,self.RHS)]}

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
				output[label]=[Rule(LHS,RHS)]
			else:
				output[label].append(Rule(LHS,RHS))

		return output

class Rules:

	def __init__(self,assertions):
		self.ws=assertions
		self.generics = []

	def execute(self):
		rules = {}
		for generic in self.generics:
			rules = zipzap(rules,generic.spawnrules(self.ws))
		output = False
		conflict_set = [rule for rule in rules["all"] if rule.isActive(self.ws)]

		"""
		if conflict_set != []:
			rule = random.choice(conflict_set)
		else:
			rule = None

		while rule != None:
			output = True
			rule.execute(self.ws)
			#conflict_set.remove(rule)
			conflict_set = [rule for rule in conflict_set if rule.isActive(self.ws)]
			print(len(conflict_set))
			print(self.ws.get("rule.*"))
			print(self.ws.get("game.hands.Daisy.*"))
			if conflict_set != []:
				rule = random.choice(conflict_set)
			else:
				rule = None
		"""
		#print(conflict_set)
		random.shuffle(conflict_set)
		for rule in conflict_set:
			if rule.isActive(self.ws):
				#print(rule)
				rule.execute(self.ws)
				output = True
			else:
				pass
				#print(rule)
				#print(self.ws.get("rule.*"))
				#print(self.ws.get("game.hands.Daisy.*"))

		rules.pop("all")
		for key,obj in rules.items():
			affordances = [rule for rule in obj if rule.isActive(self.ws)]
			if affordances != []:
				output=True
				act = random.choice(affordances)
				act.execute(self.ws)
		return output

	def addRule(self,precs, posts):
		newrule = Generic(LHS=precs,RHS=posts)
		self.generics.append(newrule)

ontology = Node()

cards = ontology.add("cards")
cards.add("Spades")
cards.add("Hearts")
cards.add("Clubs")
cards.add("Diamonds")
ranks = ontology.add("ranks")
ranks.add("One")
ranks.add("Two")
ranks.add("Three")
ranks.add("Four")
ranks.add("Fives")
ranks.add("Sixes")
ranks.add("Seven")
ranks.add("Eight")
ranks.add("Nine")
ranks.add("Ten")
ranks.add("Jack")
ranks.add("Queen")
ranks.add("King")
ranks.add("Ace")
game = ontology.add("game")
game.add("state!init")
alice = game.add("players.Alice")
#alice.add("cards.hearts.I1")
#alice.add("cards.clubs.I8")
#alice.add("cards.clubs.King")
lucy = game.add("players.Lucy")
#lucy.add("cards.spades.5")
#lucy.add("cards.hearts.8")
#lucy.add("cards.diamonds.Queen")
Daisy = game.add("players.Daisy")
#Daisy.add("cards.spades.5")
#Daisy.add("cards.hearts.8")
#Daisy.add("cards.diamonds.Queen")
game.add("turn!Alice.Lucy.Daisy")


#ontology.output()

ruleset = Rules(ontology)
#ruleset.addRule(["cards.[suit]"],[("text","playing [suit]")])

cls()

ruleset.addRule([	"game.turn![ACTOR]![Y]![Z]",
					"game.players.[ACTOR].cards.[suit].[rank]",
					"game.state!playing_hand"],
					[("text","[ACTOR] is playing her [rank] of [suit]"),
					 ("add","game.turn![Y]![Z]![ACTOR]"),
					 ("remove","game.players.[ACTOR].cards.[suit].[rank]"),
					 ("add","game.deck.[suit].[rank]"),
					 ("add","rule!play_hands")])

ruleset.addRule([	
					"game.deck.[suit].[rank]","game.state!dealing",
					"game.hands.[X]![A1]![A2]![A3]![A4]![A5]",
					"game.dealcode.[A1]","game.dealer.[Y]"],
					[("text","[Y] dealt a card to [X] .. "),
					 ("remove","game.deck.[suit].[rank]"),
					 ("add","game.players.[X].cards.[suit].[rank]"),
					 ("add","game.hands.[X]![A2]![A3]![A4]![A5]![A1]"),("add","rule!receive_cards")])
"""

ruleset.addRule([	"game.dealer.[ACTOR]", "game.turn![X]![Y]![Z]"
					,"game.deck.[suit].[rank]","game.state!dealing",
					"game.hands.[player]![A1]![A2]![A3]![A4]![A5]",
					"game.dealcode.[A1]"],
					[("text","[ACTOR] deals a card to [X]"),
					 ("remove","game.deck.[suit].[rank]"),
					 ("add","game.turn![Y]![Z]![X]"),
					 ("add","game.players.[X].cards.[suit].[rank]"),
					 ("add","game.hands.[player]![A2]![A3]![A4]![A5]![A1]")])
"""
ruleset.addRule([	"game.state!dealing",
					"game.hands.Daisy![A1]",
					"game.hands.Lucy![A1]",
					"game.hands.Alice![A1]",
					"game.endcode.[A1]"],
					[("text","Cards was dealt .. game can start"),
					 ("remove","game.deck"),
					 ("add","game.state!playing_hand"),
					 ("add","rule!game_begin"),
					 ("remove","game.hands")])


ruleset.addRule([	"game.state!init","cards.[suit]","ranks.[rank]"],
					[("add","game.deck.[suit].[rank]"),("add","rule!build_deck")])

ruleset.addRule([	"game.state!init","game.players.[player]"],
					[("add","game.hands.[player].0.0.0.0.1"),("add","rule!init_game_hands")])

ruleset.addRule([	"game.state!init"],
					[("text","A new deck of cards was opened")])

ruleset.addRule([	"game.hands.Alice.0.0.0.0.1","game.hands.Daisy.0.0.0.0.1","game.hands.Lucy.0.0.0.0.1"],
					[("text","Daisy was shuffling the cards ... "),
					 ("add","game.state!dealing"),("add","game.dealer.Daisy"),
					 ("add","game.endcode.1"),("add","game.dealcode.0"),("add","rule!setting_dealing")
					 ])

userinput = Userinput()
ptn=''
"""ptn!=rw_ENTER and"""
flag = True
while ptn!=rw_ESC and flag:
	flag = ruleset.execute()
	if flag:
		ptn = userinput.get()
print("game ended ...")

#print(ontology.combi("game.players?[X]"))
#print(ontology.get("game.players.*"))
ontology.output()