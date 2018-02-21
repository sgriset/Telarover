'''
To make the serial port accessible you must stop the kernal
using it by following the instructions here:
www.irrational.net/2012/04/19/using-the-raspberry-pis-serial-port
Note. MaxSorar has inverted TTL output so you get giggerish.
Single transistor invertor does the trick.
'''

import serial
import time

DEVICE = '/dev/ttyAMA0'
#DEVICE = '/dev/tty1'
BAUD = 9600

ser = serial.Serial(DEVICE, BAUD)
print(ser.name)
#ser.close()
#ser.open()
#ser.flush()
while 1:
    ser.flush()	
    msg = ser.read(5)
    print(msg)
    reading = int(msg[1:4])
    if reading <= 8:
        print(reading)
    	

