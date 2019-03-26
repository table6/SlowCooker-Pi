#!/usr/bin/env python3

from gpiozero import Button, LED
from time import sleep

rc = 0

def rw():
	global rc
	# use the pin as a write pin
	if rc == 1:
		w1 = LED(4)
		w2 = LED(27)
		w2.on()
		w1.on()
		sleep(0.2)
		w2.off()
		print("I pressed the button")
		slep(2)
	# use the pin as a read pin
	else:
		z = Button(4)
		hold = 1
		while hold == 1:
			if z.is_pressed:
				print("Button was pressed!")
				hold = 0
				sleep(2)

	return
	
if __name__ == "__main__":
	rw()
	rw()
	rc = 1
	rw()
	rw()
	rc = 0
	rw()
	rw()
	rc = 1
	rw()
	rw()