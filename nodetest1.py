from node import *
import copy



ws = Node()

ws.add("Singleton.In_the_world")

bk = copy.deepcopy(ws)

bk.add("Sovereign.King")
bk.add("Singleton.Start_of_universe")

#bk.output()
#ws.output()

test = ".sdasd.[sd].asdsad"
print(isUniquePath(test))
print(isVarPath(test))

print(Capitalize("der var engang. en tekst med smaa bogstaver! som skulle gores store."))