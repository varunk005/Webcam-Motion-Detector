# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 19:27:31 2020

@author: Dell
"""
import cv2,time,pandas
from datetime import datetime

first_frame = None #savinf first frame

status_list=[None,None] # none added bcause python was not finding second item whem it was getting time and date
times=[]
df=pandas.DataFrame(columns=["Start","End"])
video=cv2.VideoCapture(0)

while True:
    check,frame= video.read()
    status =0     # to check wheter motion or not
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0) # more accuracy in difference
    
    if first_frame is None:
        first_frame=gray
        
    delta_frame=cv2.absdiff(first_frame,gray)
    thresh_frame=cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1] # this one is for accesing the second item of tuple 
    thresh_frame=cv2.dilate(thresh_frame, None, iterations=2) #smoothing removing black patchesx
    
    
    #finding countours curved areasb of sane intensity here white
    (cnts,_)=cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    #if the contour density is less than 1000 than continue searching otherwise create rectangle around the image
    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        status=1
        #creatin rectangle
        (x, y, w, h)=cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 3)
    
    status_list.append(status)
    status_list=status_list[-2:] # we require only two items ot saves memory
    
    # getting time and date of motion changed
    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.now())

    
    
    cv2.imshow("Capturing",gray)
    cv2.imshow("Delta frame",delta_frame)
    cv2.imshow("Thresh",thresh_frame)
    cv2.imshow("Webcam Motion Detector",frame)
    
    
    key =cv2.waitKey(1)
 
    
    if key==ord('q'):
        #if object is int the frame and we press q it does not record eit time so we dot this
         if status==1:
            times.append(datetime.now())
         break
    print(status_list)
    print(times)
for i in range(0,len(times),2):
    df=df.append({"Start":times[i],"End":times[i+1]},ignore_index=True)

    df.to_csv("Times.csv")

video.release()
cv2.destroyAllWindows
    
    
    
