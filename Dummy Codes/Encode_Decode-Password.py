import cryptocode

password = "Sayeesh555"
encoded = cryptocode.encrypt(password,"sayeesh123password")
## And then to decode it:
decoded = cryptocode.decrypt(encoded, "sayeesh123password")
print(encoded)
print(decoded)

coming = "YRNqjMn/psNPw==*dpoKwJnT8ksqll7jfjqZFQ==*ib2OrDke0mX2+9riv/4oYQ==*GeIgmNYvuqAi7GscEWmlag=="
response = cryptocode.decrypt(coming,"sayeesh123password")
if(response == decoded):
    print('Correct Password')
else :
    print('Wrong Password')