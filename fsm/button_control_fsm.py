from state_machine import state_machine
from gpiozero import OutputDevice, Button #InputDevice

# can I set universal variable here? I want read ports for the buttons
# and  inputs from the app.. they need to be visible to almost all the
# states..
user_selection_options = ["manual", "probe", "program"]
heat_selection_options = ["_high", "_low", "_warm"]
remote_control = "no"
# read ports  inputs to the function
ON_OFF = Button(pin) 
POWER #= Button 
PROGRAM_R = Button(pin)
PROGRAM_APP #= Button 
MANUAL_R = Button(pin)
MANUAL_APP #= Button 
PROBE_R = Button(pin)
PROBE_APP #= Button 
UP_R = Button(pin)
UP_APP #= Button 
DOWN_R = Button(pin)
DOWN_APP #= Button 
ENTER_R = Button(pin)
ENTER_APP #= Button 
# internal signals  inputs to the function

# return seems to control which state is next so probably don't need 
# the clocked process to control

def idle_state:
	next_state = "idle_state"
	while next_state = "idle_state":
		#control the next state
		if POWER == high:
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
		if POWER == low:
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
		if POWER == low:
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
				PROBE_W = high
				pause(0.25)
				PROBE_W = low
				user_selection = "probe"
			elif PROGRAM_APP.is_pressed:
				PROGRAM_W = high
				pause(0.25)
				PROGRAM_W = low
				user_selection = "program"
			elif MANUAL_APP.is_pressed:
				MANUAL_W = high
				pause(0.25)
				MANUAL_W = low
				user_selection = "manual"

    return (next_state)

def cook_time_state:
	next_state = "cook_time_state"
	# start inactivity timer
	inactivity_timer.start()
	while next_state = "cook_time_state":
		#control the next state
		if POWER == low:
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
		else:
			next_state = "cook_time_state"
			
		previous_state = "cook_time_state"
		#control the outputs of this state
		# takes up, down, enter, manual, probe, program
		if remote_control = "yes": 
			if PROBE_APP.is_pressed:
				PROBE_W = high
				pause(0.25)
				PROBE_W = low
				user_selection = "probe"
			elif PROGRAM_APP.is_pressed:
				PROGRAM_W = high
				pause(0.25)
				PROGRAM_W = low
				user_selection = "program"
			elif MANUAL_APP.is_pressed:
				MANUAL_W = high
				pause(0.25)
				MANUAL_W = low
				user_selection = "manual"
			elif UP_APP.is_pressed:
				UP_W = high
				pause(0.25)
				UP_W = low
			elif DOWN_APP.is_pressed:
				DOWN_W = high
				pause(0.25)
				DOWN_W = low
			elif ENTER_APP.is_pressed:
				ENTER_W = high
				pause(0.25)
				ENTER_W = low
	
    return (next_state)

def heat_setting_state:
	next_state = "heat_setting_state"
	# start inactivity timer
	inactivity_timer.start()
	# start the start timer
	start_timer.start()
	while next_state = "heat_setting_state":
		#control the next state
		if POWER == low:
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
			elif heat_selection == "_warm":
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
			heat_selection = "_high"
		if PROBE_R.is_pressed:
			user_selection = "probe"
			heat_selection = "_high"
		if UP_R.is_pressed:
		# change heat_selection
			if heat_selection = "_high":
				heat_selection = "_low"
			elif heat_selection = "_low":
				heat_selection = "_warm"
			else:
				heat_selection = "_high"
		if DOWN_R.is_pressed:
		# change heat_selection
			if heat_selection = "_high":
				heat_selection = "_low"
			elif heat_selection = "_low":
				heat_selection = "_warm"
			else:
				heat_selection = "_high"
				
		if remote_control = "yes": 
			if PROBE_APP.is_pressed:
				PROBE_W = high
				pause(0.25)
				PROBE_W = low
				user_selection = "probe"
				heat_selection = "_high"
			elif PROGRAM_APP.is_pressed:
				PROGRAM_W = high
				pause(0.25)
				PROGRAM_W = low
			elif MANUAL_APP.is_pressed:
				MANUAL_W = high
				pause(0.25)
				MANUAL_W = low
				user_selection = "manual"
				heat_selection = "_high"
			elif UP_APP.is_pressed:
			# change heat_selection
				if heat_selection = "_high":
					heat_selection = "_low"
				elif heat_selection = "_low":
					heat_selection = "_warm"
				else:
					heat_selection = "_high"
			
				UP_W = high
				pause(0.25)
				UP_W = low
			elif DOWN_APP.is_pressed:
			# change heat_selection
				if heat_selection = "_high":
					heat_selection = "_low"
				elif heat_selection = "_low":
					heat_selection = "_warm"
				else:
					heat_selection = "_high"
			
				DOWN_W = high
				pause(0.25)
				DOWN_W = low
			elif ENTER_APP.is_pressed:
				ENTER_W = high
				pause(0.25)
				ENTER_W = low
	
    return (next_state)
	
def temp_setting_state:
	next_state = "temp_setting_state"
	# start the start timer
	start_timer.start()
	while next_state = "temp_setting_state":
		#control the next state
		if POWER == low:
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
		else
			next_state = "temp_setting_state"
			
		previous_state = "temp_setting_state"
		#control the outputs of this state
		# takes up, down, enter, manual, program
		if remote_control = "yes": 
			if PROGRAM_APP.is_pressed:
				PROGRAM_W = high
				pause(0.25)
				PROGRAM_W = low
				user_selection = "program"
			elif MANUAL_APP.is_pressed:
				MANUAL_W = high
				pause(0.25)
				MANUAL_W = low
				user_selection = "manual"
			elif UP_APP.is_pressed:
				UP_W = high
				pause(0.25)
				UP_W = low
			elif DOWN_APP.is_pressed:
				DOWN_W = high
				pause(0.25)
				DOWN_W = low
			elif ENTER_APP.is_pressed:
				ENTER_W = high
				pause(0.25)
				ENTER_W = low
	
	return (next_state)

def display_state:
	next_state = "display_state"
	# start on/off timer
	on_off_timer.start()
	while next_state = "display_state":
		#control the next state
		if POWER == low:
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
		elif PROBE_R.is_pressed:
			next_state = "heat_setting_state"
			user_selection = "probe"
		else:
			next_state = "display_state"
			
		previous_state = "display_state"
		#control the outputs of this state
		# takes probe, manual, program
		if remote_control = "yes":
			if PROBE_APP.is_pressed:
				PROBE_W = high
				pause(0.25)
				PROBE_W = low
				user_selection = "probe"
			elif PROGRAM_APP.is_pressed:
				PROGRAM_W = high
				pause(0.25)
				PROGRAM_W = low
				user_selection = "program"
			elif MANUAL_APP.is_pressed:
				MANUAL_W = high
				pause(0.25)
				MANUAL_W = low
				user_selection = "manual"
	
	return  (next_state)

def power_time_met_state:
	return  next_state

if __name__== "__main__":
    m = StateMachine 
    m.add_state("idle", idle_state)
    m.add_state("on_off", on_off_state)
    m.add_state("select", sel_state)
    m.add_state("cook_time", cook_time_state)
    m.add_state("heat_setting", heat_setting_state)
    m.add_state("temp_setting", temp_setting_state)
    m.add_state("display", display_state)
	m.add_state("power_time_met_state", None, end_state=1)
    m.set_start("idle") #this is the start command
