# This program is the basic control program for the Telarover system
# using the RaspiRobotBoard version 2


from rrb2 import *
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
import cv2



rr = RRB2()
vs = PiVideoStream().start()
time.sleep(4.0)


while True:
    frame = vs.read()
    frame = imutils.resize(frame, width = 400)
    cv2.imshow("Telarover", frame)
    # key = cv2.waitKey(1) & 0xFF
    key = cv2.waitKey(1)    
    # if the `esc` key was pressed, break from the loop
    if key == 27:
        break
    if key == 32:
        rr.stop()
        rr.set_led1(False)
        rr.set_led2(False)
    if key == 65362:
        rr.forward(0,1)
        rr.set_led1(True)
        rr.set_led2(True)
    if key == 65364:
        rr.reverse(0,1)
        rr.set_led1(True)
        rr.set_led2(True)
    if key == 65363:
        rr.right(0,1)
        rr.set_led1(True)
        rr.set_led2(False)         
    if key == 65361:
        rr.left(0,1)
        rr.set_led1(False)
        rr.set_led2(True)
                    
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
rr.stop()
