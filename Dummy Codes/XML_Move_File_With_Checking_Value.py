import xml.etree.ElementTree as ET
import pandas as pd
import shutil

def MyXML(filePath):
    lst_tag = []
    lst_text = []
    xl_tag = []
    xl_val = []
    
    file=open(filePath,"r")
    mytree = ET.parse(file)
    myroot = mytree.getroot()
    element = myroot
    ln = len(element)
   
    if(ln>0):
        #print('tag is there')
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
                                        #print(element[i][j][k][l][m].tag)
                                        lst_tag.append(element[i][j][k][l][m].tag)
                                        lst_text.append(element[i][j][k][l][m].text)
                                        
    xl_path = "D:/IRIS_Projects/XML_Mandatory1.xlsx" 
    destini='D:/IRIS_Projects/moved_files'
    source=filePath
    
    # Xl - File Read ---------
    df = pd.read_excel(xl_path)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df[df['Name'].notna()]
    js = df.to_dict(orient='records')   
    
    for x in range(len(df)):
        js[x]['Name']      = str(js[x]['Name'])
        js[x]['Value']     =str( js[x]['Value'])
        if(js[x]['Mandatory']==1):
            xl_tag.append(js[x]['Name'])
            xl_val.append(js[x]['Value'])
   
    # Moving File -----------
    test = []
    for rec in js:
      if(rec['Mandatory']==1):
             status=0
             for i in  range(len(lst_tag)): 
                if(rec['Name']==lst_tag[i]):
                    rec['Value']=str(rec['Value'])
                    if(rec['Value']=='nan'):
                       #print(rec['Name'])
                       if(lst_text[i]!=None):
                           #print(rec['Name'])
                           status=1
                        
                    else:
                        # If xl have any value ------
                        try:
                          rec['Value']=float(rec['Value'])
                          lst_text[i]=float(lst_text[i])
                        except:
                            pass
                        if(rec['Value']==lst_text[i]):
                            status=1
             test.append(status)
    print("Test = ",test)
    
    # Moving File ------------
    if(0 in test):
        print("fail")
        shutil.copy(source,destini)
        print("Moved Path = ",destini) 
    else:
        print("success, Tag have a Value")

    file.close()
   

path = "D:/IRIS_Projects/111060_Lammering Meppen (1).xml"
MyXML(path)