import os
import cherrypy
import numpy as np
import imp

#cv2 = imp.load_dynamic('cv2','./cv2.pyd')
#cv2 = imp.load_dynamic('cv2','./cv2.so')
import cv2 #Probably pip cv2 is not opencv package

#import opencv as cv2
#import cv2-wrapper as cv2

from FaceExtractor import FaceExtractor

#import ilustra

#print 'VERSION'
#print cv2.__version__

class IndexHandler(object):
    @cherrypy.expose
    def index(self):
        return open('public/index.html')

class UploadHandler(object):
    exposed = True

    def GET(self):
        return ":D"

    def POST(self, file):
        
        print("FILE SENDED")
        print(file);
   

        #Init face extractor 
        faceExtractor = FaceExtractor()
       
        

        #TODO: Implement mode to avoid too larger files to be loaded

        # CherryPy reads the uploaded file into a temporary file;
        # file.file.read reads from that.

        data = file.file.read() #Reads temp file data

        #size = len(data) #Compute data size

        img_array = np.frombuffer(data, dtype=np.uint8)

        rgbImg = cv2.imdecode(img_array, cv2.IMREAD_UNCHANGED)

        result = faceExtractor.Extract(rgbImg)
        #result = "lucas"

        #cv2.imshow("Image", rgbImg)
        #cv2.waitKey()

        return result
     


if __name__ == '__main__':

    conf = {
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd()),
            'tools.staticdir.dir': './public'
        },

        '/upload':{
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')]
        }
    }

    webapp = IndexHandler()
    webapp.upload = UploadHandler()

    # Read port selected by the cloud for our application
    PORT = int(os.getenv('PORT', 8080))
    #PORT = 80

    # Set server port
    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': PORT})

    cherrypy.quickstart(webapp, '/', conf)