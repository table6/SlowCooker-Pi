#!/usr/bin/python3 -u

import argparse
import sys
import socket
import json
import requests 
import datetime

# Configure argparse
parser = argparse.ArgumentParser()
parser.add_argument("-a", "--address", help="the address to contact")
parser.add_argument("-p", "--port", help="the port to use for sending")
args = parser.parse_args()

def get_address(target):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((target, 80))
    address = s.getsockname()[0]
    s.close()

    return address 

def make_json(address):
    d = {}
    d['address'] = address
    
    return json.dumps(d)

def send_address(json_data, target, port):
    http = "http://{}:{}/rpi-address".format(target, port)

    header = {'Content-Type': 'application/json'}
    r = requests.post(http, data=json_data, headers=header) 

# An address was provided.
if args.address:
    address = get_address(args.address)

    # A port was provided. Send JSON to this server on this port.
    if args.port:
        json_data = make_json(address)
        send_address(json_data, args.address, args.port)

# Otherwise, use Google's DNS.
else:
    address = get_address("8.8.8.8")
    print(address)
