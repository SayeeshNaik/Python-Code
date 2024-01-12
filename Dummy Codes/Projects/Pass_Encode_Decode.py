import cryptocode

encoded = cryptocode.encrypt("9","s_pass")+'By_Sayeesh'
decoded = cryptocode.decrypt(encoded, "s_pass")
print(encoded)
print(decoded)