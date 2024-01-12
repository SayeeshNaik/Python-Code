import pandas as pd

file1 = "D:/FlaskProject-1/CSV_Files/input1.xls"
file2 = "D:/FlaskProject-1/CSV_Files/input2.xls"
output = "D:/FlaskProject-1/CSV_Files/output.xls"

df1 = pd.read_excel(file1)
df2 = pd.read_excel(file2)
ot = pd.merge(df1, df2, on='name')
# ot.to_excel(output,index=False)
print(ot)