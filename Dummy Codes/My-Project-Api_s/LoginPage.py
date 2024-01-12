from Email_Sending import email
from flask import Flask,request
from flask_cors import CORS
import psycopg2 as pg
import psycopg2.extras
from sqlalchemy import create_engine
import pandas as pd
import cryptocode
import time

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


app=Flask(__name__)
CORS(app)


# ----- DataFrame LoginDetails ----------------------------------------------
# df = pd.read_sql_table('logindetails',engine)
#----------------------------------------------------------------------------

glob_password = 'olddd'
@app.route('/sign_in',methods=['GET','POST'])
def sign_in():
    global glob_password
    df = pd.read_sql_table('logindetails',engine)
    username = request.args.get('username')
    password = request.args.get('password')
    
    db_username = list(df['username'])
    db_password = list(df['password'])
    
    if username in db_username:
        ind = db_username.index(username)
        if(password == db_password[ind]):
            encode = cryptocode.encrypt(username, password)
            glob_password = password
            print('Login Success')
            decode = myDecryptedMessage = cryptocode.decrypt(encode,password)
            return {'status':'Login Success','token':encode,'username':username},200
        else:
            print('Wrong Password')
            return {'status':'Wrong Password !!!'},500
    else:
        print('Username Not Exists')
        return {'status':'Username Not Exist !!!'},500
   
@app.route('/auth',methods=['GET','POST'])
def auth():
    df = pd.read_sql_table('logindetails',engine)
    df_username = list(df['username'])
    recived_token = request.args.get('token')
    decoded_username = cryptocode.decrypt(recived_token,glob_password)
    if(decoded_username in df_username): return {'status':'username-exist'},200
    else : return {'status':'username-not-exist'},500
    
 
@app.route('/admins',methods=['GET','POST'])
def admins():
    df = pd.read_sql_table('logindetails',engine)
    admins = ['Sayeesh','Vinayak','Yatish','Mahesh']
    return {'admins':admins},200

@app.route('/exists',methods=['GET','POST'])
def exists():
    df = pd.read_sql_table('logindetails',engine)
    flag = str(request.args.get('flag'))
    val = str(request.args.get('val'))
    df_flag = list(df[flag])
    if val in df_flag: return{'status':'Exists'},500
    else: return {'status':'Not-Exists'},200

@app.route('/sign_up',methods=['GET','POST'])
def sing_up():
    df = pd.read_sql_table('logindetails',engine)
    try:
        username = str(request.args.get('username'))
        email = str(request.args.get('email'))
        password = str(request.args.get('password'))
        query = "Insert into logindetails values('{}','{}','{}')".format(username,email,password)
        cur.execute(query)
        conn.commit()
        print("Details inserted Successfully")
        cur.execute("select * from logindetails")
        conn.commit()
        df=pd.read_sql_table('logindetails',engine)
        df.to_excel('LoginPageData.xlsx')
        print('Updated')
        return {'status':'Success'},200
    except Exception as e:
        return {'status':'Failed'},500
   
glob_username = ''
glob_token = ''
valid = ''
   
@app.route('/forgot',methods=['GET','POST'])
def forgot():
    global glob_username
    global glob_token
    global valid
    valid=1
    df = pd.read_sql_table('logindetails',engine)
    username = request.args.get('username')
    df_username = list(df['username'])
    df_email = list(df['email'])
    df_password = list(df['password'])
    if username in df_username:
        ind = df_username.index(username)
        # Token Genarate
        token = cryptocode.encrypt(username, df_password[ind])
        glob_token = token
        email_status = email(df_email[ind],username,token)
        glob_username = username
        return {'email':df_email[ind],'status':email_status},200
        time.sleep(30)
        glob_token = ''
    else:
        return {'status':email_status},500
        
@app.route('/reset',methods=['GET','POST'])
def reset():
    global valid
    password = request.args.get('newPassword')
    token = request.args.get('token')
    token = token.replace(' ','+')
    token = token.replace('$','&')
    if(glob_token==token and valid==1):
        try:
            query = ''' UPDATE logindetails set password='{}' where username='{}' '''.format(password,glob_username)
            cur.execute(query)
            conn.commit()
            valid=0
            return {'status':'success'}
        except:
            return {'status':'failure'},500
           
    else:
            print('tokens not matching !!')
            return {'status':'Tokens Not Matching'},500
    



app.run()





















    