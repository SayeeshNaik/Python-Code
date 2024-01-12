lst = [1,2,3,6,9,25,44,23,78,66,27,88,640]
r = []
print("Old_List = ",lst)
ln = len(lst)
for i in lst:
   if(i%2 !=0):
     lst.remove(i)
     r.append(i)
print("Even Num = ",r)
print("New List = ",lst)
        