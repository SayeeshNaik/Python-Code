from spellchecker import SpellChecker
spell = SpellChecker(language="en")

sentence = input("Enter Sentence : ")
words = sentence.split()

for word in words:
    possibality = list(spell.candidates(word))
    for check in possibality:
        try:
            if(word==check):
                print(word,"  Good")
                break
            else:
                print(word," Wrond wrong --( Did you mean : ",check," )")
                break
        except:
            pass