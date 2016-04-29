import cv2
import numpy as np

from PersonFace import *
from GeometricElements import *
from PointGenerator import *

class FaceDetector:
    
    def __init__(self):
        #Init all the necessary cascades
        self.frontFaceCascades = (cv2.CascadeClassifier('cascades/haarcascade_frontalface_alt2.xml'),)
        self.eyesCascades = (cv2.CascadeClassifier('cascades/haarcascade_lefteye_2splits.xml'), 
            cv2.CascadeClassifier('cascades/haarcascade_righteye_2splits.xml'))
        self.nosesCascades = (cv2.CascadeClassifier('cascades/Nose.xml'), 
            cv2.CascadeClassifier('cascades/haarcascade_mcs_nose.xml'))
        self.mouthsCascades = (cv2.CascadeClassifier('cascades/Mouth.xml'),)

    def Detect(self, image):
        personFaces = []

        ugray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # normalizes brightness and increases contrast of the image
        ugray = cv2.equalizeHist(ugray)
                

        for faceCascade in self.frontFaceCascades:
        
            detectedFaces = faceCascade.detectMultiScale(ugray, 1.1, 3)

            for face in detectedFaces:

                personFace = PersonFace(Rectangle.FromTuple(face))

                personFaces.append(personFace)

                #Get the region of interest on the faces
                #Mat faceRegion = new Mat(ugray, face);
                #roi = gray[y1:y2, x1:x2]
                faceRegion = ugray[face[1]:face[1] + face[3], face[0]:face[0] + face[2]]
                        
                #Detect eyes
                for eyeCascade in self.eyesCascades:
                
                    detectedEyes = eyeCascade.detectMultiScale(faceRegion, 1.1, 3)
                    
                    for eye in detectedEyes:
                    
                        personFace.AddEye(Rectangle(eye[0] + face[0], eye[1] + face[1], eye[2], eye[3]))

                        #personFace.AddEye(Rectangle(eye.x + face.x, eye.y + face.y, 
                            #eye.width, eye.height));
                    
                

                #Detect mouths
                for mouthCascade in self.mouthsCascades:

                    detectedMouths = mouthCascade.detectMultiScale(faceRegion, 1.1, 3)

                    for mouth in detectedMouths:
                    
                        personFace.AddMouth(Rectangle(mouth[0] + face[0], mouth[1] + face[1], 
                            mouth[2], mouth[3]))

                        #personFace.AddMouth(new Rectangle(mouth.x + face.x, mouth.y + face.y, mouth.width, mouth.height));
                    
                

                #Detect noses
                noses = []
                
                for noseCascade in self.nosesCascades:
                
                    detectedNoses = noseCascade.detectMultiScale(faceRegion, 1.1, 10)

                    for nose in detectedNoses:
                    
                        noses.append(Rectangle(nose[0] + face[0], nose[1] + face[1], 
                            nose[2], nose[3]))

                        #noses.add(new Rectangle(nose.x + face.x, nose.y + face.y, nose.width, nose.height));
                    
        return personFaces                              


#Testing stuff
if __name__ == "__main__":
    print 'Testing Face Detector'

    testimg = cv2.imread('duffs.jpg')

    faceDetector = FaceDetector()
    faces = faceDetector.Detect(testimg)

    for face in faces:
        face.Evaluate()
        print face.IsValid()
        faceTuple = face.GetFace().getTuple()
        cv2.rectangle(testimg, faceTuple[0], faceTuple[1], (255,0,0), 1)

        eyes = face.GetEyes()
        for eye in eyes:
            eyeTuple = eye.getTuple()
            cv2.rectangle(testimg, eyeTuple[0], eyeTuple[1], (255,0,0), 1)

        mouth = face.GetMouth().getTuple()
        cv2.rectangle(testimg, mouth[0], mouth[1], (255,0,0), 1)

        nose = face.GetNose().getTuple()
        cv2.rectangle(testimg, nose[0], nose[1], (255,0,0), 1)

        faceLineData = face.GetFaceLineData()
        pGen = PointGenerator.FromFactors(faceLineData[0], faceLineData[1])

        p1 = pGen.GetFromY(0)
        p2 = pGen.GetFromY(testimg.shape[0])

        cv2.line(testimg, (int(p1.x), int(p1.y)), (int(p2.x), int(p2.y)), (255,0,0), 1)

    cv2.imshow("Test Image", testimg)
    cv2.waitKey()