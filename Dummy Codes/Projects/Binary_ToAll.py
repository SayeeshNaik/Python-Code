binary = input("Binary  : ")
ln = len(binary)
decimal = 0
for i in binary:
    i = int(i)
    ln = ln-1
    ans = i*pow(2,ln)
    decimal += ans
print("Decimal : ",decimal)
    