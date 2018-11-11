from picamera.array import PiRGBArray
from picamera import PiCamera
import picamera.array
import time
import cv2
import numpy as np
 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
 
# allow the camera to warmup
time.sleep(0.1)

left_counter=0  #counter for left movement
right_counter=0 #counter for right movement
        
th_value=5   #changeable threshold value 

def thresholding( value ):# function to threshold and give either left or right
    global left_counter
    global right_counter
    print(value)
    if (value<=54):   #check the parameter is less than equal or greater than range to 
        '''left_counter=left_counter+1             #increment left counter 

        if (left_counter>th_value):  #if left counter is greater than threshold value 
            print ('LEFT')  #the eye is left
            left_counter=0'''   #reset the counter

    elif(value>54):  # same procedure for right eye
        '''
        right_counter=right_counter+1

        if(right_counter>th_value):
            print ('RIGHT')
            right_counter=0
    else:
        print('STRAIGHT')'''

# capture frames from the camera
for frame1 in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    
    #frame = np.asarray(frame1)
    
    frame=frame1.array
    frame=np.asarray(frame,dtype='uint8')
    col=frame    
    frame=cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
    pupilFrame=frame
    clahe=frame
    blur=frame
    edges=frame
    eyes = cv2.CascadeClassifier('haarcascade_eye.xml')
    detected = eyes.detectMultiScale(frame, 1.3, 5)
    for (x,y,w,h) in detected: #similar to face detection
        cv2.rectangle(frame, (x,y), ((x+w),(y+h)), (0,0,255),1)  #draw rectangle around eyes
        cv2.line(frame, (x,y), ((x+w,y+h)), (0,0,255),1)   #draw cross
        cv2.line(frame, (x+w,y), ((x,y+h)), (0,0,255),1)
        print(w,x,y,h)
        pupilFrame = cv2.equalizeHist(frame[y+int((h*0.25)):(y+h),x:int(x+w)]) #using histogram equalization of better image. 
        cl1 = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(8,8)) #set grid size
        clahe = cl1.apply(pupilFrame)  #clahe
        blur = cv2.medianBlur(clahe, 5)  #median blur
        circles = cv2.HoughCircles(blur ,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=7,maxRadius=21) #houghcircles
        if circles is not None: #if atleast 1 is detected
            circles = np.round(circles[0,:]).astype("int") #change float to integer
            print ('integer',circles)
            for (x,y,r) in circles:
                cv2.circle(pupilFrame, (x, y), r, (0, 255, 255), 2)
                cv2.rectangle(pupilFrame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                #set thresholds
                thresholding(x)
                            

    #frame = cv2.medianBlur(frame,5)
    cv2.imshow('image',pupilFrame)
    cv2.imshow('clahe', clahe)
    cv2.imshow('blur', blur)
    
    rawCapture.truncate(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break




