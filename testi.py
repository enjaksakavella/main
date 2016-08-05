import sfml as sf
import Serial

# Create the main window
window = sf.RenderWindow(sf.VideoMode(800, 600), "Dankdefence")

ser = serial.Serial('/dev/ttyACM0',115200)

# Start the game loop
running = True
while running:
	for event in window.events:
		if type(event) is sf.CloseEvent:
			window.close()
			break

		if type(event) is sf.KeyEvent:
			if sf.Keyboard.is_key_pressed(sf.Keyboard.LEFT):
				ser.write(jotain)
				
		if type(event) is sf.KeyEvent:
			if sf.Keyboard.is_key_pressed(sf.Keyboard.RIGHT):
				ser.write(jotain)
				
    # Clear screen, draw the text, and update the window
	window.clear()
	window.display()