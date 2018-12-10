from picamera.array import PiRGBArray
from picamera import PiCamera
import picamera.array
import time
import cv2
import numpy as np
import RPi.GPIO as GPIO
 
GPIO.setmode(GPIO.BOARD)
 
Motor1A = 16
Motor1B = 18
#Motor1E = 22

Motor2A = 19
Motor2B = 21
#Motor2E = 23


def moveForwards():
    GPIO.setup(Motor1A,GPIO.OUT)
    GPIO.setup(Motor1B,GPIO.OUT)

    GPIO.setup(Motor2A,GPIO.OUT)
    GPIO.setup(Motor2B,GPIO.OUT) 
    print ("Going forwards")
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)

    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)

def stop():
    GPIO.setup(Motor1A,GPIO.OUT)
    GPIO.setup(Motor1B,GPIO.OUT)

    GPIO.setup(Motor2A,GPIO.OUT)
    GPIO.setup(Motor2B,GPIO.OUT)
    print ("Stopped")
    GPIO.output(Motor1A, GPIO.LOW)
    GPIO.output(Motor2A, GPIO.LOW)
 

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 60
rawCapture = PiRGBArray(camera, size=(640, 480))
 
time.sleep(0.1)

           

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
    for (x,y,w,h) in detected: 
        cv2.rectangle(frame, (x,y), ((x+w),(y+h)), (0,0,255),1)  #rectangle around eyes
        cv2.line(frame, (x,y), ((x+w,y+h)), (0,0,255),1)   #cross
        cv2.line(frame, (x+w,y), ((x,y+h)), (0,0,255),1)
        #print(w,x,y,h)
        pupilFrame = cv2.equalizeHist(frame[y+int((h*0.25)):(y+h),x:int(x+w)])  
        cl1 = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(8,8)) 
        clahe = cl1.apply(pupilFrame)  
        blur = cv2.medianBlur(clahe, 5)  
        circles = cv2.HoughCircles(blur ,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=7,maxRadius=21) #houghcircles
        if circles is not None: 
            circles = np.round(circles[0,:]).astype("int") 
            print ('integer',circles)
            for (x,y,r) in circles:
                cv2.circle(pupilFrame, (x, y), r, (0, 255, 255), 2)
                cv2.rectangle(pupilFrame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                
                if(x <=54):
                    print('Right')
                    moveForwards()
                elif(x>54):
                    print('left')
                    stop()
                            

    cv2.imshow('image',pupilFrame)
    cv2.imshow('clahe', clahe)
    cv2.imshow('blur', blur)
    
    rawCapture.truncate(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break




