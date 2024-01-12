import re


def simple():
    pattern = input('Enter Pattern : ')
    user_input = input("Enter Text : ")
    if(re.search(pattern, user_input)):
        print('valid')
    else : 
        print('invalid')

def matching():
    text = input('Enter your text : ')
    print("Text : ",text)
    finder = input('Enter Searching String : ')
    pattern = re.compile( finder )
    matching = pattern.finditer( text )
    for match in matching :
        print(match)

simple()