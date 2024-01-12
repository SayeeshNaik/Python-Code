from Email_Template import template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def email(email,username,token):      
    mail_to = email
    mail_from = '''sayeesh444@gmail.com'''
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "OTP Verification"
        msg['From'] =mail_from
        msg['To'] = mail_to
        content = template.format(username,token)
        body = MIMEText(content, 'html')
        msg.attach(body)
           
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo()
        server.starttls()
        server.login(mail_from,'coaymhewvkubseuf')
        server.sendmail(mail_from, mail_to,msg.as_string())     
        server.close()
        print("Email Send Successfully !!")
        return {'status':'success'},200
    except:
        return {'status':'failure'},500
