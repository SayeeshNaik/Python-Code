# Txt File creating
new_file = input("Enter New file name : ")
new_file = new_file + ".txt"
path = "D:/FlaskProject-1/Txt_Files/"
print(path+new_file)
file = open(path + new_file, "w+")
print("New File created Successfully")
file.close()
