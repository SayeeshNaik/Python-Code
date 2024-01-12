import tkinter as tk
import time
import sys

def digital_clock(): 
    #for i in range(10):
    print("\n")
    while(True):
      arr = []
      time_live = time.strftime("%H:%M:%S")
      arr.append(time_live)
      sys.stdout.write('\r                                  ' + arr[0])
      time.sleep(1)
      
digital_clock()