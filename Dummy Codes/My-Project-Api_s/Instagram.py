from flask import Flask,request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

dataFrame = []
@app.route('/instaPage')
def instaPage():
    data = [
        {
            'name':'Ashika',
            'image':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS9vYomz8_CprHVcRKfs9-Nlw8prhyiqC9K9g&usqp=CAU'
            },
        {
            'name':'Sayeesh',
            'image':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS9vYomz8_CprHVcRKfs9-Nlw8prhyiqC9K9g&usqp=CAU'
            },
        {
            'name':'Mahesh',
            'image':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS9vYomz8_CprHVcRKfs9-Nlw8prhyiqC9K9g&usqp=CAU'
            },
        ]
    return {'data':data}

like_lis=[]
hate_lis=[]
@app.route('/insta')
def insta():
    global dataFrame,like_lis,hate_lis
    username = request.args.get('username')
    img = request.args.get('img')
    like_status = request.args.get('like_status')
    
    if(like_status=='1'):
        like_lis.append(img)
        if img in hate_lis:
            hate_lis.remove(img)
    else:
        hate_lis.append(img)
        if img in like_lis:
            like_lis.remove(img)
            
    like_lis=list(set(like_lis))
    hate_lis=list(set(hate_lis))
    data = [{'username':username,'like_img':like_lis}]
    print('Like list = ',like_lis)
    print('Hate list = ',hate_lis)
    return {'dataframe':'good'}


app.run()
    
    

