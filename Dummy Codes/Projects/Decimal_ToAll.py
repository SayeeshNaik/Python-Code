num = int(input("Decimal Number : "))
lst = []
rem = int(num % 2)
rem = str(rem)
lst.append(rem)
ans = int(num / 2)

for i in range(ans):
    if(ans>0):
        rem = int(ans % 2)
        rem = str(rem)
        lst.append(rem)
        ans = int(ans / 2)

lst.reverse()
binary = ""
for i in lst:
    binary += i
print("Binary         :",binary)

# HexaDecimal 
lst = []
rem = int(num % 16)
rem = str(rem)
lst.append(rem)
ans = int(num / 16)

for i in range(ans):
    if(ans>0):
        rem = int(ans % 16)
        rem = str(rem)
        lst.append(rem)
        ans = int(ans / 16)
lst.reverse()     

for i in lst:
        if(i=='10'):
          lst [lst.index('10')] = 'A'
        if(i=='11'):
          lst [lst.index('11')] = 'B'
        if(i=='12'):
          lst [lst.index('12')] = 'C'
        if(i=='13'):
          lst [lst.index('13')] = 'D'
        if(i=='14'):
          lst [lst.index('14')] = 'E'
        if(i=='15'):
          lst [lst.index('15')] = 'F'
        
hexa = ""
for i in lst:
    hexa += i 
print("HexaDecimal    :",hexa)
        
        
        
        
        
        
        
        
        
        
        
        
        