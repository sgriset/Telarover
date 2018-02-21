# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# HSV color thresholds for YELLOW
#THRESHOLD_LOW = (15, 210, 20);
#THRESHOLD_HIGH = (35, 255, 255);

#HSV color thresholds for GREEN
THRESHOLD_LOW = (29, 86, 6);
THRESHOLD_HIGH = (64, 255, 255);




# Minimum required radius of enclosing circle of contour
MIN_RADIUS = 2

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
 
# allow the camera to warmup
time.sleep(0.1)


for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    # Blur image to remove noise
    img_filter = cv2.GaussianBlur(image.copy(), (3, 3), 0)
    # Convert image from BGR to HSV
    img_filter = cv2.cvtColor(img_filter, cv2.COLOR_BGR2HSV)
    # Set pixels to white if in color range, others to black (binary bitmap)
    img_binary = cv2.inRange(img_filter.copy(), THRESHOLD_LOW, THRESHOLD_HIGH)
    # Dilate image to make white blobs larger
    img_binary = cv2.dilate(img_binary, None, iterations = 1)
    # Find center of object using contours instead of blob detection.
    img_contours = img_binary.copy()
    contours = cv2.findContours(img_contours, cv2.RETR_EXTERNAL, \
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    # Find the largest contour and use it to compute the min enclosing circle	
    center = None
    radius = 0
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        if M["m00"] > 0:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            if radius < MIN_RADIUS:
                center = None

    # Print out the location and size (radius) of the largest detected contour                
    #if center != None:
    #    print str(center) + " " + str(radius)
    
    # Draw a green circle around the largest enclosed contour        
    if center != None:
        cv2.circle(image, center, int(round(radius)), (0, 255, 0))
    

    cv2.imshow("Telarover", image)
 #   cv2.imshow('binary', img_binary)
 #   cv2.imshow('contours', img_contours)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
            break
                
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
