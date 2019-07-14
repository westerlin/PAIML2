from node import *
from rulebase import *
from rwutility import *

players = ["Rachel","Boris","Ursula","Lola"]

cls()

ws = Node()
ws = createRanking(ws,"cards.",cards_ranking)
ws = createCycle(ws,"game.play_order.",players)
ws = createList(ws,"game.players.",players)
ws = createList(ws,"",pronouns)
ws = createDifference(ws,"difference.",players)

ws.add("game.players.Rachel.gender!female")
ws.add("game.players.Boris.gender!male")
ws.add("game.players.Ursula.gender!female")
ws.add("game.players.Lola.gender!female")
	
#ws.output()

ruleset = Rules(ws)
ruleset.players.append("Boris")

ruleset.addRule("Ignore it",

				[
					"game.state!play",
				 	"game.turn![X]",
				 	"difference.[X].[ACTOR]",
				 	"norms.[X].normbreaking.[ACTOR]",
				 	"[ACTOR].beliefs.[X]!is_arrogant",
				 	"^norms.[X].normbreaking.[ACTOR].retribution",
				],
				[
					("text","[ACTOR] grumbles .... '"),
					("add","norms.[X].normbreaking.[ACTOR].retribution")
				],False,
				"Cool down and refrain from retribute [X]"
				)

ruleset.addRule("Pre-expectations",

				[
					"game.state!play",
				 	"game.turn![X]",
				 	"difference.[X].[ACTOR]",
				 	"norms.[X].normbreaking.[ACTOR]",
				 	"[ACTOR].beliefs.[X]!is_arrogant",
				 	"^norms.[X].normbreaking.[ACTOR].retribution",
				],
				[
					("text","[ACTOR] sniffs 'Well, lets see if [X] has time for participating this round.'"),
					("add","norms.[X].normbreaking.[ACTOR].retribution")
				],False,
				"Make a retributing remark to [X]")

ruleset.addRule("evaluate-normbreaking-slow",
				[
					"norms.[X]!normbreaking",
				 	"game.players.[ACTOR]",
				 	"difference.[X].[ACTOR]",
				 	"^norms.[X].normbreaking.[ACTOR]",
				],
				[
					("text","[ACTOR] looks forgiving at [X]"),
					("add","[ACTOR].beliefs.[X]!is_slow"),
					("add","norms.[X].normbreaking.[ACTOR]")
				],False,
				"Evaluate [X]'s action as slight lack of focus"
	)


ruleset.addRule("evaluate-normbreaking-arrogant",
				[
					"norms.[X]!normbreaking",
				 	"game.players.[ACTOR]",
				 	"difference.[X].[ACTOR]",
				 	"^norms.[X].normbreaking.[ACTOR]",
				],
				[
					("text","[ACTOR] looks anoyed at [X]"),
					("add","[ACTOR].beliefs.[X]!is_arrogant"),
					("add","norms.[X].normbreaking.[ACTOR]")
				],False,
				"Evaluate [X]'s action as clear sign of arrogance"
	)


ruleset.addRule("Think about beliefs",

				[
					"game.state!play",
				 	"game.turn![ACTOR]",
				 	"[ACTOR].beliefs.[X]![belief]",
				 	"game.players.[ACTOR].gender![GENDER]",
				],
				[
					("text","[ACTOR] thins about [X]"),
				],False,
				"Thinks about [X] is [belief]")

ruleset.addRule("Norm-breaker",

				[
					"game.state!play",
					"game.play_order.[ACTOR].next.[Y]",
				 	"game.turn![ACTOR]",
				 	"game.players.[ACTOR].gender![GENDER]",
				],
				[
					("text","[ACTOR] looks the other way"),
					("add","norms.[ACTOR].normbreaking")
				],False,
				"Look the other way")

ruleset.addRule("Turn-taking",

				[
					"game.state!play",
					"game.play_order.[ACTOR].next.[Y]",
				 	"game.turn![ACTOR]",
				 	"game.players.[ACTOR].gender![GENDER]",
				 	"pronouns.[GENDER].adjective![pronoun]"
				],
				[
					("text","[ACTOR] takes [pronoun] turn"),
					("add","game.turn![Y]"),
					("remove","norms.[ACTOR].normbreaking")
				],False,
				"Take your turn")

ruleset.addRule("Initialise",
				[
					"^game.state!play",
					"game.players?[first_player]"
				],
				[
					("text","A new game is starting. [first_player] has the first move... "),
					("add","game.state!play"),
					("add","game.turn![first_player]")
				],False)


"""ptn!=rw_ENTER and"""
"""
userinput = Userinput()
ptn=''
flag = True
while ptn!=rw_ESC and flag:
	flag = ruleset.execute()
	if flag:
		ptn = userinput.get()
"""
import time

flag = True
while flag:
	flag = ruleset.execute()
	time.sleep(.25)

print("game ended ...")
scenes = [{}]



"""
ws.add("game.turn!Boris")

rules = [
					"game.play_order.[ACTOR].next.[Y]",
				 	"game.turn![ACTOR]",
				 	"game.players.[ACTOR].npc",
				 	"game.players.[ACTOR].gender![GENDER]",
				 	"pronouns.[GENDER].possesive![pronoun]"
				]
for rule in rules:
	scenes = ws.combi(rule,scenes)
for scene in scenes:
	print(scene)
"""
#scenes = ws.combi("game.play_order.[ACTOR].next.[Y]",scenes)
#print(scenes)
#scenes = ws.combi("game.turn.[ACTOR]",scenes)
#print(scenes)
#scenes = ws.combi("game.players.[ACTOR].npc",scenes)
#print(scenes)
