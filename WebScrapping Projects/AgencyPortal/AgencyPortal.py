import requests
import pandas as pd
import xmltodict, json
from bs4 import BeautifulSoup
from selenium import webdriver

def get_StateID():
    driver = webdriver.Chrome()
    url = 'https://agencyportal.irdai.gov.in/PublicAccess/AgentLocator.aspx'  
    driver.get(url)
    driver.implicitly_wait(10)
    page_source = driver.page_source
    driver.quit()
    soup = BeautifulSoup(page_source, 'html.parser')
    table = soup.find(id="ddlState")
    table = table.findAll("option")
    stateID_Json = []
    stateID_lis,stateName_lis = [],[]
    for htmlTag in table:
        stateName = (htmlTag.text).rstrip()
        stateID = htmlTag.get("value")
        if(stateName!="--Select State--" and stateID!=""):
            temp_stateID_Json = {}
            stateID_lis.append(stateID)
            stateName_lis.append(stateName_lis)
            temp_stateID_Json.update({"state_name": stateName})
            temp_stateID_Json.update({"state_id": stateID})
            stateID_Json.append(temp_stateID_Json)
    return stateID_Json

def get_District(stateData):
    stateID = stateData["state_id"]
    url = "https://agencyportal.irdai.gov.in/_WebService/General/DataLoader.asmx/GetDistrict"
    headers = {
        "cookie": "ASP.NET_SessionId=qjqg4afiq0kn1cf0jlk44h52",
    }
    page = requests.get(url,headers=headers,params={"StateID": stateID})
    data = xmltodict.parse(page.text)
    districtData = data["NewDataSet"]["Table"]
    return districtData
    
def table_data(insuranceType,stateID,distrinctID,pinCode):

    url = "https://agencyportal.irdai.gov.in/_WebService/PublicAccess/AgentLocator.asmx/LocateAgent"
    headers = {
        "cookie": "ASP.NET_SessionId=qjqg4afiq0kn1cf0jlk44h52",
    }
    data = {
        "page": "1",
        "rp": "9999",
        "sortname": "AgentName",
        "sortorder": "asc",
        "query": "",
        "qtype": "",
        "customquery": ",,,{},,{},{},{}".format(insuranceType,stateID,distrinctID,pinCode)
    }
    
    updated_data = []
    table_df = []
    try:
        response = requests.post(url, headers=headers, data=data)
        data = xmltodict.parse(response.text)
        for i in range(len(data["rows"]["row"])):
            temp_data = data["rows"]["row"][i]["cell"]
            if(temp_data!=None):
                updated_data.append(temp_data[1:])
        table_df = pd.DataFrame(updated_data,columns= ['Agent Name','License No', 'IRDA URN', 'AGENT ID','Insurance Type','Issuer','DP ID','STATE','DISTRICT','Pin Code','Valid From','Valid To', 'Absorbed Agent', 'Phone Number','Mobile No'])
        return table_df
    except:
        table_df = pd.DataFrame(columns= ['Agent Name','License No', 'IRDA URN', 'AGENT ID','Insurance Type','Issuer','DP ID','STATE','DISTRICT','Pin Code','Valid From','Valid To', 'Absorbed Agent', 'Phone Number','Mobile No'])

def final_data():
    main_df = pd.DataFrame(columns= ['Agent Name','License No', 'IRDA URN', 'AGENT ID','Insurance Type','Issuer','DP ID','STATE','DISTRICT','Pin Code','Valid From','Valid To', 'Absorbed Agent', 'Phone Number','Mobile No'])
    # state_json = get_StateID()
    with open('state_json.json', 'r') as f:
       state_json = json.loads(f.read())
    state_json = state_json[13:]
    for insuranceID in range(1,4):
        
        for state_data in state_json:
            stateID = state_data["state_id"]
            distrinct_data = get_District(state_data)
            for temp_distrinct_data in distrinct_data:
                try:
                    distrinctID = temp_distrinct_data["sntDistrictID"]
                    districtName = temp_distrinct_data["varDistrictName"]
                    pinCodeRange = temp_distrinct_data["varPINCodeRange"]
                    pinCodeRange = pinCodeRange.split("-")
                    
                    # for pincode in range(int(pinCodeRange[0]),int(pinCodeRange[1])):
                    for i in range(1):
    
                    # num = int(pinCodeRange[0])
                    # for pincode in range(num,num+2):
                        final_data = table_data(insuranceID,stateID,distrinctID,pinCodeRange[0])
                        print(final_data)
                        try:
                            main_df = pd.concat([main_df,final_data])
                        except: pass
                    main_df.to_excel("AgencyPortal2.xlsx")
                    print("DF Len = ",len(main_df))
                except: pass
                    
        
    
    
final_data()

# ot = table_data(1,1, 3,517001)
# print(ot)

# state_json = get_StateID()
# with open('state_json.json', 'w') as f:
#     json.dump(state_json, f)

