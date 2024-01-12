# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 12:14:42 2022

@author: User
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def email(email,otp):  
    try:    
        mail_to = email
        mail_from = '''sayeesh444@gmail.com'''
        otp = str(otp)
   
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "OTP Verification"
        msg['From'] =mail_from
        msg['To'] = mail_to
        content = "Hello"
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
        print("Mail Not Send")

email('sayeesh.naik444@gmail.com',1234)
   
    
