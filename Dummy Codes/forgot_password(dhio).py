from flask import Flask,request
from flask_cors import CORS
import re  

app=Flask(__name__)
CORS(app)

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  
regex_password = '[0-9]{8,12}'

@app.route('/forgot_password')
def forgot_password():
    datas = request.args.get('email')
    print(datas)
    
    if(re.search(regex, datas)):       
        status = 'Email sent successfully'
    else : 
        status = 'Invalid Email'
    
    return {'status' : status}

@app.route('/reset_password',methods=['GET','POST'])
def reset_password():
    newPassword = request.args.get('NewPassword')
    confirmPassword = request.args.get('ConfirmPassword')
    if(re.search(regex_password, newPassword)):
        if(newPassword == confirmPassword):
            status = 'New Password Reset Succesfully'
        else :
            status = 'Passowrd is Not Matching'
    
        return {'status':status}
    else : 
        return {'status':'length should be min 8'}

app.run()
  

  
