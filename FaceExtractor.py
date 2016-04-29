import json
import cv2

from FaceDetector import *
from PointGenerator import *

class FaceExtractor:

	def __init__(self):
		self.faceDetector = FaceDetector()

	def Extract(self, receivedImage):

		personFaces = self.faceDetector.Detect(receivedImage)

		jsonFaces = []

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

			faceRectJson = rectangleToJson(faceRect)
			mouthRectJson = rectangleToJson(mouthRect)
			noseRectJson = rectangleToJson(noseRect)

			eyesJson = []

			for eye in eyesRects:
				eyeJson = rectangleToJson(eye)
				eyesJson.append(eyeJson)


			faceLineJson = []
			faceLineJson.append(faceLineData[0])
			faceLineJson.append(faceLineData[1])

			faceJson = {
				"face": faceRectJson,
				"mouth": mouthRectJson,
				"nose": noseRectJson,
				"eyes": eyesJson,
				"line": faceLineJson
			}

			jsonFaces.append(faceJson)

		#End For loop


		imageSize = {
			"width": receivedImage.shape[1],
			"height": receivedImage.shape[0]
		}

		imageMetaData = {
			"faces": jsonFaces,
			"size": imageSize
		}

		return json.dumps(imageMetaData)


def rectangleToJson(rect):
	return { 'x': rect.x, 'y': rect.y, 'width': rect.width, 'height': rect.height }  

#Module Test
if __name__ == "__main__":
	print 'Testing Face Extractor module'

	fExtractor = FaceExtractor()

	testimg = cv2.imread('test.jpg')

	result = fExtractor.Extract(testimg)
	print result
