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


rule = Rule("Noble Fighter",["actors.[Player].gender![Gender]","^actors.[Player].class.rogue","actors.[Player].noble![Title]"])
#rule = Rule("Noble Fighter",["actors.[Player].gender.[Gender]","actors.[Player].noble![Title]"])
rete.addRule(rule)

rule = Rule("Ageing Woman",["actors.[Player].gender!female","actors.[Player].age![Age]"])
rete.addRule(rule)

rete.addFact("actors.beata.noble!countess")
rete.addFact("actors.lucy.noble!countess")
rete.addFact("actors.alice.noble!baroness")
#rete.backupBegin()
rete.addFact("actors.beata.gender.female")
rete.backupBegin()
rete.addFact("actors.alice.gender.female")
rete.addFact("actors.beata.age.33")
rete.addFact("actors.alice.age.11")
rete.addFact("actors.lucy.gender.female")
rete.backupBegin()
rete.addFact("actors.beata.class.warrior")
rete.addFact("actors.alice.class.babarian")
rete.backupBegin()
rete.addFact("actors.lucy.class.priest")
rete.addFact("actors.lucy.age.22")
rete.addFact("actors.lucy.age.21")
rete.removeFact("actors.lucy.age.22")
rete.backupBegin()
rete.addFact("actors.beata.noble!queen")
rete.backupBegin()
rete.addFact("actors.beata.noble.beggar")
rete.addFact("actors.beata.noble.sire")
rete.addFact("actors.beata.noble!emporess")
#print(rete.backup)
#rete.backupRevert()

#rule = Rule("Test Fighter",["actors.[Player].gender.[Gender]","^actors.[Player].class.rogue","actors.[Player].noble![Title]"])
#rete.addRule(rule)

#rete.removeFact("actors.beata.noble.queen")
#rete.removeFact("actors.beata.noble")

"""
rete.addFact("actors.beata.noble!queen")
rete.removeFact("actors.beata.noble")
rete.addFact("actors.beata.noble.emporess")
"""
#rule = Rule("Test Fighter",["actors.[Player].gender.[Gender]","^actors.[Player].class.rogue","actors.[Player].noble.[Title]"])
#rete.addRule(rule)

rete.output()
rete.root.output()

#print(rete.backup)

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

