# Txt File Adding texts
text = input("Enter Text : ")
path = "D:/FlaskProject-1/Txt_Files/Sayeesh_file.txt"
file = open(path, "a")
file.write( text )
print("Text inserted Successfully")
file.close()

