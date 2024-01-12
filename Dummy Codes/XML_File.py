
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime

def MyXML(filePath):
    lst_tag = []
    lst_text = []
    dup_lst = []
    dup_lst_val = []
    xl_tag = []
    xl_val = []
    new_tag = []
    
    file=open(filePath,"r")
    mytree = ET.parse(file)
    myroot = mytree.getroot()
    element = myroot[0]
    ln = len(element)
    for i in range(ln):
     # print("\n") 
      for j in range(len(element[i])):
          #print(element[i][j].tag,"  ",element[i][j].text)
          if(element[i][j] != "None"):
             # print("modified : ",element[i][j].tag,"    ",element[i][j].text)
              dup_lst.append(element[i][j].tag)
              dup_lst_val.append(element[i][j].text)
              if(element[i][j]=="ZA"):
                  print("Text is Available")
                  
    #print(dup_lst)
    #print(dup_lst_val)
    path = "D:/FlaskProject-1/XML_XL_File.xlsx" 
    df = pd.read_excel(path)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df[df['Name'].notna()]
    js = df.to_dict(orient='records')
    
    #print(df)
    #print(js)
    date = datetime.now()
    date = str(date)
    
    path = "D:/FlaskProject-1/XML-files/MyXML.txt"
    txt_file = open(path,"a")
    txt_file.write("\n********************************//  Latest Update : " + date + "  //*********************************")
    txt_file.write("\nExisted Tag's and Text's are : ")
    
    for xl in range(len(df)):
        if(js[xl]['Mandatory'] == 1):
           # print(js[xl]['Name'])
            xl_tag.append(js[xl]['Name'])
            xl_val.append(js[xl]['Value'])
    
    print("\n")
    print("\n*************//  Latest Update : " + date + "  //**************")
    ind = 1
    for b in range(len(dup_lst)):
        for c in range(len(xl_val)):
          xl_val[c] = str(xl_val[c])
          if(dup_lst_val[b]==xl_val[c] and dup_lst[b] == xl_tag[c]):
              idd = ind
              ind = idd
              print(ind,").",dup_lst[b])
              print("    " ,dup_lst_val[b],"   --text exist")
              txt_file.write("\n" + str(ind) + ") Tag  =  " + str(dup_lst[b]))
              txt_file.write("\n   Text =  " + str(dup_lst_val[b]))
              ind = ind+1
    
    count=0
    for i in range(len(dup_lst)):
        if(dup_lst[i]=="E1CUVAL"):
            count+=1
    print(count)

    

path = "C:/Users/User/Downloads/111060_Lammering Meppen_EDI.xml"
MyXML(path)
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime

def MyXML(filePath):
    lst_tag = []
    lst_text = []
    dup_lst = []
    dup_lst_val = []
    xl_tag = []
    xl_val = []
    new_tag = []
    
    file=open(filePath,"r")
    mytree = ET.parse(file)
    myroot = mytree.getroot()
    element = myroot[0]
    ln = len(element)
    for i in range(ln):
     # print("\n") 
      for j in range(len(element[i])):
          #print(element[i][j].tag,"  ",element[i][j].text)
          if(element[i][j] != "None"):
             # print("modified : ",element[i][j].tag,"    ",element[i][j].text)
              dup_lst.append(element[i][j].tag)
              dup_lst_val.append(element[i][j].text)
              if(element[i][j]=="ZA"):
                  print("Text is Available")
                  
    #print(dup_lst)
    #print(dup_lst_val)
    path = "D:/FlaskProject-1/XML_XL_File.xlsx" 
    df = pd.read_excel(path)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df[df['Name'].notna()]
    js = df.to_dict(orient='records')
    
    #print(df)
    #print(js)
    date = datetime.now()
    date = str(date)
    
    path = "D:/FlaskProject-1/XML-files/MyXML.txt"
    txt_file = open(path,"a")
    txt_file.write("\n********************************//  Latest Update : " + date + "  //*********************************")
    txt_file.write("\nExisted Tag's and Text's are : ")
    
    for xl in range(len(df)):
        if(js[xl]['Mandatory'] == 1):
           # print(js[xl]['Name'])
            xl_tag.append(js[xl]['Name'])
            xl_val.append(js[xl]['Value'])
    
    print("\n")
    print("\n*************//  Latest Update : " + date + "  //**************")
    ind = 1
    for b in range(len(dup_lst)):
        for c in range(len(xl_val)):
          xl_val[c] = str(xl_val[c])
          if(dup_lst_val[b]==xl_val[c] and dup_lst[b] == xl_tag[c]):
              idd = ind
              ind = idd
              print(ind,").",dup_lst[b])
              print("    " ,dup_lst_val[b],"   --text exist")
              txt_file.write("\n" + str(ind) + ") Tag  =  " + str(dup_lst[b]))
              txt_file.write("\n   Text =  " + str(dup_lst_val[b]))
              ind = ind+1
    
    count=0
    for i in range(len(dup_lst)):
        if(dup_lst[i]=="E1CUVAL"):
            count+=1
    print(count)

    

path = "C:/Users/User/Downloads/111060_Lammering Meppen_EDI.xml"
MyXML(path)