lis=[]
dup=[]
prime=[]
print("********** PRIME NUMBER **********")
initial = int(input("Starting : "))
final = int(input("Final : "))

for i in range(initial, final):
    lis.append(i)
    for j in range(2,10):
        if(i%j==0):
            dup.append(i)

lis=list(set(lis))
dup=list(set(dup))

for i in dup:
    lis.remove(i)
if(1 in lis):lis.remove(1)
test = [2,3,5,7]
if(initial<=10):
    [prime.append(i) for i in test if(i>=initial)]
    prime.extend(lis)
    print("\nPrime Num : ",prime)
else:
  print("\nPrime Num : ",lis)