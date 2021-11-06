from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2
import image_motion
import datetime
import os
import shutil
from collections import deque 
# Initialize the Flask application
list_images = deque(maxlen = 2)
list_images2 = deque(maxlen = 2)
list_images3 = deque(maxlen = 2)


app = Flask(__name__)

# route http posts to this method

@app.route('/api/test', methods=['POST'])
def test():
    r = request
    
    # convert string of image data to uint8
    nparr = np.frombuffer(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if(r.args.get('value') == '1'):
        list_images.append(img)
        print(len(list_images))
        #if(len(list_images) > 3):
        #    list_images.pop(0)
        motion_indicator = image_motion.detector(list_images , 1)

    elif(r.args.get('value') == '2'):
        list_images2.append(img)
        #if(len(list_images2) > 10):
        #    list_images2.pop(0)
        motion_indicator = image_motion.detector(list_images2 , 2)
    elif(r.args.get('value') == '3'):
        list_images3.append(img)
        #if(len(list_images3) > 10):
        #    list_images3.pop(0)
        motion_indicator = image_motion.detector(list_images3 , 3)
    
    #get timestamp for unique name
    
    #save received image
    #if not os.path.isdir('received_frames'):
    #    os.mkdir('received_frames')
    #cv2.imwrite("received_frames/received"+str(ct)+".jpg" , img)

    #path = os.getcwd()+"/received_frames/"
    #dir_list = os.listdir(path)
    #dir_list.sort()
    # call the motion detector....
    
    # build a response dict to send back to client
    response = {'message': 'Motion Present: '+str(motion_indicator)}
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")
# start flask app
app.run(host = '0.0.0.0' , port = 5000 , threaded = True)
