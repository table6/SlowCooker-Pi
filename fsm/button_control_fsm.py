#!/usr/bin/env python3

from state_machine import state_machine
from datetime import datetime
from gpiozero import OutputDevice, Button, Button, LED
from lib.mongoslowcooker import MongoSlowcookerClient
import time
import threading
import sys

# to fix by Tuesday:
# 1. way to know if user sent an input... instead of remote_input... (display state, whether to enter user info or not)
# 2. actuator script
# 3. fix output call to app (just need to know how to send it, format is good)
# 4. read temp probe script
# 5. receive input from app (just need to know how to recieve it)

# universal variables
in_temp = {"type": "-", "temperature": "-", "measurement": "-"}
in_cook_time = {"start_time": "-", "length": "-"}
cook_time_options = ["00:30", "01:00", "01:30", "02:00", "02:30", "03:00",
                     "03:30", "04:00", "04:30", "05:00", "05:30", "06:00",
                     "06:30", "07:00", "07:30", "08:00", "08:30", "09:00",
                     "09:30", "10:00", "10:30", "11:00", "11:30", "12:00"]
user_selection = "-"
heat_selection = "high"
remote_control = False
start_temp = 160  # degrees F
start_time = 7  # index
inactivity_time_met = 0
start_time_met = 0
off_time_met = 0
prog_time_met = 0
cooker_is_on = False
ACTUATOR = LED(17) # pin 11
actuator_status = 0  # 1 = actuated, 0 = not actuated
probe_pressed = 0
program_pressed = 0
manual_pressed = 0
on_off_pressed = 0

addr = "3.18.34.75"
port = "5000"
mongo_client = MongoSlowcookerClient(addr, port)
mongo_client.update_server_feed()


def inactivityMet():
    global inactivity_time_met
    inactivity_time_met = 1


def startMet():
    global start_time_met
    start_time_met = 1


def offMet():
    global off_time_met
    off_time_met = 1
	
def progMet():
	global prog_time_met
	prog_time_met = 1

def initialize_state():
    global ACTUATOR
    ACTUATOR.off()

    PROGRAM_R = LED(27)  # pin 13
    PROGRAM_W = LED(22)  # pin 15
    MANUAL_R = LED(18)  # pin 12
    MANUAL_W = LED(23)  # pin 16
    PROBE_R = LED(24)  # pin 18
    PROBE_W = LED(25)  # pin 22
    UP_R = LED(5)  # pin 29
    UP_W = LED(6)  # pin 31
    DOWN_R = LED(13)  # pin 33
    DOWN_W = LED(19)  # pin 35
    ENTER_R = LED(16)  # pin 36
    ENTER_W = LED(20)  # pin 38
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


def on_off_state():  # edited
    next_state = "on_off_state"
    ON_OFF = Button(4)  # pin 7

    global cooker_is_on, remote_control
    
    # change boolean and remote_control 
    remote_control = False
    if cooker_is_on:
        cooker_is_on = False
    else:
        cooker_is_on = True

    print("ON OFF STATE")

    time.sleep(0.1)

    while next_state == "on_off_state":
        # control the next state
        if ON_OFF.is_pressed:
            next_state = "sel_state"
        else:
            next_state = "on_off_state"

        # control the outputs of this state
        # no outputs

    return (next_state)


def sel_state():  # edited
    next_state = "sel_state"
    time.sleep(0.1)

    global user_selection, inactivity_time_met

    ON_OFF = Button(4)  # pin 7
    PROGRAM_R = Button(27)  # pin 13
    MANUAL_R = Button(18)  # pin 12
    PROBE_R = Button(24)  # pin 18

    # start inactivity timer
    inact_timer = threading.Timer(30.0, inactivityMet)
    inact_timer.start()

    print("SELECT STATE")

    while next_state == "sel_state":
        # control the next state
        if ON_OFF.is_pressed or inactivity_time_met == 1:
            next_state = "on_off_state"
        elif PROGRAM_R.is_pressed:
            user_selection = "program"
            next_state = "cook_time_state"
        elif PROBE_R.is_pressed:
            print("probe is pressed")
            user_selection = "probe"
            next_state = "heat_setting_state"
        elif MANUAL_R.is_pressed:
            user_selection = "manual"
            next_state = "heat_setting_state"
        else:
            next_state = "sel_state"

    inact_timer.cancel()
    inactivity_time_met = 0

    return (next_state)


def cook_time_state():  # edited
    next_state = "cook_time_state"
    time.sleep(0.1)

    global start_time, user_selection, inactivity_time_met

    ON_OFF = Button(4)  # pin 7
    MANUAL_R = Button(18)  # pin 12
    PROBE_R = Button(24)  # pin 18
    UP_R = Button(5)  # pin 29
    DOWN_R = Button(13)  # pin 33
    ENTER_R = Button(16)  # pin 36

    # start inactivity timer
    inact_timer = threading.Timer(30.0, inactivityMet)
    inact_timer.start()
    start_time = 7

    print("COOK TIME STATE")

    while next_state == "cook_time_state":
        # control the next state
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

    return (next_state)


def heat_setting_state():  # edited
    print("HEAT SETTING STATE")
    
    next_state = "heat_setting_state"
    time.sleep(0.1)

    global user_selection, heat_selection, inactivity_time_met, start_time_met

    if user_selection == "probe":
        timer = threading.Timer(30.0, inactivityMet)
        timer.start()
    else:
        timer = threading.Timer(20.0, startMet)
        timer.start()

    print("initializing buttons")

    ON_OFF = Button(4)  # pin 7
    PROGRAM_R = Button(27)  # pin 13
    MANUAL_R = Button(18)  # pin 12
    PROBE_R = Button(24)  # pin 18
    UP_R = Button(5)  # pin 29
    DOWN_R = Button(13)  # pin 33
    ENTER_R = Button(16)  # pin 36

    print("buttons initialized")

    while next_state == "heat_setting_state":
        # control the next state
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

        # control the outputs of this state
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

    timer.cancel()

#    inact_timer.cancel()
    inactivity_time_met = 0
#    start_timer.cancel()
    start_time_met = 0

    return (next_state)


def temp_setting_state():  # edited
    next_state = "temp_setting_state"
    time.sleep(0.1)

    global start_temp, user_selection, start_time_met

    ON_OFF = Button(4)  # pin 7
    PROGRAM_R = Button(27)  # pin 13
    MANUAL_R = Button(18)  # pin 12
    UP_R = Button(5)  # pin 29
    DOWN_R = Button(13)  # pin 33
    ENTER_R = Button(16)  # pin 36

    # start the start timer
    start_timer = threading.Timer(20.0, startMet)
    start_timer.start()

    print("TEMP SETTING STATE")

    while next_state == "temp_setting_state":
        # control the next state
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

    return (next_state)


def record_probe_press():
    global probe_pressed
    probe_pressed = 1


def record_program_press():
    global program_pressed
    program_pressed = 1


def record_manual_press():
    global manual_pressed
    manual_pressed = 1


def record_on_off_press():
    global on_off_pressed
    on_off_pressed = 1


def record_local_lid_press():
    status = ""
    if toggle_actuators() == True:
        status = "unsecure"    
    else:
        status = "secure"

    global mongo_client
    mongo_client.add_data_to_collection({"status": status}, "lid_status")


def display_state():  # edited
    next_state = "display_state"
    time.sleep(0.25)

    global user_selection, remote_control, prog_time_met, heat_selection
    global start_temp, start_time, off_time_met, in_cook_time, in_temp
    global probe_pressed, program_pressed, manual_pressed, mongo_client
    global on_off_pressed

    # cooker is locally programmed, remote control can start
    print("DISPLAY STATE")

    remote_input = False

    # start on/off timer
    off_timer = threading.Timer(14*60*60, offMet)
    off_timer.start()
	
    # start program timer
    if user_selection == "program":
        user_cook_time = in_cook_time["start_time"].split(":")
        if len(user_cook_time) > 1:
            hour = int(user_cook_time[0])
            minut = int(user_cook_time[1])
            prog_timer = threading.Timer(((hour*360)+(minut*60)), progMet)
            prog_timer.start()

    # send information to the app
    # sent as [time, heat, temp]
    out = {}
    if user_selection == "program":
        out = {"type": "program", "temperature": heat_selection,
               "measurement": "N/A"}
    elif user_selection == "manual":
        out = {"type": "manual", "temperature": heat_selection,
               "measurement": "N/A"}
    else:
        out = {"type": "probe", "temperature": str(
            start_temp), "measurement": "F"}

    out2 = {"start_time": cook_time_options[start_time]}
    out3 = {"status": "cooking"}

    mongo_client.add_data_to_collection(out, "temperature")
    mongo_client.add_data_to_collection(out2, "cook_time")
    mongo_client.add_data_to_collection(out3, "cooker_status")
   
    print("\t", str(out))
    print("\t", str(out2))
    print("\t", str(out3))

    ON_OFF = Button(4)  # pin 7
    PROGRAM_R = Button(27)  # pin 13
    MANUAL_R = Button(18)  # pin 12
    PROBE_R = Button(24)  # pin 18
    ENTER_R = Button(16)  # pin 36
    LOCAL_LID = Button(21) # pin 40

    # Register call backs so we can track button presses outside
    # of the main thread.
    PROBE_R.when_pressed = record_probe_press 
    PROGRAM_R.when_pressed = record_program_press 
    MANUAL_R.when_pressed = record_manual_press 
    LOCAL_LID.when_pressed = record_local_lid_press
    ON_OFF.when_pressed = record_on_off_press

    # reset global variables
    user_selection = "-"
    heat_selection = "high"
    remote_control = True
    start_time = 7
    start_temp = 160

    while next_state == "display_state":
        # control the next state
        if on_off_pressed == 1:
            next_state = "on_off_state"
            on_off_pressed = 0
        elif off_time_met == 1:
            next_state = "power_time_met_state"
        elif prog_time_met == 1:
            print("\tFinished cooking for ", in_cook_time[start_time], " hours.")
            mongo_client.add_data_to_collection({"status": "done"}, "cooker_status")
        elif program_pressed == 1:
            next_state = "cook_time_state"
            user_selection = "program"
            program_pressed = 0
        elif manual_pressed == 1:
            next_state = "heat_setting_state"
            user_selection = "manual"
            manual_pressed = 0
        elif PROBE_R.is_pressed and ENTER_R.is_pressed:
            # temperature setting is changed to C, nothing to tell app
            next_state = "display_state"
        elif probe_pressed == 1:
            next_state = "heat_setting_state"
            user_selection = "probe"
            probe_pressed = 0
        else:
            next_state = "display_state"

        # ask for instructions
        feed = mongo_client.update_server_feed()

        temperature_feed = feed.get("control_temperature")
        if temperature_feed is not None:
            in_temp = temperature_feed
            remote_input = True

        cook_time_feed = feed.get("control_cook_time")
        if cook_time_feed is not None:
            in_cook_time = cook_time_feed
            remote_input = True

        toggle_feed = feed.get("control_lid_status")
        if toggle_feed is not None:
            set_actuators(toggle_feed["status"])

        # control the outputs of this state
        if remote_input and remote_control:
            # if info is given, go to the select state
            next_state = "write_state"

    off_timer.cancel()
    off_time_met = 0

    return (next_state)


def write_state():
    global in_temp, in_cook_time, start_temp, start_time, user_selection
    global heat_selection

    # choose the cook setting
    if in_temp["type"] == "probe":
        PROBE_R = LED(24)  # pin 18
        PROBE_W = LED(25)  # pin 22
        time.sleep(.2)
        PROBE_W.on()
        PROBE_R.on()
        time.sleep(0.2)
        PROBE_W.off()
        time.sleep(0.2)
        user_selection = "probe"
    elif in_temp["type"] == "program":
        PROGRAM_R = LED(27)  # pin 13
        PROGRAM_W = LED(22)  # pin 15
        time.sleep(0.2)
        PROGRAM_W.on()
        PROGRAM_R.on()
        time.sleep(0.2)
        PROGRAM_W.off()
        time.sleep(0.2)
        user_selection = "program"
    elif in_temp["type"] == "manual":
        MANUAL_R = LED(18)  # pin 12
        MANUAL_W = LED(23)  # pin 16
        time.sleep(0.2)
        MANUAL_W.on()
        MANUAL_R.on()
        time.sleep(0.2)
        MANUAL_W.off()
        time.sleep(0.2)
        user_selection = "manual"

    if user_selection == "program":
        # get the hour and minute selection as integers
        user_cook_time = in_cook_time["start_time"].split(":")
        defined_time = cook_time_options[start_time].split(":")

        if len(user_cook_time) > 1 and len(defined_time) > 1:
            hour = int(user_cook_time[0])
            minut = int(user_cook_time[1])

            # get the hour and minute current option as integers
            opt_hour = int(defined_time[0])
            while hour > opt_hour:
                press_up()
                time.sleep(0.2)
                press_up()
                time.sleep(0.2)
                start_time += 2

                # update current hour and minute option
                opt_hour += 1
                time.sleep(0.2)

            if minut == 30:
                start_time = start_time + 1
                press_up()
                # update current hour and minute option

            while hour < opt_hour:
                press_down()
                time.sleep(0.2)
                press_down()
                time.sleep(0.2)
                start_time -= 2

                # update current hour and minute option
                opt_hour -= 1
                time.sleep(0.2)

            # go to the next state
            press_enter()
            time.sleep(0.2)

    # choose the heat setting
    if in_temp["type"] == "probe":
        heat_selection = "high"
        time.sleep(0.2)
    else:
        heat_selection = in_temp["temperature"]
        if heat_selection == "low":
            press_up()
        elif heat_selection == "warm":
            press_up()
            time.sleep(0.2)
            press_up()

    # go to next state
    time.sleep(0.2)
    press_enter()
    time.sleep(0.2)

    # choose probe temp setting if probe is chosen
    if user_selection == "probe":
        while start_temp < int(in_temp["temperature"]):
            press_up()
            time.sleep(0.2)
            start_temp = start_temp + 5

        while start_temp > int(in_temp["temperature"]):
            time.sleep(0.2)
            press_down()
            start_temp = start_temp - 5

        time.sleep(0.2)
        press_enter()
        time.sleep(0.2)

    return ("display_state")


def press_up():
    UP_W = LED(6)
    UP_R = LED(5)
    time.sleep(0.2)
    UP_W.on()
    UP_R.on()
    time.sleep(0.25)


def press_down():
    DOWN_W = LED(19)
    DOWN_R = LED(13)
    time.sleep(0.2)
    DOWN_W.on()
    DOWN_R.on()
    time.sleep(0.25)


def press_enter():
    ENTER_W = LED(20)
    ENTER_R = LED(16)
    time.sleep(0.2)
    ENTER_W.on()
    ENTER_R.on()
    time.sleep(0.25)
    ENTER_W.off()
    time.sleep(0.2)


def set_actuators(status):
    global ACTUATOR
    if status == "secure":
        ACTUATOR.off()
    elif status == "unsecure":
        ACTUATOR.on()

    lid_status = ""
    if ACTUATOR.is_lit == True:
        lid_status = "unsecure"    
    else:
        lid_status = "secure"

    global mongo_client
    mongo_client.add_data_to_collection({"status": lid_status}, "lid_status")


def toggle_actuators():
    global ACTUATOR
    if ACTUATOR.is_lit == True:
        ACTUATOR.off()
    else:
        ACTUATOR.on()

    return ACTUATOR.is_lit


def power_time_met_state():
    return ("on_off_state")


if __name__ == "__main__":
    try:
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
        m.set_start("initialize_state")  # this is the start command
        print("STARTING RUN")

        m.run()
    except(KeyboardInterrupt):
        sys.exit(0)
