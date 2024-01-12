import json

file = open("MyntraPDP_Json.txt",'r')
data = json.loads(file.read())
print(data)
file.close()