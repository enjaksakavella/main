from Eyetracker import Eyetracker
import cv2
import serial
import threading
import time




def main():
	try:
		ser = serial.Serial('/dev/ttyACM0',115200) # TODO: korjaa
	except serial.serialutil.SerialException as e:
		print(e)
	
	tracker = Eyetracker()
	tracker.getBoundingRectangle()
	tracker.calibrate()
	
	print(tracker.blink_value)
	
	maxRotationVal = 40
	minRotationVal = -40
	start = time.time()
	end = time.time()
	blinktimer = 0
	while True:
		
		'''t = tracker.detectBlink()
		if (t > 0.5):
			print("Long blink detected:",t)'''
		
		end = time.time()
		dt = end-start
		if tracker.detectBlink():
			blinktimer += dt
		else:
			blinktimer = 0
		start = time.time()
		
		if blinktimer > 1:
			print(blinktimer)
		
		tracker.trackPupil()
		dist = tracker.pupil[0]- tracker.center[0]
		if dist > maxRotationVal:
			dist = maxRotationVal
		if dist < minRotationVal:
			dist = minRotationVal
		
		#print(dist)
		i = 85
		if dist < 0:
			i = i - 21*dist/minRotationVal
		if dist > 0:
			i = i + 26*dist/maxRotationVal
			
		#ser.write(i)
		
		#print(i)
		tracker.draw()
		
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
			
	tracker.cam.release()

	
if (__name__ == "__main__"):
	main()