import sys
sample = "Twinkle twinkle little star, How I wonder what you are!, Up above the world so high, Like a diamond in the sky, Twinkle twinkle little star, How I wonder what you are"
splitted=sample.split(',')
align = [1,2,4,4,2,1]
if(len(splitted)==len(align)):
    for i in range(len(align)):
        for j in range(align[i]):
          sys.stdout.write("  ")
        print(splitted[i])
else:print("Give Same length for both")