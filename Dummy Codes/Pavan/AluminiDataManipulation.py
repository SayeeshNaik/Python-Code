import json

file = "C:/Users/SaishNaik/Downloads/alumnidataexport.json"

with open(file,'r') as file_data:
    data = list(json.loads(file_data.read()))
    
key_names = ['A_Name','A_Occupation']
value_counts = {}
output_data = {}

for key in key_names:
    for item in data:
        value = item[key]
        try:
            if value in value_counts:
                value_counts[value] += 1
            else:
                value_counts[value] = 1
        except: pass
    output_data[key] = value_counts
    value_counts ={}

print(output_data)