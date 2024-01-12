import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def email(email,otp):      
    mail_to = email
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
        print("Email Send Successfully !!")
        return {'status':'success'},200
    
    except:
        print("Not Sending Email !!")
        return {'status':'failure'},500
    
email('yathish.s@dhiomics.com','8937')