from flask import Flask,request
from flask_cors import CORS
import psycopg2 as pg
import psycopg2.extras
from sqlalchemy import create_engine
import pandas as pd
import cryptocode
from twilio.rest import Client
import random
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from excel import excel


hostname = 'localhost'
database = 'postgres'
username = 'postgres'
pwd = 12345
port_id = 5432

conn = pg.connect (
                    host = hostname,
                    dbname = database,
                    user = username,
                    password = pwd,
                    port = port_id
                  )
cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
engine = create_engine("postgresql://postgres:12345@127.0.0.1/postgres")


app = Flask(__name__)
CORS(app)

def email(mail,otp):      
    mail_to = mail
    mail_from = '''sayeesh444@gmail.com'''
    otp = str(otp)
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "OTP Verification"
        msg['From'] =mail_from
        msg['To'] = mail_to
        content = " Dear Customer,<br/><br/>Please don't share this OTP with anyone.<br/>Your OTP is : <b><u>"+ otp +"</u></b> <br/><br/> Thank you,<br/>Sayeesh Naik."
        body = MIMEText(content, 'html')
        msg.attach(body)
           
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo()
        server.starttls()
        server.login(mail_from,'#sayeesh444#')
        server.sendmail(mail_from, mail_to,msg.as_string())     
        server.close()
        return {'status':'success'},200
    
    except:return {'status':'failure'},500
        
@app.route('/p_sign_up',methods=['GET','POST'])
def sign_up():
    try:
        username = request.args.get('username')
        email = request.args.get('email')
        password = request.args.get('password')
        query = "Insert into logindetails values('{}','{}','{}')".format(username,email,password)
        cur.execute(query)
        conn.commit()
        print(query)
        print("Details inserted Successfully")
        cur.execute("select * from logindetails")
        conn.commit()
        df=pd.read_sql_table('logindetails',engine)
        print(df)
        return 'Data Updated'
    except Exception as e:
        print("Error : ",e)
        return 'fail'
        
@app.route('/sign_in',methods=['GET','POST'])
def sign_in():
    try:
        data = json.loads(request.data)
        username = data['email']
        # email = data['email']
        password = eval(data['password'])
        try:password = eval(password)
        except:password = password
        df=pd.read_sql_table('logindetails',engine)
        for i in range(len(df)):
            try:df['password'][i] = eval(df['password'][i])
            except:df['password'][i] = df['password'][i]
        status = 0
        for j in range(len(df)):
            if(username==df['username'][j] and password == df['password'][j]):
                status += 1 
            
        if(status>=1):return {'status':'success'},200
        else:return {'status':'failed'}
    except Exception as e:
        print('Error : ',e)
        pass
        return {'status':'error'}
    
        print(username,password)
   
otp = 0
@app.route('/p_send_otp',methods=['GET','POST'])
def otp():
    global otp
    
    otp = random.randint(1000,9999)
    acc = "ACfa39b27a2b317912309fd0b9064c8dc2"
    token = "3906b07d1e9eb6e888a952b09f5328ea"
    # mobile_num = request.args.get('num')
    # mobile_num = str(mobile_num)
    mail = request.args.get('mail')

    status = email(mail,otp)
    
    mobile_num = "9663064870"
    client = Client(acc,token)
    msg = client.messages.create(
        body = f"Your OTP is : {otp} \nThanks,\n--Sayeesh Naik",
        from_ = "+19105974306",
        to = "+91" + mobile_num
      )
    return {'status':status}

@app.route('/p_recived_otp',methods=['GET','POST'])
def recived_otp():
    recived_otp = request.args.get('otp')
    recived_otp = int(recived_otp)
    if(recived_otp == otp):return {'Status':'Success'},200
    else:return {'Status':'Fail'},500
        
          
   


app.run()