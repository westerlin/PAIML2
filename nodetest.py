# testing node
import rwutility as rwu
from node import *


rwu.cls()

myworld = Node()

node = myworld.add("actors.lydia")
node.add("gender.female")
node.add("age.27")
node.add("profession.priestess")
node = myworld.add("actors.ophelia")
node.add("gender.female")
node.add("age.42")
node.add("profession.domina")
node = myworld.add("actors.marcus")
node.add("gender.male")
node.add("age.23")
node.add("profession.centurion")

myworld.add("locations.old_barn.lydia")
myworld.add("locations.old_barn.marcus")
myworld.add("locations.old_mill.ophelia")

myworld.output()

scenes1 = myworld.combi("actors.[actors]")
print(scenes1)
scenes1 = myworld.combi("actors.[actors].gender.female",scenes1)
print(scenes1)
print(myworld.combi("locations.[location].[actors]",scenes1))
scenes2 = myworld.combi("actors.[actors]")
print(scenes2)
scenes2 = myworld.combi("locations.old_barn.[actors]",scenes2)
print(scenes2)

print(myworld.get("actors.lydia"))
print(myworld.get("actors!lydia"))
print(myworld.get("actors.lydia.gender!female"))
myworld.add("actors.lydia.gender!male")
myworld.output()


myworld.add("actors!alfred")
scenes1 = myworld.combi("actors.[actors]")
print(scenes1)
scenes1 = myworld.combi("actors![actors]")
print(scenes1)
