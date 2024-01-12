import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime

def MyXML(filePath):
    lst_tag = []
    lst_text = []
    file=open(filePath,"r")
    mytree = ET.parse(file)
    myroot = mytree.getroot()
    element = myroot[0]
    ln = len(element)
    
    for i in range(ln):
   #     print("\n")
        tag = element[i].tag
   #     print(tag)
        ln = len(element[i])
       # print(i)
        #print('el = ',ln)
        for j in range(ln):
            sub_tag = element[i][j].tag
            lst_tag.append(sub_tag)
   #         print("    tag  : ",sub_tag)
            text = element[i][j].text
            lst_text.append(text)
            #print("    ",sub_tag,"     ",text)
    
    path = "D:/FlaskProject-1/XML_XL_File.xlsx" 
    df = pd.read_excel(path)
    js = df.to_dict(orient='records')
    
    print("\n*********************************// OUTPUT //*********************************")
    # Output-File
    latest = datetime.now()
    latest = str(latest)
    print("Last Updated : ", latest)
    file_path = "D:/FlaskProject-1/XML-files/MyXML.txt" 
    txt_file = open(file_path ,"a")
    txt_file.write("\n\n **********// Latest Update : " + latest +" //**********")
    txt_file.write("\n Existing Tags & Values are : ")
    for i in range(len(js)):
        if(js[i]['Mandatory'] == 1):
            tag_name = js[i]['Name']
            print("\nTag = ",tag_name)
            index = lst_tag.index(tag_name)
            ans = lst_text[index]
            print("value = ",ans) 
            # Output-File
            txt_file.write("\n TagName = " + tag_name)
            txt_file.write("\n Value = " + ans)
            if(ans != None):
                print("--Text is Exist")
            else:
                print("--Text is Not-Exist")
    
    '''
    tag_name = input("Enter Tag Name : ")
    index = lst_tag.index(tag_name)
    ans = lst_text[index]
    print(index)
    print("value = ",ans)
    if(ans != None):
        print("Text is Exist")
    else:
        print("Text is Not-Exist")
        
    '''


        
path = "C:/Users/User/Downloads/111060_Lammering Meppen_EDI.xml"
MyXML(path)