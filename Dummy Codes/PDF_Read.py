# path = "C:/Users/User/Downloads/dummy.pdf"
path = "C:/Users/User/customer-data-table.pdf"

import PyPDF2
sample_pdf = open(path, mode='rb')
pdfdoc = PyPDF2.PdfFileReader(sample_pdf)
word = input("Enter a word : ")
for i in range(pdfdoc.numPages): 
    page_one= pdfdoc.getPage(i)
    output = page_one.extractText()
    
    count = 0
    for j in output.split():
        if word in j:
          count=count+1
    print('''Total Count of "{}" in page '''.format(word),i+1," = " ,count)
