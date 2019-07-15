from rete import *
from rwutility import *


rete = ReteEngine()
"""
cnode = rete.addCondition("actors.[Player].gender.male")
rete.root.output()
rete.addFact("actors.bruce.gender.female")
rete.root.output()
rete.addFact("actors.peter.gender.male")
rete.root.output()
rete.addFact("actors.peter.age.65")
rete.root.output()
"""
#rete.addFact("actors.peter.gender.male")
#rete.root.output()
#rete.removeFact("actors.peter.gender")

#rete.root.output()

cls()

#print("rule added")

#print("fact added")
rete.addFact("actors.beata.noble.countess")
rete.addFact("actors.lucy.noble.countess")
rete.addFact("actors.beata.gender.female")
rete.addFact("actors.alice.gender.female")
#rete.output()
rete.addFact("actors.beata.age.33")
rete.addFact("actors.alice.age.11")
#rete.output()
#rete.addFact("actors.eliza.gender.female")
#rete.addFact("actors.eliza.age.33")
#rete.root.output()

#rete.addFact("actors!alice.age.46")
#rete.root.output()
rete.addFact("actors.lucy.gender.female")
#rete.output()

rete.addFact("actors.lucy.fighter")
rete.addFact("actors.lucy.age.22")
rete.addFact("actors.lucy.age.22")
rete.addFact("actors.lucy.age.22")

#rete.removeFact("actors.beata")
#rete.addFact("actors!rasmus")
#rete.addFact("actors.lucy.noble!baroness")
rule = Rule("Test Age",["actors.[Player].age.[Age]","actors.[Player].gender.female"])
rete.addRule(rule)
print("----")
rule = Rule("Test Fighter",["actors.[Player].gender.[female]","actors.[Player].fighter","actors.[Player].noble.[title]"])
rete.addRule(rule)
rete.addFact("actors!rasmus")

rete.output()

rete.root.output()

if 1==0:
	rete.addFact("actors.lucy.age.22")
	rete.root.output()
	rete.addFact("actors.lucy.gender.female")
	rete.addFact("actors.lucy.age.22")
	rete.root.output()
	#rete.addFact("actors!lucy.gender.female")
	#rete.addFact("actors.lucy.age.23")
	#rete.root.output()
	rete.addFact("locations.barn")
	rete.removeFact("actors.beata")
	rete.addFact("actors!Irvin")
	rete.root.output()
	rule = Rule("test",["locations.[Location]"])
	rete.addRule(rule)
	rete.root.output()
	#rule = Rule("test",["actors.[Player].gender.male","actors.[Player].age.[Age]"])
	#rete.addRule(rule)
#print("  -----------oooooOOOOOooooo-----------")
#rete.root.output()
#print("  -----------oooooOOOOOooooo-----------")

#rete.root.output()
