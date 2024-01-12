import xml.etree.ElementTree as ET
import pandas as pd

def MyXML(filePath):
    lst_tag = []
    lst_text = []
    tag1 = []
    tag2 = []
    tag3 = []
    tag4 = []
    
    file=open(filePath,"r")
    mytree = ET.parse(file)
    myroot = mytree.getroot()
    element = myroot[0]
    ln = len(element)
   
    if(ln>0):
        #print('tag is there')
        for i in range(ln):
           lst_tag.append(element[i].tag)
           lst_text.append(element[i].text)
           tag1.append(element[i].tag)
           ln1 = len(element[i])
           if(ln1 > 0):
                for j in range(ln1):
                 # print(element[i][j].tag)
                  lst_tag.append(element[i][j].tag)
                  lst_text.append(element[i][j].text)
                  tag2.append(element[i][j].tag)
                  ln2 = len(element[i][j])
                  
                  if(ln2 > 0):
                      for k in range(ln2):
                        #print(element[i][j][k].tag)
                        lst_tag.append(element[i][j][k].tag)
                        lst_text.append(element[i][j][k].text)
                        tag3.append(element[i][j][k].tag)
                        ln3 = len(element[i][j][k])
                        
                        if(ln3 > 0):
                            for l in range(ln3):
                               # print(element[i][j][k][l].tag)
                                lst_tag.append(element[i][j][k][l].tag)
                                lst_text.append(element[i][j][k][l].text)
                                tag4.append(element[i][j][k][l].tag)
                                ln4 = len(element[i][j][k][l])
                                
                                if(ln4 > 0):
                                    for m in range(ln4):
                                        print(element[i][j][k][l][m].tag)
                                        lst_tag.append(element[i][j][k][l][m].tag)
                                        lst_text.append(element[i][j][k][l][m].text)
                                
    # Append All-Tags To Xl-Sheet --------------
    xl_path="D:/IRIS_Projects/XML_Tag_Child.xlsx"
    df = pd.DataFrame(tag1)
    list1=pd.Series(tag1)
    list2=pd.Series(tag2)
    list3=pd.Series(tag3)
    df = pd.concat([list1,list2,list3], ignore_index=True, axis=1)
    df.columns=["Tag","SubTag","ChildTag"]
    df.to_excel(xl_path,index = False)
    print(df)
 
    

path = "D:/IRIS_Projects/111093_Lammering withoutDocNum.xml"
MyXML(path)


