from flask import Flask,request
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

app.config['count']=0
@app.route('/quiz',methods=['GET','POST'])
def quz():
    data = [{
    'id':1,
    'question':'What is you name ?',
    'options':['sayeesh','yatish','vinayak','pavan']},
    {
    'id':2,
    'question':'What is your City ?',
    'options':['hubli','mysore','andra','kumta']},
    {
    'id':3,
    'question':'What is your Qualification ?',
    'options':['BSC','BCOM','ARTS','IT']}]
    
    ans = {1:'sayeesh',2:'hubli',3:'BSC',4:'India',5:''}
    f_id=request.args.get('id')
    print(f_id)
    if(f_id==''):f_id=1
    f_id=int(f_id)+1
    f_ans = request.args.get('ans')
    if(f_id<=len(data[0])):
        df = data[f_id-1]
        # df['options'] = random.sample(df['options'],4)
        # print(df)
        if(f_id>2):f_id-=1
        print(ans[f_id])
        print(f_ans)
        if(f_ans==ans[f_id+1]): 
            
            app.config['count']=app.config['count']+1
            
            print("right")
            return {'total':len(df),'data':df,'status':'Write','count':1}
        else: 
            print("****** ",app.config['count'])
            return {'total':len(df),'data':df,'status':'Wrong','count':0}
        print("%%%%%%% ",app.config['count'])
    else: return {'total':len(df),'data':df,'status':'Data Out of Range','count':0}
    
@app.route('/result',methods=['GET','POST'])
def result():
    count = 3
    return {'count':count}
app.run()