from state_machine import state_machine
from gpiozero import OutputDevice, Button, InputDevice, LED

# to fix by Tuesday:
# 1. using info from the app to reprogram the cooker
# 2. call to the next state: does anything besides the name need passed that isn't a global variable?

# universal variables
# user_selection_options = ["manual", "probe", "program"]
# heat_selection_options = ["high", "low", "warm"]
user_selection = ""
heat_selection = ""
remote_control = "no"
start_temp = 160 #degrees
start_time = 4 #hours
# read ports  inputs to the function
ON_OFF = Button(pin) 
POWER = InputDevice(pin)
PROGRAM_R = Button(pin)
PROGRAM_W = LED(pin)
MANUAL_R = Button(pin)
MANUAL_W = LED(pin) 
PROBE_R = Button(pin)
PROBE_W = LED(pin) 
UP_R = Button(pin)
UP_W = LED(pin)
DOWN_R = Button(pin)
DOWN_W = LED(pin)
ENTER_R = Button(pin)
ENTER_W = LED(pin)
# input from app won't act like a button, but will be a string

# return seems to control which state is next so probably don't need 
# the clocked process to control

def idle_state:
	next_state = "idle_state"
	while next_state = "idle_state":
		#control the next state
		if POWER.value == 1: #might have to treat this input as something other than a boolean (real value?)
			next_state = "on_off_state"
		else:
			next_state = "idle_state"
			
		previous_state = "idle_state"
		
		#control the outputs of this state
		# no outputs

    return (next_state)

def on_off_state:
	next_state = "on_off_state"
	while next_state = "on_off_state":
		#control the next state
		if POWER.value == 0:
			next_state = "idle_state"
		elif ON_OFF.is_pressed:
			next_state = "sel_state"
		else:
			next_state = "on_off_state"
			
		previous_state = "on_off_state"	
		#control the outputs of this state
		# no outputs 
    
	return (next_state)

def sel_state:
	next_state = "sel_state"
	# start inactivity timer
	inactivity_timer.start()
	while next_state = "sel_state":
		#control the next state
		if POWER.value == 0:
			next_state = "idle_state"
		elif ON_OFF.is_pressed or inactivity_timer.is_met():
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
			
		previous_state = "sel_state"
		#control the outputs of this state
		# takes probe, manual, program
		if remote_control = "yes":
			if PROBE_APP.is_pressed:
				PROBE_W.on()
				pause(0.25)
				PROBE_W.off()
				user_selection = "probe"
				next_state = "heat_setting_state"
			elif PROGRAM_APP.is_pressed:
				PROGRAM_W.on()
				pause(0.25)
				PROGRAM_W.off()
				user_selection = "program"
				next_state = "cook_time_state"
			elif MANUAL_APP.is_pressed:
				MANUAL_W.on()
				pause(0.25)
				MANUAL_W.off()
				user_selection = "manual"
				next_state = "heat_setting_state"

    return (next_state)

def cook_time_state:
	next_state = "cook_time_state"
	# start inactivity timer
	inactivity_timer.start()
	while next_state = "cook_time_state":
		#control the next state
		if POWER.value == 0:
			next_state = "idle_state"
		elif ON_OFF.is_pressed:
			next_state = "on_off_state"
		elif inactivity_timer.is_met():
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
			if start_time < 12:
				start_time = start_time + .5
				
		elif DOWN_R.is_pressed:
			if start_time > .5:
				start_time = start_time - .5
				
		else:
			next_state = "cook_time_state"
			
		previous_state = "cook_time_state"
		#control the outputs of this state
		# takes up, down, enter, manual, probe, program
		if remote_control = "yes": 
			if PROBE_APP.is_pressed:
				PROBE_W.on()
				pause(0.25)
				PROBE_W.off()
				user_selection = "probe"
				next_state = "heat_setting_state"
			elif PROGRAM_APP.is_pressed:
				PROGRAM_W.on()
				pause(0.25)
				PROGRAM_W.off()
				user_selection = "program"
				start_time = 4
			elif MANUAL_APP.is_pressed:
				MANUAL_W.on()
				pause(0.25)
				MANUAL_W.off()
				user_selection = "manual"
				next_state = "heat_setting_state"
			elif UP_APP.is_pressed:
				UP_W.on()
				pause(0.25)
				UP_W.off()
				if start_time < 12:
					start_time = start_time + .5
					
			elif DOWN_APP.is_pressed:
				DOWN_W.on()
				pause(0.25)
				DOWN_W.off()
				if start_time > .5
					start_time = start_time - .5
					
			elif ENTER_APP.is_pressed:
				ENTER_W.on()
				pause(0.25)
				ENTER_W.off()
				next_state = "heat_setting_state"
	
    return (next_state)

def heat_setting_state:
	next_state = "heat_setting_state"
	# start inactivity timer
	inactivity_timer.start()
	# start the start timer
	start_timer.start()
	while next_state = "heat_setting_state":
		#control the next state
		if POWER.value == 0:
			next_state = "idle_state"
		elif ON_OFF.is_pressed:
			next_state = "on_off_state"
		elif inactivity_timer.is_met() and user_selection == "probe":
			next_state = "sel_state"
		elif start_timer.is_met() and user_selection != "probe":
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
		else
			next_state = "heat_setting_state"
			
		previous_state = "heat_setting_state"
		
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
			if heat_selection = "high":
				heat_selection = "low"
			elif heat_selection = "low":
				heat_selection = "warm"
			else:
				heat_selection = "high"
		if DOWN_R.is_pressed:
		# change heat_selection
			if heat_selection = "high":
				heat_selection = "low"
			elif heat_selection = "low":
				heat_selection = "warm"
			else:
				heat_selection = "high"
				
		if remote_control = "yes": 
			if PROBE_APP.is_pressed:
				PROBE_W.on()
				pause(0.25)
				PROBE_W.off()
				user_selection = "probe"
				heat_selection = "high"
				# doesn't change state
			elif PROGRAM_APP.is_pressed:
				PROGRAM_W.on()
				pause(0.25)
				PROGRAM_W.off()
				next_state = "cook_time_state"
			elif MANUAL_APP.is_pressed:
				MANUAL_W.on()
				pause(0.25)
				MANUAL_W.off()
				user_selection = "manual"
				heat_selection = "high"
				# doesn't change state
			elif UP_APP.is_pressed:
			# change heat_selection
			# if the selection doesn't match the cooker when remotely changed, remove this if/else
			# ... mostly likely the problem is that this if/else is running and then the UP_R/DOWN_R is triggered and changes the selection again
				if heat_selection = "high":
					heat_selection = "low"
				elif heat_selection = "low":
					heat_selection = "warm"
				else:
					heat_selection = "high"
			
				UP_W.on()
				pause(0.25)
				UP_W.off()
			elif DOWN_APP.is_pressed:
			change heat_selection
				if heat_selection = "high":
					heat_selection = "low"
				elif heat_selection = "low":
					heat_selection = "warm"
				else:
					heat_selection = "high"
			
				DOWN_W.on()
				pause(0.25)
				DOWN_W.off()
			elif ENTER_APP.is_pressed:
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
	
def temp_setting_state:
	next_state = "temp_setting_state"
	# start the start timer
	start_timer.start()
	while next_state = "temp_setting_state":
		#control the next state
		if POWER.value == 0:
			next_state = "idle_state"
		elif ON_OFF.is_pressed:
			next_state = "on_off_state"
		elif start_timer.is_met() or ENTER_R.is_pressed:
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
			if start_temp < 180
				start_temp = start_temp + 5
		elif DOWN_R.is_pressed:
			if start_temp > 140
				start_temp = start_temp - 5
		else
			next_state = "temp_setting_state"
			
		previous_state = "temp_setting_state"
		#control the outputs of this state
		# takes up, down, enter, manual, program
		if remote_control = "yes": 
			if PROBE_APP.is_pressed: ######################### TAKE NOTES HERE, NOT SURE IF THIS IS WHAT HAPPENS #############################
				PROBE_W.on()
				pause(0.25)
				PROBE_W.off()
				start_temp = 160
			if PROGRAM_APP.is_pressed:
				PROGRAM_W.on()
				pause(0.25)
				PROGRAM_W.off()
				user_selection = "program"
				next_state = "cook_time_state"
			elif MANUAL_APP.is_pressed:
				MANUAL_W.on()
				pause(0.25)
				MANUAL_W.off()
				user_selection = "manual"
				next_state = "heat_setting_state"
			elif UP_APP.is_pressed:
				UP_W.on()
				pause(0.25)
				UP_W.off()
				if start_temp < 180
					start_temp = start_temp + 5
					
			elif DOWN_APP.is_pressed:
				DOWN_W.on()
				pause(0.25)
				DOWN_W.off()
				if start_temp > 140
					start_temp = start_temp - 5
				
			elif ENTER_APP.is_pressed:
				ENTER_W.on()
				pause(0.25)
				ENTER_W.off()
				next_state = "display_state"
	
	return (next_state)

def display_state:
	next_state = "display_state"
	# cooker is locally programmed, remote control can start
	remote_control = "yes"
	# start on/off timer
	on_off_timer.start()
	# send information to the app
	# sent as [time, heat, temp]
	if user_selection == "program":
		out = [str(start_time), heat_selection, "NULL"]
	elif user_selection == "manual":
		out = ["NULL", heat_selection, "NULL"]
	else:
		out = ["NULL", heat_selection, str(start_temp)]
	
	while next_state = "display_state":
		#control the next state
		if POWER.value == 0:
			next_state = "idle_state"
		elif ON_OFF.is_pressed:
			next_state = "on_off_state"
		elif on_off_timer.is_met():
			next_state = "idle_state"
		elif PROGRAM_R.is_pressed:
			next_state = "cook_time_state"
			user_selection = "program"
		elif MANUAL_R.is_pressed:
			next_state = "heat_setting_state"
			user_selection = "manual"
		elif PROBE_R.is_pressed and ENTER_R.is_pressed:
			# do nothing
		elif PROBE_R.is_pressed:
			next_state = "heat_setting_state"
			user_selection = "probe"
		else:
			next_state = "display_state"
			
		previous_state = "display_state"
		#control the outputs of this state
		# takes probe, manual, program
		if remote_control = "yes":
			# request info 
			# if info is given, press the necessary button
			if PROBE_APP.is_pressed:
				PROBE_W.on()
				pause(0.25)
				PROBE_W.off()
				user_selection = "probe"
				next_state = "heat_setting_state"
			elif PROGRAM_APP.is_pressed:
				PROGRAM_W.on()
				pause(0.25)
				PROGRAM_W.off()
				user_selection = "program"
				next_state = "cook_time_state"
			elif MANUAL_APP.is_pressed:
				MANUAL_W.on()
				pause(0.25)
				MANUAL_W.off()
				user_selection = "manual"
				next_state = "heat_setting_state"
	
	return  (next_state)

def power_time_met_state:
	return  next_state

if __name__== "__main__":
    m = StateMachine()
    m.add_state("idle_state", idle_state)
    m.add_state("on_off_state", on_off_state)
    m.add_state("sel_state", sel_state)
    m.add_state("cook_time_state", cook_time_state)
    m.add_state("heat_setting_state", heat_setting_state)
    m.add_state("temp_setting_state", temp_setting_state)
    m.add_state("display_state", display_state)
	m.add_state("power_time_met_state", None, end_state=1)
    m.set_start("idle") #this is the start command
	m.run()
