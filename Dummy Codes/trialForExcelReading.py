import pandas as pd

path = 'C:/Users/User/OneDrive/Documents/' ;
file =pd.read_excel(path+'MyExcell.xlsx') ;

# To convert DataFrame to Object
DJ = file.to_json(orient = 'records',)

print(file)
print(DJ)

print()