
data = {
    "users":{
        "sayeesh":[]
    }
}

default_user = "sayeesh"
main_data=data['users'][default_user]

def chatting():
    for msg in main_data:
        if(msg[0]==default_user):
            # print('\t\t'," . ")
            for msg_content in msg[1:]:
                print('.\t\t\t\t\t\t',msg_content)
        else:
            for msg_content in msg[1:]:
                print(msg_content)
         
while(1):
    temp_lis = []
    user = input("U = ")
    msg = input("Msg = ")
    temp_lis.append(user)
    temp_lis.append(msg)
    main_data.append(temp_lis)
    
    print("\n**********************************************")
    chatting()
    print("\n**********************************************\n")
                
                
                
                
                
                
                