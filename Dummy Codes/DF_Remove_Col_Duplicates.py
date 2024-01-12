import pandas as pd

data = [
            {'name':'sayeesh','age':20},
            {'name':'yatish','age':20},
            {'name':'pavan','age':10},
            {'name':'megha','age':50}
        ]

df = pd.DataFrame(data)
for i in df.columns: df.drop(columns=i,inplace=True) if len(set(df[i]))!=len(df)else ''
print(df)
