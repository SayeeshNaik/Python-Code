from twilio.rest import Client
import random
      
otp = random.randint(1000,9999)

acc = "ACfa39b27a2b317912309fd0b9064c8dc2"
token = "3906b07d1e9eb6e888a952b09f5328ea"

client = Client(acc,token)
msg = client.messages.create(
    body = f"Your OTP is : {otp}",
    from_ = "+19105974306",
    to = "+919663064870"
 )
def test(otp):
  a = int(input("Enter you OTP : "))
  if(a==otp):
      print("success") 
  else:
      print("fail")
      
test(otp)


