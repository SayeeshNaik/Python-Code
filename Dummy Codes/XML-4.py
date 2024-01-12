
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
    count = 0
    
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
              if(element[i][j].tag=="E1CUVAL" or element[i][j].tag=="E1EDP01"):
                  count+=1
                  for l in range(len(element[i][j])):
                      True
                      print(element[i][j][l].tag,"  ",element[i][j][l].text)
                      dup_lst.append(element[i][j][l].tag)
                      dup_lst_val.append(element[i][j][l].text)
                  
    #print(len(element[92][5]))
   
                  
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
    
   # print("\n")
    #print("\n*************//  Latest Update : " + date + "  //**************")
    ind = 1
    for b in range(len(dup_lst)):
        for c in range(len(xl_val)):
          xl_val[c] = str(xl_val[c])
          xl_tag[c] = str(xl_tag[c])
          dup_lst[b] = str(dup_lst[b])
          dup_lst_val[b] = str(dup_lst_val[b])
          if(xl_val[c]==dup_lst_val[b] and xl_tag[c]==dup_lst[b]):
              idd = ind
              ind = idd
              print(ind,").",dup_lst[b],"   ",xl_val[c])
              print("    " ,dup_lst_val[b],"   --text exist")
              txt_file.write("\n" + str(ind) + ") Tag  =  " + str(dup_lst[b]))
              txt_file.write("\n   Text =  " + str(dup_lst_val[b]))
              ind = ind+1
    
    count=0
    for i in range(len(dup_lst)):
        if(dup_lst[i]=="E1CUVAL"):
            count+=1
   

    

path = "C:/Users/User/Downloads/111060_Lammering Meppen_EDI.xml"
MyXML(path)