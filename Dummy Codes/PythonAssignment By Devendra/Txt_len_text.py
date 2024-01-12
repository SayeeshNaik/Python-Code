# Txt count Text length
path = "D:/FlaskProject-1/Txt_Files/Sayeesh_file.txt"

file = open(path,"r")
total = 0
for i in file:
    txt = i.split()
    for j in txt:
        print(len(j),j)
        total = total + len(j)

print("\nTotal Num of Texts = ",total)
    