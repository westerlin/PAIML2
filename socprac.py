# TEsting social practices

from social_practice import *
from node import *
from rwutility import *

world = Node()
world.add("practices.meeting!start")
node = world.add("actors.brown")
node.add("gender!male")
node.add("mood!calm")
node.add("age!22")
node = world.add("actors.lucy")
node.add("gender!female")
node.add("age!25")


practice = SocialPractice(world,{"SELF":"practices.meeting","brown":"Mr. Brown","lucy":"Young fair Lucy"})

action = Action()
action.precs = ["actors.[AGENT].gender!female","actors.[OTHER].mood!calm","[SELF]!start"]
action.post = [("text","[[AGENT]] says 'Hello [[OTHER]]'"),("add","actors.[OTHER].mood!surprised"),("add","[SELF].norm!response_greet![OTHER]"),
("add","[SELF].respond")]
practice.actions["Greet"] = action

action = Action()
action.precs = ["actors.[AGENT].mood!surprised","[SELF].norm!response_greet![OTHER]"]
action.post = [("text","[[AGENT]] looks surprised .. "),("text","Suddenly it seems as if [[AGENT]] remembers something.\n\t He smiles gently ... "),("add","actors.[AGENT].mood!calm")]
practice.actions["Surprised"] = action

action = Action()
action.precs = ["actors.[AGENT].mood!calm","[SELF].norm!response_greet![AGENT]"]
action.post = [("text","[[AGENT]] says 'Hello there, mrs ..?? ' "),("add","[SELF].norm!name_is")]
practice.actions["Greet_back"] = action

action = Action()
action.precs = ["actors.[AGENT].gender!female","[SELF].norm!name_is"]
action.post = [("text","Well hello there. I am [[AGENT]] ' "),("add","[SELF].norm!embarressed")]
practice.actions["RememberName"] = action

action = Action()
action.precs = ["actors.[AGENT].gender!female","[SELF].norm!name_is"]
action.post = [("text","[AGENT] looks quite disappointed ...  ' "),("add","[SELF].norm!disappointed")]
practice.actions["Disappointed"] = action


cls()
print ("------------- ooooOOOOoooo -------------")
world.output()
print ("------------- ooooOOOOoooo -------------")
userinput = Userinput()
ptn=''
"""ptn!=rw_ENTER and"""
flag = True
while ptn!=rw_ESC and flag:
	flag = practice.progress()
	ptn = userinput.get()
	#print ("------------- ooooOOOOoooo -------------")
	#world.output()
	#print ("------------- ooooOOOOoooo -------------")
	#if ptn not in rw_SPECIALS:
print ("------------- ooooOOOOoooo -------------")
world.output()
print ("------------- ooooOOOOoooo -------------")




"""
tests = [("text","Hello world")]
for tuplee in action.post:
	print(key)
"""

