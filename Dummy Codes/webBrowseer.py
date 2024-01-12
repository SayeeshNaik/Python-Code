import webbrowser,pyautogui,time
urls = ['google.com','google.com/search?q=yana']
for url in urls:
    webbrowser.open(url)
    time.sleep(2)
    #pyautogui.hotkey('ctrl', 'w')