from GeometricElements import *
from PointGenerator import *

import math

class PersonFace:
    
    def __init__(self, faceRect):
        self.face = faceRect

        self.mouths = []
        self.evaluatedMouth = Rectangle(0,0,0,0)

        self.eyes = []
        self.evaluatedEyes = []

        self.isValid = False

        self.faceLineSlope = 0
    	self.faceLineOffset = 0


    def IsValid(self):
    	return self.isValid

    def GetFaceLineData(self):
    	return (self.faceLineSlope, self.faceLineOffset)

    def GetFace(self):
        return self.face

    def AddMouth(self, mouth):
        self.mouths.append(mouth)

    def GetMouth(self):
        return self.evaluatedMouth

    def AddEye(self, eye):
        self.eyes.append(eye)

    def GetEyes(self):
    	evEyes = []
    	for eye in self.evaluatedEyes:
    		evEyes.append(eye)
    			
        return evEyes

    def GetNose(self):
        faceLinePoint = PointGenerator.FromFactors(self.faceLineSlope, self.faceLineOffset)

        noseSize = Size(self.face.width / 7, self.face.height / 7)

        projNosePos = faceLinePoint.GetFromY(self.evaluatedMouth.y - noseSize.height)

        createdNose = Rectangle(projNosePos.x - noseSize.width / 2, 
        	projNosePos.y - noseSize.height / 2, noseSize.width, noseSize.height)

        return createdNose

    def Evaluate(self):

    	#Evaluate mouth
        self.evaluatedMouth = Rectangle(0, 0, 0, 0)

        #TODO must work a few on the mouth to choose the best one and proceed to histogram check for try to determinate skin color, eye color, hair color etc..

        for mouth in self.mouths:
        
            if mouth.y < self.face.y + self.face.height / 2:
                continue

            if self.evaluatedMouth.width > mouth.width:
                continue

            self.evaluatedMouth = mouth
        

        #Evaluate eyes
        self.evaluatedEyes = []
        
        rightCandidates = []
        leftCandidates = []

        for eye in self.eyes:
        
            #Ensure the eyes are in the upper half of the img region
            if eye.y + eye.height / 2 > self.face.y + self.face.height / 2:
                continue

            if eye.x + eye.width / 2 < self.face.x + self.face.width / 2:
                rightCandidates.append(eye)
            else:
                leftCandidates.append(eye)
        

        #get centers for each side weighted by their areas
        totalAreas = 0.0
        totalX = 0.0
        totalY = 0.0

        if len(rightCandidates) > 0:
        
            for eye in rightCandidates:
            
                eyeArea = eye.width * eye.height
                totalAreas += eyeArea

                totalX += (eye.x + eye.width / 2) * eyeArea
                totalY += (eye.y + eye.height / 2) * eyeArea
            

            rightPoint = Point(totalX / totalAreas, totalY / totalAreas)

            rightEyeSide = math.sqrt(totalAreas / len(rightCandidates))

            rightEye = Rectangle(rightPoint.x - rightEyeSide / 2,
            	rightPoint.y - rightEyeSide/ 2, rightEyeSide, rightEyeSide)

            self.evaluatedEyes.append(rightEye)
        



        if len(leftCandidates) > 0:
        
            totalAreas = 0.0
            totalX = 0.0
            totalY = 0.0

            for eye in leftCandidates:
            
                eyeArea = eye.width * eye.height
                totalAreas += eyeArea

                totalX += (eye.x + eye.width / 2) * eyeArea
                totalY += (eye.y + eye.height / 2) * eyeArea
            

            leftPoint = Point(totalX / totalAreas, totalY / totalAreas)

            leftEyeSide = math.sqrt(totalAreas / len(leftCandidates))

            leftEye = Rectangle(leftPoint.x - leftEyeSide / 2,
            	leftPoint.y - leftEyeSide / 2, leftEyeSide, leftEyeSide)

            self.evaluatedEyes.append(leftEye)
        



        #Check if it is valid
        self.isValid = False



        if len(self.evaluatedEyes) == 2:
        
            self.isValid = True

            #Get the face line data

            eye1Center = Point(self.evaluatedEyes[0].x + self.evaluatedEyes[0].width / 2,
                self.evaluatedEyes[0].y + self.evaluatedEyes[0].height / 2)

            eye2Center = Point(self.evaluatedEyes[1].x + self.evaluatedEyes[1].width / 2,
                self.evaluatedEyes[1].y + self.evaluatedEyes[1].height / 2)

            xOffset = (eye2Center.x - eye1Center.x) / 2
            yOffset = (eye2Center.y - eye1Center.y) / 2

            eyeLineCenter = Point(eye1Center.x + xOffset, eye1Center.y + yOffset)

            zeroDivFac = 1 if eye1Center.x == eye2Center.x else 0

            #Generate face line slope and offset
            aFact = (eye1Center.y - eye2Center.y) / (eye1Center.x - eye2Center.x + zeroDivFac)

            aFact = math.atan(aFact) + math.pi / 2
            aFact = math.tan(aFact)

            bFact = eyeLineCenter.y - aFact * eyeLineCenter.x

            self.faceLineSlope = aFact
            self.faceLineOffset = bFact

            #If the mouth is invalid, project a new based on the face line
            if self.evaluatedMouth.width == 0:
            
                faceLinePoint = PointGenerator.FromFactors(aFact, bFact)

                projMouthPos = faceLinePoint.GetFromY(self.face.y + self.face.height * 0.8)

                self.evaluatedMouth = Rectangle(projMouthPos.x - (self.face.width / 3) / 2, 
                	projMouthPos.y - (self.face.height / 5) / 2, self.face.width / 3, self.face.height / 5)

         



        if len(self.evaluatedEyes) == 1 and self.evaluatedMouth.width > 0:
        
            self.isValid = True

            #Project the other eye based on the mouth

            #Get the bottom mouth coords
            mouthBottomCenter = Point(self.evaluatedMouth.width / 2 + self.evaluatedMouth.x,
                self.evaluatedMouth.y + self.evaluatedMouth.height)

            #get the facetop coords
            faceTopCenter = Point(self.face.width / 2 + self.face.x, self.face.y)

            #Apply an experimental correct factor to the values
            correctFact = mouthBottomCenter.x - faceTopCenter.x
            #correctFact = correctFact * 0.5

            mouthBottomCenter.x += correctFact
            faceTopCenter.x -= correctFact

            #Get the slope of the faceline

            #In case they are the same value, add a pixel to prevent division by 0
            zeroDivFac = 1 if mouthBottomCenter.x == faceTopCenter.x else 0

            a = (mouthBottomCenter.y - faceTopCenter.y) / (mouthBottomCenter.x - faceTopCenter.x + zeroDivFac)

            #Get the offset of the face line
            b = mouthBottomCenter.y - a * mouthBottomCenter.x

            self.faceLineSlope = a
            self.faceLineOffset = b

            #Get the line function of the face
            faceLinePoint = PointGenerator.FromFactors(a, b)

            #Get the reference of the existing eye and its center point
            eyeRef = self.evaluatedEyes[0]
            eyeCenter = Point(eyeRef.x + eyeRef.width / 2, eyeRef.y + eyeRef.height / 2)

            #Get the slope of the eye line (it must be normal to the face line, so we turn it Pi/2
            aEyeFact = math.atan(a) + math.pi / 2
            aEyeFact = math.tan(aEyeFact)

            #Get the eye line offset
            bEyeFact = eyeCenter.y - aEyeFact * eyeCenter.x

            #Get the line function of the eye
            eyeLinePoint = PointGenerator.FromFactors(aEyeFact, bEyeFact)

            #Get the horizontal difference between the center of the existing eye and the face line
            diff = faceLinePoint.GetFromY(eyeCenter.y).x - eyeCenter.x

            #Get the project eye coords
            projEyePoint = eyeLinePoint.GetFromX(eyeCenter.x + diff * 2)
            
            #Get the project eye rectangle
            projEyeRect = Rectangle(projEyePoint.x - eyeRef.width / 2, 
            	projEyePoint.y - eyeRef.height / 2, eyeRef.width, eyeRef.height)

            self.evaluatedEyes.append(projEyeRect)
           

        #If the face keep invalid, put the face line on the middle of the face square
        if not self.isValid:
            self.faceLineSlope = -self.face.height / 0.01
            self.faceLineOffset = self.face.y - self.faceLineSlope * self.face.x + self.face.width / 2
        

#Testing stuff
if __name__ == '__main__':

    print "Testing PersonFace module..."
    personFace = PersonFace(Rectangle(0,0,100,100))

    personFace.Evaluate()
    print "Expecting FALSE:"
    print personFace.IsValid()


    personFace.AddEye(Rectangle(10,10,30,30))
    personFace.Evaluate()
    print "Expecting FALSE:"
    print personFace.IsValid()

    personFace.AddMouth(Rectangle(10,60,30,30))
    personFace.Evaluate()
    print "Expecting TRUE:"
    print personFace.IsValid()


    personFace.AddEye(Rectangle(90,10,30,30))
    personFace.Evaluate()
    print "Expecting TRUE:"
    print personFace.IsValid()
