import pandas as pd

path = "C:/Users/User/Downloads/19-01-2022-06-41-07extra_grade_minibar.xlsx"
df = pd.read_excel(path)
file = pd.DataFrame(df)
js = df.to_json(orient=('records'))

print(js)
