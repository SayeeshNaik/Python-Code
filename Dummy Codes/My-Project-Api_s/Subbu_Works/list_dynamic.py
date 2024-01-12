lis = ['sayeesh',['vinayak',['abhi',['mahesh',['hello',['no more']]]]],'yatish',['subbu'],['jakkk',('vinayak')]]

ans = []
def list_fun(ls):
    for i in ls:
        if(type(i)==str):ans.append(i)
        else:list_fun(i)
     
list_fun(lis)        

print(ans)
