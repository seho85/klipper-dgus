import argparse
import json
import os

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config_dir', type=str, help="Path to config directory")
args = parser.parse_args()

if args.config_dir:
    config_dir = args.config_dir

else:
    print("Error: Need -c (--config_dir) parameter")



def read_json_config(serial_config_json_file):
        try:
            with open(serial_config_json_file) as json_file:
                json_data = json.load(json_file)
                return json_data
                
        except FileNotFoundError:
            print("Could not open: %s", serial_config_json_file)
            


print("Klipper for DGUS - Settings Common Parameters:\n")

websocket_json_file = os.path.join(config_dir, "websocket.json")
websocket_json = read_json_config(websocket_json_file)
ip = websocket_json["websocket"]["ip"]
port = websocket_json["websocket"]["port"]
print("websocket.json:")
print(f"Printer IP: {ip}:{port}" )


serial_config_json_file = os.path.join(config_dir, "serial_config.json")
serial_config_json = read_json_config(serial_config_json_file)

serial_port = serial_config_json["com_interface"]["serial_port"]
print("\nserial_config.json:")
print(f"Serial Port: {serial_port}")
