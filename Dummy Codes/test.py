lis = [1,'sayeesh',23,'yatish',11.6,'subbu',0]
string,num,num2 = [],[],[]
[string.append(i) if type(i)==int else num2.append(i) if type(i)==str else num.append(i) for i in lis]
print(string)
print(num)
print(num2)