import rotatescreen
import time
import emoji

screen = rotatescreen.get_primary_display()
start_pos = screen.current_orientation
name = input ("Enter you name : ")
name = name.upper()
for i in range(0,5):
    pos = abs((start_pos - i*90) % 360)
    screen.rotate_to(pos)
    print("############# ",name,"HENGE NAAVU",emoji.emojize(':grinning_face:')," #############")
    time.sleep(0.5)