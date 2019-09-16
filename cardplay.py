from node import *
from rulebase import *


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

"""
ruleset.addRule([	"game.turn![ACTOR]",
					"game.leader![ACTOR]",
					"game.state!playing_hand"
					],[
					 ("text","New round!")
					],"New round"
					)
"""




ruleset.addRule("Discarding",
				[	
					"game.turn![ACTOR]![Y]![Z]",
					"game.players.[ACTOR].cards.[suit].[rank]",
					"game.state!playing_hand",
					"^game.lead.[suit]",
					"game.rounds.[T1].[T2].[T3].[T4]",
					"^game.trumph.[suit]"
				],
				[
					("text","\t[ACTOR] cannot answer color and discards [rank] of [suit]"),
					 ("add","game.turn![Y]![Z]![ACTOR]"),
					 ("add","game.rounds![T2]![T3]![T4]![T1]"),
					 ("remove","game.players.[ACTOR].cards.[suit].[rank]"),
					 ("add","game.deck.[suit].[rank]")
				],False,
				"Discard [rank] of [suit]")

ruleset.addRule("Playing Color",
				[	
					"game.turn![ACTOR]![Y]![Z]",
					"game.players.[ACTOR].cards.[suit].[rank]",
					"game.state!playing_hand",
					"game.rounds.[T1].[T2].[T3].[T4]",
					"game.lead.[suit]",
					"^game.trumph.[suit]"
				],
				[
					("text","\t[ACTOR] is playing her [rank] of [suit]"),
					("add","game.turn![Y]![Z]![ACTOR]"),
					("add","game.rounds![T2]![T3]![T4]![T1]"),
					("remove","game.players.[ACTOR].cards.[suit].[rank]"),
					("add","game.deck.[suit].[rank]")
				],False,
				"Match color playing [rank] of [suit]")

ruleset.addRule("Playing Trumph",
				[	
					"game.turn![ACTOR]![Y]![Z]",
					"game.players.[ACTOR].cards.[suit].[rank]",
					"game.rounds.[T1].[T2].[T3].[T4]",
					"game.trumph.[suit]",
					"game.state!playing_hand"
				],
				[
					("text","\t[ACTOR] is trumphing with [rank] of [suit]"),
					("add","game.turn![Y]![Z]![ACTOR]"),
					("remove","game.players.[ACTOR].cards.[suit].[rank]"),
					("add","game.rounds![T2]![T3]![T4]![T1]"),
					("add","game.deck.[suit].[rank]")
				],False,
				"Trumph with [rank] of [suit]")

ruleset.addRule("Dealing card to player",
					[	
					"game.deck.[suit].[rank]",
					"game.state!dealing",
					"game.hands.[X].[A1]!None"],
					[
					 ("remove","game.deck.[suit].[rank]"),
					 ("add","game.players.[X].cards.[suit].[rank]"),
					 ("add","game.hands.[X].[A1]!OK")
					])

ruleset.addRule( "Card play is ended",
				[	
					"game.state!playing_hand",
					"game.players.Lucy.cards!empty",
					"game.players.Daisy.cards!empty",
					"game.players.Alice.cards!empty"
				],
				[
					 ("text","No more cards to play .. game ends .. "),
					 ("add","game.state!end_of_play")
				])

ruleset.addRule("Player received cards",
				[	
					"game.state!dealing",
					"game.hands.[X].card1!OK",
					"game.hands.[X].card2!OK",
					"game.hands.[X].card3!OK",
					"game.hands.[X].card4!OK"
				],
				[
					 ("add","game.hands.[X]!cards")
				])

ruleset.addRule("End of Round",
				[
					"game.state!playing_hand",
					"game.rounds!1!0!0!0"],
				[
					("add","game.state!newround")
				])

ruleset.addRule("New Round",
				[
					"^game.hands.[X].cards!empty",
					"game.state!newround",
					"game.deck.[suit].[rank]"
				],
				[	("text","\n\tNew Round! Current color is [suit]"),
					("remove","game.deck.[suit].[rank]"),
					("add","game.lead![suit].[rank]"),
					("add","game.rounds!0!0!0!1"),
					("add","game.state!playing_hand")
				])

ruleset.addRule("First card played",
				[	"game.state!first_card",
				],
				[
					 ("add","game.state!newround"),
					 ("add","game.leader!Alice")
				])

ruleset.addRule("Begin game",
				[	
					"game.state!dealing",
					"game.hands.Daisy!cards",
					"game.hands.Lucy!cards",
					"game.hands.Alice!cards",
					"game.deck.[suit].[rank]",
				],
				[
					("text","Cards was dealt .. game can start"),
					("text","[suit] was selected trumph.."),
					("add","game.trumph.[suit]"),
					("remove","game.deck.[suit].[rank]"),
					("add","game.state!first_card"),
					("remove","game.hands")
				])


ruleset.addRule("Building deck",
				[	
					"game.state!init",
					"cards.[suit]",
					"ranks.[rank]"
				],
				[
					("add","game.deck.[suit].[rank]")
				])

ruleset.addRule("Setting player hands empty",
				[	
					"game.state!init","game.players.[player]"
				],
				[
					("add","game.hands.[player].card1!None"),
					("add","game.hands.[player].card2!None"),
					("add","game.hands.[player].card3!None"),
					("add","game.hands.[player].card4!None"),
					("add","game.players.[player].cards.empty")
				])

ruleset.addRule("Prepare for dealing cards",
				[	
					"game.hands.Alice.card1!None",
					"game.hands.Daisy.card1!None",
					"game.hands.Lucy.card1!None"
				],
				[
					("add","game.state!dealing"),
					("add","game.dealer.Daisy"),
					("add","tech.go!0"),
					("add","tech.stop!1"),
					("add","game.leader.empty")
				])


ruleset.players.append("Alice")

userinput = Userinput()
ptn=''
"""ptn!=rw_ENTER and"""
flag = True
while ptn!=rw_ESC and flag:
	flag = ruleset.execute_base()
	if flag:
		ptn = userinput.get()

print("game ended ...")

