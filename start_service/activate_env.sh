#!/usr/bin/env bash

pi_dir="/home/pi/SlowCooker-Pi/"

source ${pi_dir}venv/bin/activate
python3 ${pi_dir}fsm/button_control_fsm.py &
