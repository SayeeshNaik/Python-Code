text = input("Enter a text : ")
u_count = 0
l_count = 0
u_case = []
l_case = []
for i in range(len(text)):
    asc_value = ord(text[i])
    if(asc_value >=65 and asc_value <=90):
        u_case.append(text[i])
        u_count+=1
    if(asc_value >= 97 and asc_value <=122):
        l_case.append(text[i])
        l_count+=1
print("UpperCase = ",u_count,"\n",u_case)
print("LowerCase = ",l_count,"\n",l_case)