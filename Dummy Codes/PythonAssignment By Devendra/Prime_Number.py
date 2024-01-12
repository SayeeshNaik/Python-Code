count = 0
number = int(input('Enter a Number : '))
for i in range(2,11):
    if(number % i == 0):
        count+=1
if(count == 1):
    print("Prime Number")
else :
    print("Not Prime Number")