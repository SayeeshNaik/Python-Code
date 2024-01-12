import os
import time
from datetime import timedelta
import sys

hr = int(input("Hrs : "))
mn = int(input("Min : "))
sec = int(input("Sec : "))
stop_time = (hr*60*60) + (mn*60) + sec
print("\n Music will Stop = ",hr,':',mn,':',sec)

for i in range(stop_time+1):
    sys.stdout.write('\r Playing.')
    time.sleep(0.1)
    sys.stdout.write('\r Playing.....')
    t = timedelta(seconds= stop_time - i)
    sys.stdout.write('\r Remaining Time = '+str(t))
    time.sleep(1)

os.system('taskkill /F /im Music.ui.exe')
# os.system('taskkill /F /im pythonw.exe')
print("\n Music Stoped")

