import numpy as np

#cv2 = imp.load_dynamic('cv2','./cv2.pyd')
#cv2 = imp.load_dynamic('cv2','./cv2.so')
import cv2 #Probably pip cv2 is not opencv package

testImg = cv2.imread('test.jpg', cv2.CV_LOAD_IMAGE_GRAYSCALE)

frontFaceCascades = (cv2.CascadeClassifier('cascades/haarcascade_frontalface_alt2.xml'),)

eyesCascades = (cv2.CascadeClassifier('cascades/haarcascade_lefteye_2splits.xml'), 
	cv2.CascadeClassifier('cascades/haarcascade_righteye_2splits.xml'))

nosesCascades = (cv2.CascadeClassifier('cascades/Nose.xml'),
	cv2.CascadeClassifier('cascades/haarcascade_mcs_nose.xml'))

mouthsCascades = (cv2.CascadeClassifier('cascades/Mouth.xml'),)



faces = frontFaceCascades[0].detectMultiScale(testImg, 1.1, 3)

for (x,y,w,h) in faces:
    cv2.rectangle(testImg,(x,y),(x+w,y+h),(255,0,0),2)



cv2.imshow("Image", testImg)
cv2.waitKey()