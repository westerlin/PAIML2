from drama import *
from rete import *

drama = Drama()

schema0 = Schema("main")
schema1 = Schema("calc")
schema2 = Schema("common")

rule = Rule("Noble Fighter",
			[
				"actors.[Player].gender![Gender]",
				"^actors.[Player].class.rogue",
				"actors.[Player].noble![Title]"
			]
			)
schema0.addRule(rule)
schema2.addRule(rule)

rule = Rule("Women of age",
			[	
				"actors.[Player].gender!female",
				"actors.[Player].age![Age]"
			]
			)

schema1.addRule(rule)
schema2.addRule(rule)

drama.addSchema(schema0)
drama.addSchema(schema1)
drama.addSchema(schema2)

drama.addFact("actors.beata.noble!countess")
drama.addFact("actors.lucy.noble!countess")
drama.addFact("actors.alice.noble!baroness")
drama.addFact("actors.beata.gender.female")
drama.addFact("actors.alice.gender.female")
drama.addFact("actors.beata.age.33")
drama.addFact("actors.alice.age.11")
drama.addFact("actors.lucy.gender.female")
drama.addFact("actors.beata.class.warrior")
drama.addFact("actors.alice.class.babarian")
drama.addFact("actors.lucy.class.priest")
drama.addFact("actors.lucy.class!ranger")
drama.addFact("actors.lucy.age.22")
drama.addFact("actors.lucy.age.21")
drama.addFact("actors.lucy.age!34")
drama.addFact("actors.beata.noble!queen")
drama.addFact("actors.beata.noble.beggar")
drama.addFact("actors.beata.noble.sire")
drama.addFact("actors.beata.noble!emporess")


#print("MAIN:")
#drama.execute("main")
#print("CALC:")
#drama.execute("calc")
print("COMMON:")
drama.execute("common")
