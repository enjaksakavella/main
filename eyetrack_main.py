from Eyetracker import Eyetracker
import cv2
import serial
import threading


def detectingLoop(t):
	while True:
		if t.detectBlink():
			print("blink")
			a = 0
		t.trackPupil()

def main():
	#print(threading.active_count())
	try:
		ser = serial.Serial('/dev/ttyACM0',115200) # TODO: korjaa
	except serial.serialutil.SerialException as e:
		print(e)
	
	tracker = Eyetracker()
	tracker.getBoundingRectangle()
	tracker.calibrate()
	
	print(tracker.blink_value)
	
	#tracking_thread = threading.Thread(target = detectingLoop(tracker))
	#print(threading.active_count())
	#tracking_thread.start()
	
	while True:
		
		t = tracker.detectBlink()
		if (t > 0.5):
			print("Long blink detected:",t)

		tracker.trackPupil()
		dist = tracker.pupil[0]- tracker.center[1]
		#print(dist)
		if dist > 30:
			dist = 30
		if dist < -30:
			dist = -30
		
		i = 190+dist
		#ser.write(i)
		
		#print(i)
		tracker.draw()
		
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
			
	tracker.cam.release()

	
if (__name__ == "__main__"):
	main()