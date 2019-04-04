#!/usr/bin/env python3

from state_machine import state_machine
from datetime import datetime
from gpiozero import OutputDevice, Button, Button, LED
import time
import threading

# to fix by Tuesday:
# 1. way to know if user sent an input... instead of remote_input... (display state, whether to enter user info or not)
# 2. actuator script
# 3. fix output call to app (just need to know how to send it, format is good)
# 4. read temp probe script
# 5. receive input from app (just need to know how to recieve it)

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
inactivity_time_met = 0
start_time_met = 0
off_time_met = 0
# read ports  inputs to the function
# ON_OFF = Button(4) # pin 7
# PROGRAM_R = Button(27) # pin 13
# PROGRAM_W = LED(22) # pin 15
# MANUAL_R = Button(18) # pin 12
# MANUAL_W = LED(23) # pin 16
# PROBE_R = Button(24) # pin 18
# PROBE_W = LED(25) # pin 22
# UP_R = Button(5) # pin 29
# UP_W = LED(6) # pin 31
# DOWN_R = Button(13) # pin 33
# DOWN_W = LED(19) # pin 35
# ENTER_R = Button(16) # pin 36
# ENTER_W = LED(20) # pin 38
next_state = "on_off_state"
# input from app won't act like a button, but will be a string
def inactivityMet():
    global inactivity_time_met
    inactivity_time_met = 1

def startMet():
    global start_time_met
    start_time_met = 1
	
def offMet():
    global off_time_met
    off_time_met = 1
	
def initialize_state():
    PROGRAM_R = LED(27) # pin 13
    PROGRAM_W = LED(22) # pin 15
    MANUAL_R = LED(18) # pin 12
    MANUAL_W = LED(23) # pin 16
    PROBE_R = LED(24) # pin 18
    PROBE_W = LED(25) # pin 22
    UP_R = LED(5) # pin 29
    UP_W = LED(6) # pin 31
    DOWN_R = LED(13) # pin 33
    DOWN_W = LED(19) # pin 35
    ENTER_R = LED(16) # pin 36
    ENTER_W = LED(20) # pin 38
    PROGRAM_R.on()
    PROGRAM_R.off()
    PROGRAM_W.on()
    PROGRAM_W.off()
    MANUAL_R.on()
    MANUAL_R.off()
    MANUAL_W.on()
    MANUAL_W.off()
    PROBE_R.on()
    PROBE_R.off()
    PROBE_W.on()
    PROBE_W.off()
    UP_R.on()
    UP_R.off()
    UP_W.on()
    UP_W.off()
    DOWN_R.on()
    DOWN_R.off()
    DOWN_W.on()
    DOWN_W.off()
    ENTER_R.on()
    ENTER_R.off()
    ENTER_W.on()
    ENTER_W.off()
    return("on_off_state")

def on_off_state(): #edited
    next_state = "on_off_state"
    ON_OFF = Button(4) # pin 7
    print("ON OFF STATE")
    time.sleep(0.25)

    while next_state == "on_off_state":
        #control the next state
        if ON_OFF.is_pressed:
            next_state = "sel_state"
        else:
            next_state = "on_off_state"
            
        #control the outputs of this state
        # no outputs 

    return (next_state)

def sel_state(): #edited
    next_state = "sel_state"
    time.sleep(0.25)
    global user_selection, remote_control, remote_input, inactivity_time_met, in_temp
    if not (remote_control == "yes" and remote_input != "NULL"):
        ON_OFF = Button(4) # pin 7
        PROGRAM_R = Button(27) # pin 13
        MANUAL_R = Button(18) # pin 12
        PROBE_R = Button(24) # pin 18
        # start inactivity timer
        inact_timer = threading.Timer(30.0, inactivityMet)
        inact_timer.start()
        print("SELECT STATE")
        while next_state == "sel_state":
            #control the next state
            if ON_OFF.is_pressed or inactivity_time_met == 1:
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
            inact_timer.cancel()
            inactivity_time_met = 0
	
    else:
        #control the outputs of this state
        # takes probe, manual, program
        if remote_input != "NULL":
            if in_temp["type"] == "probe":
                print("writing to the probe button...")
                PROBE_R = LED(24) # pin 18
                PROBE_W = LED(25) # pin 22
                time.sleep(.2)
                PROBE_W.on()
                PROBE_R.on()
                time.sleep(0.25)
                PROBE_W.off()
                time.sleep(0.2)
                user_selection = "probe"
                next_state = "heat_setting_state"
            elif in_temp["type"] == "program":
                print("writing to the program button...")
                PROGRAM_R = LED(27) # pin 13
                PROGRAM_W = LED(22) # pin 15
                time.sleep(0.2)
                PROGRAM_W.on()
                PROGRAM_R.on()
                time.sleep(0.25)
                PROGRAM_W.off()
                time.sleep(0.2)
                user_selection = "program"
                next_state = "cook_time_state"
            elif in_temp["type"] == "manual":
                print("writing to the manual button...")
                MANUAL_R = LED(18) # pin 12
                MANUAL_W = LED(23) # pin 16
                time.sleep(0.2)
                MANUAL_W.on()
                MANUAL_R.on()
                time.sleep(0.25)
                MANUAL_W.off()
                time.sleep(0.2)
                user_selection = "manual"
                next_state = "heat_setting_state"

    print(user_selection)
    return (next_state)

def cook_time_state(): #edited
    next_state = "cook_time_state"
    time.sleep(0.25)
    global start_time, remote_control, remote_input, user_selection, inactivity_time_met, in_cook_time
    if not (remote_control == "yes" and remote_input != "NULL"):
        ON_OFF = Button(4) # pin 7
        MANUAL_R = Button(18) # pin 12
        PROBE_R = Button(24) # pin 18
        UP_R = Button(5) # pin 29
        DOWN_R = Button(13) # pin 33
        ENTER_R = Button(16) # pin 36
        # start inactivity timer
        inact_timer = threading.Timer(30.0, inactivityMet)
        inact_timer.start()
        start_time = 7
        print("COOK TIME STATE")
        while next_state == "cook_time_state":
            #control the next state
            if ON_OFF.is_pressed:
                next_state = "on_off_state"
            elif inactivity_time_met == 1:
                next_state = "sel_state"
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
                time.sleep(0.20)
            elif DOWN_R.is_pressed:
                if start_time > 0:
                    start_time = start_time - 1
                time.sleep(0.20)
            else:
                next_state = "cook_time_state"
        inact_timer.cancel()
        inactivity_time_met = 0
		
    # remote control: set time
    else:
        UP_R = LED(5) # pin 29
        UP_W = LED(6) # pin 31
        DOWN_R = LED(13) # pin 33
        DOWN_W = LED(19) # pin 35
        ENTER_R = LED(16) # pin 36
        ENTER_W = LED(20) # pin 38
        if remote_input != "NULL":
            UP_R.on()
            DOWN_R.on()
            ENTER_R.on()
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
                time.sleep(0.25)
                UP_W.off()
                time.sleep(0.2)
                start_time = start_time + 2
                # update current hour and minute option
                [opt_hour, opt_min] = cook_time_options[start_time].split(":")
                opt_hour = int(opt_hour)
                opt_min = int(opt_min)
                time.sleep(0.75)
			
            if min == 30:
                start_time = start_time + 1
                # update current hour and minute option
                [opt_hour, opt_min] = cook_time_options[start_time].split(":")
                opt_hour = int(opt_hour)
                opt_min = int(opt_min)
					
            while hour < opt_hour:
                DOWN_W.on()
                time.sleep(0.25)
                DOWN_W.off()
                time.sleep(0.2)
                start_time = start_time - 2
                # update current hour and minute option
                [opt_hour, opt_min] = cook_time_options[start_time].split(":")
                opt_hour = int(opt_hour)
                opt_min = int(opt_min)
                time.sleep(0.75)
			
            # go to the next state
            ENTER_W.on()
            time.sleep(0.25)
            ENTER_W.off()
            time.sleep(0.2)
            next_state = "heat_setting_state"

    print(cook_time_options[start_time])
    return (next_state)

def heat_setting_state(): #edited
    next_state = "heat_setting_state"
    time.sleep(0.25)
    global user_selection, heat_selection, remote_control, remote_input, inactivity_time_met, start_time_met, in_temp
    if not (remote_control == "yes" and remote_input != "NULL"):
        ON_OFF = Button(4) # pin 7
        PROGRAM_R = Button(27) # pin 13
        MANUAL_R = Button(18) # pin 12
        PROBE_R = Button(24) # pin 18
        UP_R = Button(5) # pin 29
        DOWN_R = Button(13) # pin 33
        ENTER_R = Button(16) # pin 36
        # start inactivity timer
        inact_timer = threading.Timer(30.0, inactivityMet)
        inact_timer.start()
        # start the start timer
        start_timer = threading.Timer(20.0, startMet)
        start_timer.start()
        print("HEAT SETTING STATE")
        while next_state == "heat_setting_state":
            #control the next state
            if ON_OFF.is_pressed:
                next_state = "on_off_state"
            elif inactivity_time_met == 1 and user_selection == "probe":
                next_state = "sel_state"
            elif start_time_met == 1 and user_selection != "probe":
                next_state = "display_state"
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
                time.sleep(0.25)
            if DOWN_R.is_pressed:
                # change heat_selection
                if heat_selection == "high":
                    heat_selection = "low"
                elif heat_selection == "low":
                    heat_selection = "warm"
                else:
                    heat_selection = "high"
                time.sleep(0.25)
            inact_timer.cancel()
            inactivity_time_met = 0
            start_timer.cancel()
            start_time_met = 0
	
    else:
        #UP_R = LED(5) # pin 29
        #UP_W = LED(6) # pin 31	
        #ENTER_R = LED(16) # pin 36
        #ENTER_W = LED(20) # pin 38
        if remote_control == "yes" and remote_input != "NULL":
            #UP_R.on()
            #ENTER_R.on()
            # change heat_selection
            if in_temp["type"] == "probe":
                heat_selection = "high"
            else:
                heat_selection = in_temp["temperature"]
                UP_R = LED(5) # pin 29
                UP_W = LED(6) # pin 31
                #time.sleep(0.2)
                if heat_selection == "low":
                    UP_R.on()
                    UP_W.on()
                    time.sleep(0.25)
                elif heat_selection == "warm":
                    UP_R.on()
                    UP_W.on()
                    time.sleep(.2)
                    UP_R.off()
                    time.sleep(0.25)
                    UP_R.on()
                    time.sleep(0.25)
			
            # go to next state
            ENTER_R = LED(16) # pin 36
            ENTER_W = LED(20) # pin 38
            time.sleep(0.2)
            ENTER_R.on()
            ENTER_W.on()
            time.sleep(0.25)
            #ENTER_R.off()
            #time.sleep(0.2)
            print("Enter was pressed")
            
            if user_selection != "probe":
                next_state = "display_state"
            elif heat_selection == "warm":
                next_state = "display_state"
            else:
                next_state = "temp_setting_state"

    print(heat_selection)
    return (next_state)
	
def temp_setting_state(): #edited
	next_state = "temp_setting_state"
	time.sleep(0.25)
	global start_temp, remote_input, remote_control, user_selection, start_time_met, in_temp
	if not (remote_control == "yes" and remote_input != "NULL"):
		ON_OFF = Button(4) # pin 7
		PROGRAM_R = Button(27) # pin 13
		MANUAL_R = Button(18) # pin 12
		PROBE_R = Button(24) # pin 18
		UP_R = Button(5) # pin 29
		DOWN_R = Button(13) # pin 33
		ENTER_R = Button(16) # pin 36
		# start the start timer
		start_timer = threading.Timer(20.0, startMet)
		start_timer.start()
		print("TEMP SETTING STATE")
		while next_state == "temp_setting_state":
			#control the next state
			if ON_OFF.is_pressed:
				next_state = "on_off_state"
			elif ENTER_R.is_pressed or start_time_met == 1:
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
				time.sleep(0.25)
			elif DOWN_R.is_pressed:
				if start_temp > 140:
					start_temp = start_temp - 5
				time.sleep(0.25)
			else:
				next_state = "temp_setting_state"
		start_timer.cancel()
		start_time_met = 0
			
	else:
		#control the outputs of this state
		# takes up, down, enter, manual, program
		if remote_input != "NULL": 
			ENTER_R = LED(16) # pin 36
			ENTER_W = LED(20) # pin 38
			time.sleep(0.2)
			#ENTER_W.off()
			#ENTER_R.off()
			junk = input("waiting for something ... ")
			
			while start_temp < int(in_temp["temperature"]):
				UP_R = LED(5) # pin 29
				UP_W = LED(6) # pin 31
				UP_R.on()
				UP_W.on()
				time.sleep(0.25)
				start_temp = start_temp + 5
				UP_R.off()
					
			while start_temp > int(in_temp["temperature"]):
				DOWN_R = LED(13) # pin 33
				DOWN_W = LED(19) # pin 35
				DOWN_R.on()
				DOWN_W.on()
				time.sleep(0.25)
				DOWN_R.off()
				start_temp = start_temp - 5
				
			# got to next state
			time.sleep(0.2)
			ENTER_R.on()
			ENTER_W.on()
			time.sleep(0.25)
			#ENTER_W.off()
			ENTER_R.off()
			time.sleep(0.2)
			next_state = "display_state"

	print(start_temp)
	return (next_state)

def display_state(): #edited
	next_state = "display_state"
	time.sleep(0.25)
	global user_selection, remote_control, remote_input, heat_selection, start_temp, start_time, off_time_met, in_cook_time, in_temp
	# cooker is locally programmed, remote control can start
	print("DISPLAY STATE")
	remote_control = "yes"
	remote_input = "NULL"
	# start on/off timer
	off_timer = threading.Timer(14*60*60, offMet)
	off_timer.start()
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
	
	answer = input("Do you want to test the writing of buttons? y/n: ")
	if answer == "y":
		if user_selection == "program":
			in_temp = {"type": "manual", "temperature": "low", "measurement": "F"}
			in_cook_time = {"start_time": datetime.utcnow(), "length": "NA"}
			remote_input = "new"
		elif user_selection == "manual":
			in_temp = {"type": "probe", "temperature": "140", "measurement": "F"}
			in_cook_time = {"start_time": datetime.utcnow(), "length": "NA"}
			remote_input = "new"
		else:
			in_temp = {"type": "program", "temperature": "low", "measurement": "F"}
			in_cook_time = {"start_time": datetime.utcnow(), "length": cook_time_options[1]}
			remote_input = "new"
		time.sleep(5)
	else:
		remote_input = "NULL"
	
	# reset global variables
	user_selection = "-"
	heat_selection = "high"
	start_time = 7
	start_temp = 160

	ON_OFF = Button(4) # pin 7
	PROGRAM_R = Button(27) # pin 13
	MANUAL_R = Button(18) # pin 12
	PROBE_R = Button(24) # pin 18
	ENTER_R = Button(16) # pin 36
	while next_state == "display_state":
		#control the next state
		if ON_OFF.is_pressed:
			next_state = "on_off_state"
		elif off_time_met == 1:
			next_state = "on_off_state"
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
			# if info is given, go to the select state
			next_state = "write_state"

	off_timer.cancel()
	off_time_met = 0
	return (next_state)

def write_state():
    #UP_R = LED(5) # pin 29
    #UP_W = LED(6) # pin 31
    #DOWN_R = LED(13) # pin 33
    #DOWN_W = LED(19) # pin 35
    #ENTER_R = LED(16) # pin 36
    #ENTER_W = LED(20) # pin 38
	
    #UP_R.off()
    #UP_W.off()
    #DOWN_R.off()
    #DOWN_W.off()
    #ENTER_R.off()
    #ENTER_W.off()

    global in_temp, in_cook_time, start_temp, start_time
	# choose the cook setting
    if in_temp["type"] == "probe":
        print("writing to the probe button...")
        PROBE_R = LED(24) # pin 18
        PROBE_W = LED(25) # pin 22
        time.sleep(.2)
        PROBE_W.on()
        PROBE_R.on()
        time.sleep(0.25)
        PROBE_W.off()
        time.sleep(0.2)
        user_selection = "probe"
    elif in_temp["type"] == "program":
        print("writing to the program button...")
        PROGRAM_R = LED(27) # pin 13
        PROGRAM_W = LED(22) # pin 15
        time.sleep(0.2)
        PROGRAM_W.on()
        PROGRAM_R.on()
        time.sleep(0.25)
        PROGRAM_W.off()
        time.sleep(0.2)
        user_selection = "program"
    elif in_temp["type"] == "manual":
        print("writing to the manual button...")
        MANUAL_R = LED(18) # pin 12
        MANUAL_W = LED(23) # pin 16
        time.sleep(0.2)
        MANUAL_W.on()
        MANUAL_R.on()
        time.sleep(0.25)
        MANUAL_W.off()
        time.sleep(0.2)
        user_selection = "manual"

    # UP_W = LED(6)
    # UP_W.off()
    # UP_R = LED(5)
    # DOWN_W = LED(19)
    # DOWN_W.off()
    # DOWN_R = LED(13)
    # ENTER_W = LED(20)
    # ENTER_W.off()
    # ENTER_R = LED(16)
	junk = input("acknowledge probe was pressed :")
	# if program is chosen, go here
    if user_selection == "program":
        # get the hour and minute selection as integers
        [hour, min] = in_cook_time["length"].split(":")
        hour = int(hour)
        min = int(min)
        # get the hour and minute current option as integers
        [opt_hour, opt_min] = cook_time_options[start_time].split(":")
        opt_hour = int(opt_hour)
        opt_min = int(opt_min)
        while hour > opt_hour:
            press_up()
            time.sleep(0.25)
            press_up()
            time.sleep(0.2)
            start_time = start_time + 2
            # update current hour and minute option
            [opt_hour, opt_min] = cook_time_options[start_time].split(":")
            opt_hour = int(opt_hour)
            opt_min = int(opt_min)
            time.sleep(0.75)
		
        if min == 30:
            start_time = start_time + 1
			press_up()
            # update current hour and minute option
            [opt_hour, opt_min] = cook_time_options[start_time].split(":")
            opt_hour = int(opt_hour)
            opt_min = int(opt_min)
		
        while hour < opt_hour:
            press_down()
            time.sleep(0.25)
            press_down()
            time.sleep(0.2)
            start_time = start_time - 2
            # update current hour and minute option
            [opt_hour, opt_min] = cook_time_options[start_time].split(":")
            opt_hour = int(opt_hour)
            opt_min = int(opt_min)
            time.sleep(0.75)
        # go to the next state
        press_enter()
        time.sleep(0.25)
        next_state = "heat_setting_state"

    # choose the heat setting
    if in_temp["type"] == "probe":
        heat_selection = "high"
        time.sleep(2)
    else:
        heat_selection = in_temp["temperature"]
        #time.sleep(0.2)
        if heat_selection == "low":
            press_up()
        elif heat_selection == "warm":
            press_up()
			time.sleep(0.2)
			press_up()

	# go to next state
    time.sleep(2)
	press_enter()
    time.sleep(0.25)
    junk = input("acknowledge heat setting was passed:")
	
	# choose probe temp setting if probe is chosen
    if user_selection == "probe":
        time.sleep(0.2)
        junk = input("waiting for something ... ")
        print("start temp = ", start_temp)
        while start_temp < int(in_temp["temperature"]):
            print("pressing up")
			press_up()
            start_temp = start_temp + 5
        while start_temp > int(in_temp["temperature"]):
            print("pressing down")
			press_down()
            start_temp = start_temp - 5
        # got to next state
        time.sleep(0.2)
        press_enter()
        time.sleep(0.2)

    return ("display_state")
	
def press_up():
	UP_W = LED(6)
    UP_R = LED(5)
	UP_R.on()
	UP_W.on()
	time.sleep(0.2)
	UP_W.off()
	return()
	
def press_down():
	DOWN_W = LED(6)
    DOWN_R = LED(5)
	DOWN_R.on()
	DOWN_W.on()
	time.sleep(0.2)
	DOWN_W.off()
	return()
	
def press_enter():
	ENTER_W = LED(6)
    ENTER_R = LED(5)
	ENTER_R.on()
	ENTER_W.on()
	time.sleep(0.2)
	ENTER_W.off()
	return()

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
    m.add_state("initialize_state", initialize_state)
    m.add_state("write_state", write_state)
    m.set_start("initialize_state") #this is the start command
    print("STARTING RUN")
    m.run()
