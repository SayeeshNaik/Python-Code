data = [{
    'id':1,
    'qn':'What is you name ?',
    'op':['sayeesh','yatish','vinayak','pavan'],
    'ans':'sayeesh'},
    {
    'id':2,
    'qn':'What is your City ?',
    'op':['hubli','mysore','andra','kumta'],
    'ans':'hubli'},
    {
    'id':3,
    'qn':'What is your Qualification ?',
    'op':['BSC','BCOM','ARTS','IT'],
    'ans':'BSC'}]

# count_ans = 0
# for i in data:
#     i['id']=1
#     print(str(i['id'])+')',i['qn'])
#     for j in set(i['op']):
#       print("  ",chr(i['id']+96)+')',j)
#       i['id']+=1
#     choice = input('Ans : ')
#     if(choice==i['op'][0]):
#         print('Right Ans')
#         count_ans+=1
#     else:
#         print('Wrong Ans')
#     print("*******************************")

# avg = (count_ans * 100)/len(data)
# print('Persentage = ',round(avg,2),'%')