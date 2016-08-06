import cv2
import cv2.cv as cv
import numpy as np
import time

class Eyetracker:
	
	def __init__(self):
		cam = cv2.VideoCapture(1)
		self.cam = cam
		self.center = (0,0)
		self.pupil = (0,0)
		self.img = None
		self.blink_value = 0
		self.blink = False
		
	def takeSnapShot(self,gray = False, blurr = False):
		ret, frame = self.cam.read()
		if gray:
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		if blurr:
			frame = cv2.medianBlur(frame,5)
		return frame

		
	def detectBlink(self):
		x,y,w,h = self.eyeRec[0],self.eyeRec[1],self.eyeRec[2],self.eyeRec[3]
		frame = self.takeSnapShot(gray = True, blurr = True)
		ret, thresh = cv2.threshold(frame[y:(y+h),x:(x+w)],70,250,cv2.THRESH_BINARY)
		thresh = cv2.erode(thresh,np.ones((15,15),np.uint8),iterations =4)
		cv2.imshow('blinkdetection',thresh)
		#print(cv2.countNonZero(thresh))

		if cv2.countNonZero(thresh) >= self.blink_value:
			self.blink = True
			return True
		self.blink = False
		return False
		
	def getBoundingRectangle(self):
		eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
		
		eye_found = False
		
		while not eye_found:
			frame = self.takeSnapShot(gray = True, blurr = True)
			eyes = eye_cascade.detectMultiScale(frame,1.2,1,minSize=(100, 100))
			for (x,y,w,h) in eyes:
				eye = frame[y:(y+h), x:(x+w)]
				cv2.imshow('img4',eye)
				print("Is this your eye? (y/n)\n")
				if cv2.waitKey(0) & 0xFF == ord('y'): #TODO: FIX Error that occurs when eye is too near to corner.
					self.eyeRec = (x-(250-w)/2,y-(250-h)/2,250,250)
					#self.eyeRec = (x,y,w,h)
					#print(eyeRec)
					eye_found = True
					
					x2,y2,w2,h2 = self.eyeRec[0],self.eyeRec[1],self.eyeRec[2],self.eyeRec[3]
					ret, thresh = cv2.threshold(frame[y2:(y2+h2),x2:(x2+w2)],70,250,cv2.THRESH_BINARY)
					thresh = cv2.erode(thresh,np.ones((10,10),np.uint8),iterations =4)
					self.blink_value = cv2.countNonZero(thresh)+2000
					
					break

					
	def trackPupil(self):
		frame = self.takeSnapShot(gray = True, blurr = True)
		x,y,w,h = self.eyeRec[0],self.eyeRec[1],self.eyeRec[2],self.eyeRec[3]
		for i in range(40,90,2):
			ret, thresh = cv2.threshold(frame,i,250,cv2.THRESH_BINARY)
			#thresh = cv2.dilate(thresh,np.ones((5,5),np.uint8),iterations =1)
			thresh = cv2.erode(thresh,np.ones((5,5),np.uint8),iterations =4)
			thresh = cv2.dilate(thresh,np.ones((5,5),np.uint8),iterations = 2)
			cv2.imshow('pupildetection',thresh[y:(y+h),x:(x+w)])
			contours, hierarchy = cv2.findContours(thresh[y:(y+h),x:(x+w)],cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
			#print(len(contours))
			largeBlob = contours[0]
			maxArea = 0
			
			for cnt in contours:
				area = cv2.contourArea(cnt)
				if area == cv2.contourArea(contours[len(contours)-1]):
					break
				if area > maxArea:
					maxArea = area
					largeBlob = cnt
			if len(contours)>1:
				#print(i)
				'''(px,py), r = cv2.minEnclosingCircle(largeBlob)
				self.pupil = (int(x+px),int(y+py))'''
				
				
				center = cv2.moments(largeBlob)
				cx,cy = int(center['m10']/center['m00']), int(center['m01']/center['m00'])
				self.pupil = (x+cx,y+cy)
				if cv2.waitKey(1) & 0xFF == ord('l'):
					self.loadimages(i)
				#cv2.circle(frame,(int(x+xx),int(y+yy)),int(10),(0,0,255),2)
				#print(i)
				break
				
	def calibrate(self):
		print("Look forward and press any key")
		cv2.waitKey(0)
		self.trackPupil()
		self.center = self.pupil
				
	def draw(self):
		frame = self.takeSnapShot()
		if self.blink:
			string = "BLINK"
		else:
			cv2.circle(frame,(int(self.pupil[0]),int(self.pupil[1])),int(10),(0,0,255),2)
			string = str(self.pupil[0]-self.center[0])
		x,y = self.eyeRec[0],self.eyeRec[1]
		
		
		font = cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(frame,string,(x,y), font, 1,(255,255,255),2)
		cv2.line(frame,(self.center[0],self.center[1]-100),(self.center[0],self.center[1]+100),(255,0,0),5)
		cv2.imshow('img1',frame)
		
		
	def loadimages(self,t):
		x,y,w,h = self.eyeRec[0],self.eyeRec[1],self.eyeRec[2],self.eyeRec[3]
		image1 = self.takeSnapShot()
		gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
		blur1 = cv2.medianBlur(gray1,5)
		ret, thresh1 = cv2.threshold(blur1,t,250,cv2.THRESH_BINARY)
		thresh2 = cv2.erode(thresh1,np.ones((5,5),np.uint8),iterations =4)
		thresh3 = cv2.dilate(thresh2,np.ones((5,5),np.uint8),iterations =2)
		cv2.imwrite('image1.jpeg',image1)
		cv2.imwrite('gray1.jpeg',gray1)
		cv2.imwrite('blur1.jpeg',blur1)
		cv2.imwrite('thresh1.jpeg',thresh1[y:(y+h),x:(x+w)])
		cv2.imwrite('thresh2.jpeg',thresh2[y:(y+h),x:(x+w)])
		cv2.imwrite('thresh3.jpeg',thresh3[y:(y+h),x:(x+w)])
		