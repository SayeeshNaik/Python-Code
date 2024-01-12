import os
from PyPDF2 import PdfFileMerger

path = "C:/Users/User/Downloads/Table.pdf"
merger=PdfFileMerger()

for item in os.listdir(source_dir):
    
    if item.endswith('pdf'):
        print(item)
        merger.append(item)
        
