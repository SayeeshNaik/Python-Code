
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
    latest_tag  = []
    latest_text = []
    test = 0
    
    file=open(filePath,"r")
    mytree = ET.parse(file)
    myroot = mytree.getroot()
    element = myroot[0]
    ln = len(element)
   
    if(ln>0):
        print('tag is there')
        for i in range(ln):
           # print(element[i].tag)
           lst_tag.append(element[i].tag)
           lst_text.append(element[i].text)
           ln1 = len(element[i])
           if(ln1 > 0):
                for j in range(ln1):
                 # print(element[i][j].tag)
                  lst_tag.append(element[i][j].tag)
                  lst_text.append(element[i][j].text)
                  ln2 = len(element[i][j])
                  
                  if(ln2 > 0):
                      for k in range(ln2):
                        #print(element[i][j][k].tag)
                        lst_tag.append(element[i][j][k].tag)
                        lst_text.append(element[i][j][k].text)
                        ln3 = len(element[i][j][k])
                        
                        if(ln3 > 0):
                            for l in range(ln3):
                               # print(element[i][j][k][l].tag)
                                lst_tag.append(element[i][j][k][l].tag)
                                lst_text.append(element[i][j][k][l].text)
                                ln4 = len(element[i][j][k][l])
                                
                                if(ln4 > 0):
                                    for m in range(ln4):
                                        print(element[i][j][k][l][m].tag)
                                        lst_tag.append(element[i][j][k][l][m].tag)
                                        lst_text.append(element[i][j][k][l][m].text)
                                
    xl_path = "D:/FlaskProject-1/XML_XL_File.xlsx" 
    df = pd.read_excel(xl_path)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df[df['Name'].notna()]
   # df = df.fillna(False)
    js = df.to_dict(orient='records')
    #print(js)
    
    for x in range(len(df)):
        js[x]['Name']      = str(js[x]['Name'])
        js[x]['Value']     = str(js[x]['Value'])
        
        if(js[x]['Mandatory']==1):
            xl_tag.append(js[x]['Name'])
            xl_val.append(js[x]['Value'])
        
    for y in range(len(lst_tag)):
        for z in range(len(xl_tag)):
            if(lst_tag[y]==xl_tag[z] and xl_val[z]==None):    
               # print(xl_tag[z],"  ",xl_val[z])
                latest_tag.append(lst_tag[y])
                latest_text.append(lst_text[y])
           
            if(lst_tag[y]==xl_tag[z] and xl_val[z]=='nan'):
                    count+=1
                   # print(lst_tag[y],"  ",lst_text[y])
                    latest_tag.append(lst_tag[y])
                    latest_text.append(lst_text[y])
                    
    # Text File OutPut ----------------------
    date = datetime.now()
    date = str(date)
    path = "D:/FlaskProject-1/XML-files/MyXML.txt"
    txt_file = open(path,"a")
    txt_file.write("\n********************************//  Latest Update : " + date + "  //*********************************")
    txt_file.write("\nExisted Tag's and Text's are : ")
    for r in range(len(latest_tag)):
        print(latest_tag[r],"  ",latest_text[r])
        txt_file.write("\n" + str(r) +").Tag   =  " + latest_tag[r])
        txt_file.write("\n   Text  =  " + latest_text[r])
   
    

path = "C:/Users/User/Downloads/111060_Lammering Meppen_EDI.xml"
MyXML(path)