# Txt Remove existing txt file
import os
file_name = input("Enter Removing Txt file name : ")
file_name = file_name +".txt"
path = "D:/FlaskProject-1/Txt_Files/" + file_name
if os.path.exists(path):
    os.remove(path)
    print("Successfully file was removed")
else :
    print("File is Not-Exist")