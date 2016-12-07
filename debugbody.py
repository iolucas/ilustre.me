from FaceDetector import *

import numpy as np

from PersonFace import *
from GeometricElements import *
from PointGenerator import *

import cv2

#image = cv2.imread("./debugpic/people1.jpg");
#image = cv2.imread("./debugpic/people2.jpg");
#image = cv2.imread("./debugpic/eu.png");
image = cv2.imread("./debugpic/test.jpg");
#image = cv2.imread("./debugpic/duffs.jpg");



maxWidth = 1800

if image.shape[1] > maxWidth:
    
    newHeight = maxWidth * image.shape[0] / image.shape[1]
    image = cv2.resize(image, (maxWidth, newHeight))


faceDetector = FaceDetector()

personFaces = faceDetector.Detect(image)

for personFace in personFaces:

    personFace.Evaluate()

    if not personFace.IsValid():
        continue

    faceRect = personFace.GetFace()
    mouthRect = personFace.GetMouth()
    noseRect = personFace.GetNose()
    eyesRects = personFace.GetEyes()

    faceLineData = personFace.GetFaceLineData()
    faceLine = PointGenerator(faceLineData[0], faceLineData[1])
    faceTopPoint = faceLine.GetFromY(faceRect.y)
    faceBottomPoint = faceLine.GetFromY(faceRect.y + faceRect.height)

    #faceRectJson = rectangleToJson(faceRect)
    #mouthRectJson = rectangleToJson(mouthRect)
    #noseRectJson = rectangleToJson(noseRect)

    #PIPELINE

    #1. Find the person faces squared region of interest
    #2. Create a region of interest around it scaled of 3.5 times the face square size
    #3. Scale the region of interest to standard size OF TO BE DEFINED
    #4. Create small quared cells (size TO BE DEFINED) (like HOG) to compute the histograms orientations of that region (must check all the other hog features that may be useful)
    #5. Compute machine learning with this
    



    #Get circle center
    circleCenter = (int(faceRect.x + faceRect.width/2), int(faceRect.y + faceRect.height/2))

    areaFactor = 3.5

    cv2.circle(image, circleCenter, int(faceRect.width/2 * areaFactor), (255,128,128), 2)

    print("SIZES")
    print(faceRect.width)
    print(faceRect.height)

    cv2.rectangle(image, faceRect.getTuple()[0], faceRect.getTuple()[1], (0,255,255), 2)
    #cv2.rectangle(image, mouthRect.getTuple()[0], mouthRect.getTuple()[1], (0,255,255), 1)
    #cv2.rectangle(image, noseRect.getTuple()[0], noseRect.getTuple()[1], (0,255,255), 1)

    #for eye in eyesRects:
        #cv2.rectangle(image, eye.getTuple()[0], eye.getTuple()[1], (0,255,255), 1)
        #cv2.rectangle(eye, )
        #eyeJson = rectangleToJson(eye)
        #eyesJson.append(eyeJson)

#KEEP DOING IT

cv2.imshow("Image", image)
cv2.waitKey(0)