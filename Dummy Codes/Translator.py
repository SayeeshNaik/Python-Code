from translate import Translator

translator = Translator(to_lang="kn", from_lang="en")

text_to_translate = input("English : ")
translated = translator.translate(text_to_translate)

print("Kannada :",translated)
