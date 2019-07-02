# Exclamaition in Nodes

import re


pattern = r'([\.|\!]?)([\[|\{|\()]?\w+[\]|\}|\)]?)'
text = "actors.[ACTOR].gender!female"

match = re.findall(pattern,text)

print(match)