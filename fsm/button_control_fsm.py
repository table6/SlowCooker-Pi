#!/usr/bin/env python3

from state_machine import state_machine
from datetime import datetime
from gpiozero import OutputDevice, Button, Button, LED
import time

# to fix by Tuesday:
# 1. way to know if user sent an input... instead of remote_input... (display state, whether to enter user info or not)
# 2. 
# 3. fix output call to app (just need to know how to send it, format is good)
# 4. 
# 5. receive input from app (just need to know how to recieve it)
# 6. create timers

# universal variables
in_temp = {"type": "-", "temperature": "-", "measurement": "-"}
in_cook_time = {"start_time": "-", "length": "-"}
cook_time_options = ["00:30", "01:00", "01:30", "02:00", "02:30", "03:00", "03:30", "04:00", "04:30", "05:00", "05:30", "06:00", "06:30", "07:00", "07:30", "08:00", "08:30", "09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00"]
user_selection = "-"
heat_selection = "high"
remote_control = "no"
start_temp = 160 #degrees F
start_time = 7 #index
remote_input = "NULL"
# read ports  inputs to the function
ON_OFF = Button(4) # pin 7
PROGRAM_R = Button(27) # pin 13
PROGRAM_W = LED(22) # pin 15
MANUAL_R = Button(18) # pin 12
MANUAL_W = LED(23) # pin 16
PROBE_R = Button(24) # pin 18
PROBE_W = LED(25) # pin 22
UP_R = Button(5) # pin 29
UP_W = LED(6) # pin 31
DOWN_R = Button(13) # pin 33
DOWN_W = LED(19) # pin 35
ENTER_R = Button(16) # pin 36
ENTER_W = LED(20) # pin 38
next_state = "on_off_state"
# input from app won't act like a button, but will be a string

def on_off_state():
	next_state = "on_off_state"
	print("ON OFF STATE")
	time.sleep(1)

    # Sleep for a period of time to ignore slow cooker initialization.
    #time.sleep(1)

	while next_state == "on_off_state":
		#control the next state
		if ON_OFF.is_pressed:
			next_state = "sel_state"
		else:
			next_state = "on_off_state"
			
		#control the outputs of this state
		# no outputs 

	return (next_state)

def sel_state():
	next_state = "sel_state"
	# start inactivity timer
	# # inactivity_timer.start()
	print("SELECT STATE")
	while next_state == "sel_state":
		#control the next state
		if ON_OFF.is_pressed: ##or inactivity_timer.is_met():
			next_state = "on_off_state"
		elif PROGRAM_R.is_pressed:
			user_selection = "program"
			next_state = "cook_time_state"
		elif PROBE_R.is_pressed:
			user_selection = "probe"
			next_state = "heat_setting_state"
		elif MANUAL_R.is_pressed:
			user_selection = "manual"
			next_state = "heat_setting_state"
		else:
			next_state = "sel_state"
			
		#control the outputs of this state
		# takes probe, manual, program
		if remote_control == "yes" and remote_input != "NULL":
			if in_temp["type"] == "probe":
				PROBE_W.on()
				pause(0.25)
				PROBE_W.off()
				user_selection = "probe"
				next_state = "heat_setting_state"
			elif in_temp["type"] == "program":
				PROGRAM_W.on()
				pause(0.25)
				PROGRAM_W.off()
				user_selection = "program"
				next_state = "cook_time_state"
			elif in_temp["type"] == "manual":
				MANUAL_W.on()
				pause(0.25)
				MANUAL_W.off()
				user_selection = "manual"
				next_state = "heat_setting_state"

	return (next_state)

def cook_time_state():
	next_state = "cook_time_state"
	global start_time, remote_control, remote_input
	# start inactivity timer
	# # inactivity_timer.start()
	start_time = 7
	print("COOK TIME STATE")
	while next_state == "cook_time_state":
		#control the next state
		if ON_OFF.is_pressed:
			next_state = "on_off_state"
		##elif inactivity_timer.is_met():
		##	next_state = "sel_state"
		elif ENTER_R.is_pressed:
			next_state = "heat_setting_state"
		elif MANUAL_R.is_pressed:
			user_selection = "manual"
			next_state = "heat_setting_state"
		elif PROBE_R.is_pressed:
			user_selection = "probe"
			next_state = "heat_setting_state"
		elif UP_R.is_pressed:
			if start_time < 23:
				start_time = start_time + 1		
		elif DOWN_R.is_pressed:
			if start_time > 0:
				start_time = start_time - 1
		else:
			next_state = "cook_time_state"
			
		# remote control: set time
		if remote_control == "yes" and remote_input != "NULL":
			# get the hour and minute selection as integers
			[hour, min] = in_cook_time["length"].split(":")
			hour = int(hour)
			min = int(min)
			# get the hour and minute current option as integers
			[opt_hour, opt_min] = cook_time_options[start_time].split(":")
			opt_hour = int(opt_hour)
			opt_min = int(opt_min)
			while hour > opt_hour:
				UP_W.on()
				pause(0.25)
				UP_W.off()
				start_time = start_time + 2
				# update current hour and minute option
				[opt_hour, opt_min] = cook_time_options[start_time].split(":")
				opt_hour = int(opt_hour)
				opt_min = int(opt_min)
				pause(0.75)
			
			if min == 30:
				start_time = start_time + 1
				# update current hour and minute option
				[opt_hour, opt_min] = cook_time_options[start_time].split(":")
				opt_hour = int(opt_hour)
				opt_min = int(opt_min)
					
			while hour < opt_hour:
				DOWN_W.on()
				pause(0.25)
				DOWN_W.off()
				start_time = start_time - 2
				# update current hour and minute option
				[opt_hour, opt_min] = cook_time_options[start_time].split(":")
				opt_hour = int(opt_hour)
				opt_min = int(opt_min)
				pause(0.75)
					
			# go to the next state
				ENTER_W.on()
				pause(0.25)
				ENTER_W.off()
				next_state = "heat_setting_state"

	return (next_state)

def heat_setting_state():
	next_state = "heat_setting_state"
	global user_selection, heat_selection, remote_control, remote_input
	# start inactivity timer
	# # inactivity_timer.start()
	# start the start timer
	# # start_timer.start()
	print("HEAT SETTING STATE")
	while next_state == "heat_setting_state":
		#control the next state
		if ON_OFF.is_pressed:
			next_state = "on_off_state"
		##elif inactivity_timer.is_met() and user_selection == "probe":
		##	next_state = "sel_state"
		##elif start_timer.is_met() and user_selection != "probe":
		##	next_state = "display_state"
		elif ENTER_R.is_pressed:
			if user_selection != "probe":
				next_state = "display_state"
			elif heat_selection == "warm":
				next_state = "display_state"
			else:
				next_state = "temp_setting_state"
		elif PROGRAM_R.is_pressed:
			user_selection = "program"
			next_state = "cook_time_state"
		else:
			next_state = "heat_setting_state"
		
		#control the outputs of this state
		# takes up, down, enter, manual, probe, program
		if MANUAL_R.is_pressed:
			user_selection = "manual"
			heat_selection = "high"
		if PROBE_R.is_pressed:
			user_selection = "probe"
			heat_selection = "high"
		if UP_R.is_pressed:
		# change heat_selection
			if heat_selection == "high":
				heat_selection = "low"
			elif heat_selection == "low":
				heat_selection = "warm"
			else:
				heat_selection = "high"
		if DOWN_R.is_pressed:
		# change heat_selection
			if heat_selection == "high":
				heat_selection = "low"
			elif heat_selection == "low":
				heat_selection = "warm"
			else:
				heat_selection = "high"
				
		if remote_control == "yes" and remote_input != "NULL": 
			# change heat_selection
			if in_temp["type"] == "probe":
				heat_selection = "high"
			else:
				heat_selection = in_temp["temperature"]
				if heat_selection == "low":
					UP_W.on()
					pause(0.25)
					UP_W.off()
					pause(0.75)
				elif heat_selection == "warm":
					UP_W.on()
					pause(0.25)
					UP_W.off()
					pause(0.50)
					UP_W.on()
					pause(0.25)
					UP_W.off()
					pause(0.75)
					
			# go to next state
				ENTER_W.on()
				pause(0.25)
				ENTER_W.off()
				if user_selection != "probe":
					next_state = "display_state"
				elif heat_selection == "warm":
					next_state = "display_state"
				else:
					next_state = "temp_setting_state"

	return (next_state)
	
def temp_setting_state():
	next_state = "temp_setting_state"
	global start_temp, remote_input, remote_control
	# start the start timer
	# # start_timer.start()
	print("TEMP SETTING STATE")
	while next_state == "temp_setting_state":
		#control the next state
		if ON_OFF.is_pressed:
			next_state = "on_off_state"
		elif ENTER_R.is_pressed: ## or start_timer.is_met():
			next_state = "display_state"
		elif MANUAL_R.is_pressed:
			user_selection = "manual"
			next_state = "heat_setting_state"
		elif PROGRAM_R.is_pressed:
			user_selection = "program"
			next_state = "cook_time_state"
		elif PROBE_R.is_pressed: ######################### TAKE NOTES HERE, NOT SURE IF THIS IS WHAT HAPPENS #############################
			start_temp = 160
		elif UP_R.is_pressed:
			if start_temp < 180:
				start_temp = start_temp + 5
		elif DOWN_R.is_pressed:
			if start_temp > 140:
				start_temp = start_temp - 5
		else:
			next_state = "temp_setting_state"
			
		#control the outputs of this state
		# takes up, down, enter, manual, program
		if remote_control == "yes" and remote_input != "NULL": 
			while start_temp < in_temp["temperature"]:
				UP_W.on()
				pause(0.25)
				UP_W.off()
				start_temp = start_temp + 5
					
			while start_temp > in_temp["temperature"]:
				DOWN_W.on()
				pause(0.25)
				DOWN_W.off()
				start_temp = start_temp - 5
				
			# got to next state
				ENTER_W.on()
				pause(0.25)
				ENTER_W.off()
				next_state = "display_state"

	return (next_state)

def display_state():
	next_state = "display_state"
	global user_selection, remote_control_remote_input
	# cooker is locally programmed, remote control can start
	remote_control = "yes"
	remote_input = "NULL"
	# start on/off timer
	# # on_off_timer.start()
	# send information to the app
	# sent as [time, heat, temp]
	if user_selection == "program":
		out = {"type": "program", "temperature": heat_selection, "measurement": "F"}
		out2 = {"start_date": datetime.utcnow(), "cook_time": cook_time_options[start_time]}
	elif user_selection == "manual":
		out = {"type": "manual", "temperature": heat_selection, "measurement": "F"}
		out2 = {"start_date": datetime.utcnow(), "cook_time": "NA"}
	else:
		out = {"type": "probe", "temperature": str(start_temp), "measurement": "F"}
		out2 = {"start_date": datetime.utcnow(), "cook_time": "NA"}
	
	print("DISPLAY STATE")
	while next_state == "display_state":
		#control the next state
		if ON_OFF.is_pressed:
			next_state = "on_off_state"
		##elif on_off_timer.is_met():
		##	next_state = "on_off_state"
		elif PROGRAM_R.is_pressed:
			next_state = "cook_time_state"
			user_selection = "program"
		elif MANUAL_R.is_pressed:
			next_state = "heat_setting_state"
			user_selection = "manual"
		elif PROBE_R.is_pressed and ENTER_R.is_pressed:
            # temperature setting is changed to C, nothing to tell app
			next_state = "display_state"
		elif PROBE_R.is_pressed:
			next_state = "heat_setting_state"
			user_selection = "probe"
		else:
			next_state = "display_state"
			
		# ask for instructions
			
		#control the outputs of this state
		# takes probe, manual, program
		if remote_control == "yes" and remote_input != "NULL":
			# request info 
			# if info is given, press the necessary button
			if in_temp["type"] == "probe":
				PROBE_W.on()
				pause(0.25)
				PROBE_W.off()
				user_selection = "probe"
				next_state = "heat_setting_state"
			elif in_temp["type"] == "program":
				PROGRAM_W.on()
				pause(0.25)
				PROGRAM_W.off()
				user_selection = "program"
				next_state = "cook_time_state"
			elif in_temp["type"] == "manual":
				MANUAL_W.on()
				pause(0.25)
				MANUAL_W.off()
				user_selection = "manual"
				next_state = "heat_setting_state"

	return (next_state)

def power_time_met_state():
	return (next_state)

if __name__== "__main__":
    m = state_machine()
    m.add_state("on_off_state", on_off_state)
    m.add_state("sel_state", sel_state)
    m.add_state("cook_time_state", cook_time_state)
    m.add_state("heat_setting_state", heat_setting_state)
    m.add_state("temp_setting_state", temp_setting_state)
    m.add_state("display_state", display_state)
    m.add_state("power_time_met_state", None, end_state=1)
    m.set_start("on_off_state") #this is the start command
    print("STARTING RUN")
    m.run()
