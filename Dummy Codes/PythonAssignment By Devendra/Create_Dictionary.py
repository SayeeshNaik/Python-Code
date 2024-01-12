keys = []
values = []
for i in range(2):
    k = input('Key : ')
    keys.append(k)
    v = input('val : ')
    values.append(v)
d = [dict(zip(keys,values))]

print(d)