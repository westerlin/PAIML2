import node

worldstate = node.Node()

worldstate.add("actors.brown.trait.generous")
worldstate.add("actors.brown.trait.provoking")
worldstate.add("actors.brown.trait.conservative")
worldstate.add("actors.lucy.trait.humourous")
worldstate.add("actors.lucy.trait.forgiving")
worldstate.add("actors.peter.trait.humourous")

worldstate.add("actors.peter.handsome")

worldstate.add("actors.lucy.trait.flirty")
worldstate.add("practice.conversation.tell_joke")
worldstate.add("practice.conversation.lucy.flirt.peter")
worldstate.add("practice.donation.lucy.donate_hugely")
worldstate.add("practice.donation.brown.donate_hugely")
worldstate.add("practice.conversation.brown.talkdown.lucy")

#worldstate.output()
#print(worldstate.combi("actors.[ACTORS]"))
#print(worldstate.combi("actors.brown"))
#print(len(worldstate.combi("practice.conversation.tell_joke",[{}])))

rule1 = {"if":[	
				"practice.conversation.tell_joke",
				"actors.[ACTOR].trait.humourous"
				],
		"then":[("add","actors.[ACTOR].emotions.happy.tell_joke")]
		}

rule2 = {"if":[	
				"actors.[OTHER].handsome",
				"practice.conversation.[ACTOR].flirt.[OTHER]",
				"actors.[ACTOR].trait.flirty"
				],
		"then":[("add","actors.[ACTOR].emotions.happy.flirting")]
		}

rule3 = {"if":[	
				"practice.conversation.[ONE].flirt.[ANOTHER]",
				"actors.[ACTOR].trait.conservative"
				],
		"then":[	("add","actors.[ACTOR].emotions.judgemental.flirting"),
					("add","actors.[ACTOR].relations.[ONE].dislikes.is_flirty")
					]
		}

rule4 = {"if":[	
				"practice.donation.[ACTOR].donate_hugely",
				"actors.[ACTOR].trait.generous"
				],
		"then":[	
				("add","actors.[ACTOR].emotions.happy.donation"),
					]
		}

rule5 = {"if":[	
				"practice.conversation.[ACTOR].talkdown.[OTHER]",
				"actors.[ACTOR].relations.[OHTER].dislikes.[REASON]"
				],
		"then":[	
				("add","actors.[ACTOR].emotions.happy.talkdown.[OTHER].[REASON]"),
					]
		}

rule6 = {"if":[	
				"practice.conversation.[OTHER].talkdown.[ACTOR]",
				"^actors.[ACTOR].trait.forgiving"
				],
		"then":[	
				("add","actors.[ACTOR].relations.[OTHER].dislikes.talkdownto"),
					]
		}


rule6 = {"if":[	
				"actors.[ACTOR]",
				"actors.[OTHER]"
				],
		"then":[	
				("add","emotions.[ACTOR].likes.[OTHER]"),
					]
		}

def evaluate(rule,ws):
	contextes = [{}]
	for sentence in rule["if"]:
		if sentence[0] == "^":
			rs = ws.combi(sentence[1:],contextes)
			if len(rs) != 0 : return "Rule was not fired because '"+sentence+"' was false"
		else:
			rs = ws.combi(sentence,contextes)
			if len(rs) == 0 : return "Rule was not fired because '"+sentence+"' was false"
			contextes = rs
	fire = 0
	for context in contextes:
		for subaction in rule["then"]:
			if subaction[0] == "add":
				newSentence = node.populate(subaction[1],context)
				print("Adding:",newSentence)
				ws.add(newSentence)
				fire += 1
	return "Rule was fired %d!" %fire

print(evaluate(rule1,worldstate))
print(evaluate(rule2,worldstate))
print(evaluate(rule3,worldstate))
print(evaluate(rule4,worldstate))
print(evaluate(rule5,worldstate))
#worldstate.backup=[]
print(evaluate(rule6,worldstate))
worldstate.output(["emotions","beliefs","relations"])

"""

worldstate.backupRevert()
#worldstate.delete("emotions")
worldstate.output()

worldstate.add("delta.test.test.butter.cheese")
worldstate.add("delta.test.test.butter!ketchup")
worldstate.add("delta.test.test.bread")
worldstate.backup()
worldstate.remove("delta.test.test.bread")
worldstate.add("delta.test.test.bread")
worldstate.remove("delta.test.test.bread")
worldstate.output()
worldstate.backupRevert()
worldstate.output()
worldstate.add("delta.nothing")
node = worldstate.get("delta.nothing")
node.add("mountains.hills.tops")
print(node.undoRegister)
print(worldstate.undoRegister)
worldstate.output()
worldstate.backupRevert()
worldstate.output()
print("testing reference")
my1 = ["test","plob"]
my2 = my1
my2.append("klk")
my1.append("2klk")
print(my1)
print(my2)
"""