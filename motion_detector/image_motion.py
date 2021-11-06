import cv2
import numpy as np
import os
from time import time
from detector import MotionDetector
from packer import pack_images
from numba import jit

@jit(nopython=True)
def filter_fun(b):
    return ((b[2] - b[0]) * (b[3] - b[1])) > 300

if __name__ == "__main__":

	
	detector = MotionDetector(bg_history=1,
                              bg_skip_frames=1,
                              movement_frames_history=2,
                              brightness_discard_level=30,
                              bg_subs_scale_percent=0.2,
                              pixel_compression_ratio=0.2,
                              group_boxes=False,
                              expansion_step=1)

	b_height = 320
	b_width = 320
	
	res = []
	avg_fps = []
	fc = dict()
	ctr = 0
	path = "/home/darrylsf/Desktop/Motion_API/frames_college/"
	dir_list = os.listdir(path)
	dir_list.sort()
	#print(dir_list)
	#print(path+dir_list[0])
	path2 = path+dir_list[0]
	#frame = cv2.imread(path2)
	#cv2.imshow('Frame' , frame)
	
	for i in dir_list:
		frame = cv2.imread('/home/darrylsf/Desktop/Motion_API/frames_college/'+i)
		frame2 = cv2.imread('/home/darrylsf/Desktop/Motion_API/frames_college/ezgif-frame-005.jpg')
		#cv2.imshow("5 FRAME" , frame2)
		print('/home/darrylsf/Desktop/Motion_API/frames_college/'+i)
		begin = time()

		boxes, frame = detector.detect(frame)
        # boxes hold all boxes around motion parts

        ## this code cuts motion areas from initial image and
        ## fills "bins" of 320x320 with such motion areas.
        ##
		results = []
        
		if boxes:
			results, box_map = pack_images(frame=frame, boxes=boxes, width=b_width, height=b_height,
                                            box_filter=filter_fun)
			text = "Yes"
            # box_map holds list of mapping between image placement in packed bins and original boxes

        ## end
		f = open("frame_counter.txt", "a")
		for b in boxes:
			cv2.rectangle(frame, (b[0], b[1]), (b[2], b[3]), (0, 0, 255), 2)
		if(len(boxes) > 0):
			text = "Yes"
			f.write("1\n")    

		else:
			text = "No"
			f.write("0\n")  

		f.close()
		end = time()
       
		it = (end - begin) * 1000
		it2 = (end - begin)
		fps = (1 / it2)
		print("FPS: "+str(fps))
		avg_fps.append(fps)
		if(len(avg_fps) == 0):
			continue
		else:
			avg = sum(avg_fps) / len(avg_fps)
		res.append(it)
		print("StdDev: %.4f" % np.std(res), "Mean: %.4f" % np.mean(res), "Last: %.4f" % it,
              "Boxes found: ", len(boxes))

		cv2.putText(frame, "Motion Detected: {}".format(text), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

		cv2.putText(frame, "Average FPS: {}".format(avg), (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
		if len(res) > 10000:
			res = []

        # idx = 0
        # for r in results:
        #      idx += 1
        #      cv2.imshow('packed_frame_%d' % idx, r)

		ctr += 1
		nc = len(results)
		if nc in fc:
			fc[nc] += 1
		else:
			fc[nc] = 0

		if ctr % 100 == 0:
			print("Total Frames: ", ctr, "Packed Frames:", fc)

		cv2.imshow('last_frame', frame)
		cv2.imshow('detect_frame', detector.detection_boxed)
		cv2.imshow('diff_frame', detector.color_movement)
		cv2.imwrite('/home/darrylsf/Desktop/Motion_API/result_frames/'+i , frame)
	
	cv2.waitKey(0) 
  
	#closing all open windows 
	cv2.destroyAllWindows() 