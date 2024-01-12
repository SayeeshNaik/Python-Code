import pyttsx3

engine = pyttsx3.init()
# text = input("Text : ")
text = ['hello','vinayaka','bye','illi']
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

engine.say(text)
# time.sleep(1)
engine.runAndWait()