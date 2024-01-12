import PyPDF2
from tabula import read_pdf
from tabulate import tabulate
import tabulate as tb
import pandas as pd
from PyPDF2 import PdfFileReader

pdf_file = "C:/Users/User/Downloads/Descours Athies-sous-Laon + Saint-Dizier8237.pdf"
readpdf = PyPDF2.PdfFileReader(pdf_file)
totalpages = readpdf.numPages

table = read_pdf(pdf_file,pages=1)
df1 = pd.concat(table)
print(df1)
    
for i in range(1,totalpages):
    table = read_pdf(pdf_file,pages=i)
    df2 = pd.concat(table)
    df = pd.concat([df1,df2])
    df1 = df
    # df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    # df.drop('Desc %', inplace=True, axis=1)
    # df = df[df['Und Item'].notna()]
    df.fillna("*",inplace=True)
    data = PdfFileReader(pdf_file)
    
xl_path = 'C:/Users/User/Downloads/table.xlsx'
excel = df1.to_excel(xl_path)

# print(df.to_string())
# print(totalpages)