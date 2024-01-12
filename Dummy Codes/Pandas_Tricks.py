import pandas as pd
import io
import requests
# Fetch data from URL
# url='http://bit.ly/chiporders'
url = 'http://bit.ly/movieusers'
# Add cols
col_list=['id','age','gender','occuption','sallary']
new = ['i','jj','kk','ss','cc']
df = pd.read_csv(url,names=col_list,sep='|')

# Rename
# df.columns = new

# Str replace
# df.columns = df.columns.str.replace('a','$')

# Shape of DF
# df.shape

# Drop Row 
# df.drop(['age'],axis=1,inplace=True)

# Drop Columns
# df.drop([0,1,2],axis=0,inplace=True)

# Sorting
# df.head().age.sort_values()
# df.head().age.sort_values(ascending=False)
# df.head().sort_values('age')
# df.head().sort_values(['age','sallary'])

# For Loop like a work
# test = df.loc[df.age >=25,'id']
# df[df.age.isin([61,70])]
# df.loc[(df.age>60) & (df.gender=='M'),['age', 'gender', 'sallary']]

print()



















