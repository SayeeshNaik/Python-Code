lst = [1,2,3,4,5]
print("Old_List = ",lst)
for i in range(2):
    n = i
    d_number = int(input("Enter a Deleting Number : "))
    if( d_number in lst):
        index = lst.index(d_number)
        del lst[index]
    else :
        print("Not Exist : ",d_number)
print("New_list = ",lst)
