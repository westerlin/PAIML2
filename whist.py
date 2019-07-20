from node import *
from rulebase import *
from rwutility import *
import time


players = ["Albert","Beata","Christian","Doris"]

suits = ["Spades","Hearts","Clubs","Diamonds"]


cls()

ws = Node()
ws.addList(createRanking("cards_ranking.",cards_ranking))
ws.addList(createCycle("game.playorder.",players))
ws.addList(createList("game.players.",players))
ws.addList(createList("suits.",suits))
ws.addList(createList("ranks.",cards_ranking))
ws.addList(createList("",pronouns))
ws.addList(createDifference("difference.",players))

ws.add("game.players.Albert.gender!male")
ws.add("game.players.Beata.gender!female")
ws.add("game.players.Christian.gender!male")
ws.add("game.players.Doris.gender!female")
ws.add("game.state!init")
	
#ws.output()

ruleset = Rules(ws)
ruleset.players.append("Doris")

stage1 = Stage("Preparation",STAGES_EXECUTE_REACT_ORDER,"Game_starting")
stage2 = Stage("Game_starting",STAGES_EXECUTE_REACT_ORDER,"Card_Play")
stage3 = Stage("Card_Play",STAGES_EXECUTE_REACT_ORDER,"")

stage1.addRule("Building deck",
				[	
					"game.state!init",
					"suits.[suit]",
					"ranks.[rank]",
					"^game.deck.[suit].[rank]"
				],
				[
					("add","game.deck.[suit].[rank]"),
				])

stage2.addRule("Select sDealer",
				[
					"^game.dealer",
					"game.players?[dealer].gender.[gender]",
					"pronouns.[gender].subject.[sbj]",
					"game.playorder.[dealer].next.[first]"
				],[
					("text","[dealer] is selected as dealer. [sbj] starts shuffling the cards .. "),
					("add","game.dealer![dealer]"),
					("add","game.first![first]"),
					("add","game.state!dealing"),
				])

stage2.addRule("Initialise players hands",
				[
					"game.dealer",
					"game.players.[player]",
					"^game.cards.[player].card1"
				],[
					("add","game.cards.[player].card1!empty"),
					("add","game.cards.[player].card2!empty"),
					("add","game.cards.[player].card3!empty"),
					("add","game.cards.[player].card4!empty")
				])

stage3.addRule("Deal cards",
				[
					"game.players.[player]",
					"game.cards.[player].[slot]!empty",
					"game.deck?[suit]?[rank]"
				],[
					("add","game.cards.[player].[slot]![suit].[rank]"),
					("remove","game.deck.[suit].[rank]"),
				])

stage3.addRule("End of deal cards",
				[
					"game.cards.[player].[slot]",
					"game.state!dealing",
					"^game.cards.[player].[slot]!empty",
				],[
					("add","game.deck.[suit].[rank]"),
					("add","game.state!play_hand"),
				])

stage3.addRule("Game can start",
				[
					"game.state!play_hand",
					"game.first![player]",
				],[
					("text","All cards was dealt. [player] has the first turn."),
					("add","game.state!playing"),
				])

ruleset.addStage(stage1)
ruleset.addStage(stage2)
ruleset.addStage(stage3)

print("Welcome to the Whist card game... \n")

flag = "Preparation"
while flag!="":
	flag = ruleset.execute(flag)
	time.sleep(.45)

print("\ngame ended ...bye for now")

#ws.output()
#game = ws.get("game.cards")
#game.output()