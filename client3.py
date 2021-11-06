from __future__ import print_function
import requests
import json
import cv2
import time

addr = 'http://localhost:5000'
test_url = addr + '/api/test?value=3'

# prepare headers for http request
content_type = 'image/jpeg'
headers = {'content-type': content_type}

#img = cv2.imread('/home/darrylsf/Desktop/Motion_API/frames_college/ezgif-frame-090.jpg')

video_capture = cv2.VideoCapture('/home/darrylsf/Desktop/Motion_Detection/rt-motion-detection-opencv-python/VIRAT_S_000001.mp4')
#video_capture = cv2.VideoCapture('/home/darrylsf/Desktop/Motion_Detection/rt-motion-detection-opencv-python/test.mp4')

i = 0
FPS = int(video_capture.get(cv2.CAP_PROP_FPS))
frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
whole_time_begin = time.time()
#print(FPS)
while True:
        # Capture frame-by-frame
		ret, frame = video_capture.read()

		if frame is None:
			break
		#frame = cv2.resize(frame , (1280, 720))

        # encode image as jpeg
		_, img_encoded = cv2.imencode('.jpg', frame)
		#cv2.imshow("FRAME" , img_encoded)
		
		
		if i % FPS == 0:
		# send http request with image and receive response
			#print("VALUE: "+str(i%30))
			#print("I: "+str(i))
			#begin = time.time()
			response = requests.post(test_url, data= img_encoded.tobytes() , headers=headers)
			print(json.loads(response.text))
			#end = time.time()

			#print("Time Taken: "+str(end - begin))
		i += 1
		# decode response
		
whole_time_end = time.time()
print("Time take for whole video to inference: "+str(whole_time_end -whole_time_begin))	
print("Length of the video: "+str(frame_count/FPS))	
		
	