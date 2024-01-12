from flask import Flask,render_template,jsonify,request
from flask_cors import CORS

app=Flask(__name__,template_folder='template')
CORS(app)

@app.route('/',methods=['GET','POST'])
def run():
    return render_template('demo5.html')



@app.route('/demo',methods=['GET','POST'])

def deo():
    
    if request.method == 'GET':
        obj={'gender':['male','female']}
        return jsonify(obj)

if __name__ == '__main__':
    app.run()

  
