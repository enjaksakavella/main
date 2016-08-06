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
	
	#print(tracker.blink_value)
	
	maxRotationVal = 40
	minRotationVal = -40
	start = time.time()
	end = time.time()
	blinktimer = 0
	forwardmode = False
	
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
		
		#print(blinktimer)
		if blinktimer > 0.5:
			if forwardmode:
				forwardmode = False
			else:
				forwardmode = True
			blinktimer = -9999
		r = 192
		f = 64
		
		if not tracker.blink:
			tracker.trackPupil()
			dist = tracker.pupil[0]- tracker.center[0]
			if dist > maxRotationVal:
				dist = maxRotationVal
			if dist < minRotationVal:
				dist = minRotationVal

			#print(dist)
			if dist < 0:
				r = r - 63*dist/minRotationVal
			if dist > 0:
				r = r + 63*dist/maxRotationVal
			if forwardmode:
				print("FORWAAAAAARD")
				f = 80
			
			
		#ser.write(chr(r))
		#ser.write(chr(f))
		
		print(r)
		tracker.draw()
		
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
			
	tracker.cam.release()

	
if (__name__ == "__main__"):
	main()