#!/usr/bin/env python3

from os import listdir
from sys import exit


import argparse
import os
import json

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config_dir', type=str, help="Path to config directory")
args = parser.parse_args()

config_dir = os.path.join(os.getcwd(), "..", "config")

if args.config_dir:
    config_dir = args.config_dir




def determine_serial_interface():
    print("Please disconnect USB-TTL used for DGUS Display...")
    input("Press Enter to continue")


    try:
        serial_device_before_connect = listdir("/dev/serial/by-id")
    except FileNotFoundError:
        serial_device_before_connect = []

    print("\nPlease connect USB-TTL of DGUS Display")
    input("And press Enter to continue")

    serial_device_after_connect = listdir("/dev/serial/by-id")



    diff = list(set(serial_device_after_connect) - set(serial_device_before_connect))


    if len(diff) == 1:
        dev = diff[0]
        print(f"\nFound serial interface for DGUS Display: {dev}")

    else:
        print("\nDetection failed! - Aborting")
        exit(-1)


    serial_device = f'/dev/serial/by-id/{dev}'

    return serial_device


def setup_printer_ip():
    print("Is the Display connected to same machine were (MainsailOS) is running on?")
    local_machine = input("(y/n):")

    if local_machine == "y":
        printer_ip = "127.0.0.1"
    else:
        printer_ip = input("Please enter IP of MainsailOS machine:")

    print(f"\nUsing IP: {printer_ip}")
    return printer_ip

def update_serial_config(serial_device):
    serial_config_file = os.path.join(config_dir, "serial_config.json")
    json_data = {}
    try:
        with open(serial_config_file) as json_file:
            json_data = json.load(json_file)

    except FileNotFoundError:
        print("Unable to read configuration from %s", serial_config_file)
        return False

    json_data["com_interface"]["serial_port"] = serial_device


    with open(serial_config_file, "w") as json_file:
            json_file.write(json.dumps(json_data, indent=3))


    print("Updated serial configuration...")


def update_websocket_config(ip):
    websocket_config_file = os.path.join(config_dir, "websocket.json")
    json_data = {}
    try:
        with open(websocket_config_file) as json_file:
            json_data = json.load(json_file)

    except FileNotFoundError:
        print("Unable to read configuration from %s", websocket_config_file)
        return False

    json_data["websocket"]["ip"] = ip

    with open(websocket_config_file, "w") as json_file:
            json_file.write(json.dumps(json_data, indent=3))

    print("Updated websocket configuration...")





print("DGUS for Klipper - Config generation\n\n")

print("Step 1) Determine serial device for USB-TTL from Display:\n")
serial_device = determine_serial_interface()

print("\n\nStep 2) Setup Moonraker IP")
printer_ip = setup_printer_ip()


update_serial_config(serial_device)
update_websocket_config(printer_ip)
