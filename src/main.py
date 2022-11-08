 # 
 # This file is part of python-dgus (https://github.com/seho85/python-dgus).
 # Copyright (c) 2022 Sebastian Holzgreve
 # 
 # This program is free software: you can redistribute it and/or modify  
 # it under the terms of the GNU General Public License as published by  
 # the Free Software Foundation, version 3.
 #
 # This program is distributed in the hope that it will be useful, but 
 # WITHOUT ANY WARRANTY; without even the implied warranty of 
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
 # General Public License for more details.
 #
 # You should have received a copy of the GNU General Public License 
 # along with this program. If not, see <http://www.gnu.org/licenses/>.
 #

import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config_dir', type=str, help="Path to config directory")
args = parser.parse_args()

config_dir = os.path.join(os.getcwd(), "..", "config")

if args.config_dir:
    config_dir = args.config_dir

import json
import sys
import logging
import logging.config

logger_json_file = os.path.join(config_dir, "logging.json")
with open(logger_json_file) as json_file:
    json_data = json.load(json_file)
    logging.config.dictConfig(json_data)


from signal import signal, SIGINT
from time import sleep
from dgus.display.communication.request import Request
from dgus.display.communication.protocol import build_write_vp
from dgus.display.communication.communication_interface import SerialCommunication
from dgus.display.display import Display
from dgus.display.mask import Mask


from overview_display_mask import OverviewDisplayMask
from axes_display_mask import AxesDisplayMask
from homeing_mask import HomeingDisplayMask
from tuning_mask import TuningMask
from extruder_mask import ExtruderMask
from extruder_temp_to_low_mask import ExtruderTemperatureToLowMask
from fan_display_mask import FanMask
from startup_mask import StartupMask

from moonraker.websocket_interface import WebsocketInterface
from moonraker.klippy_state import KlippyState


logger = logging.getLogger(__name__)

def emergency_stop_pressed(response : bytes):
    
    response_payload = response[7:]
    keycode = int.from_bytes(response_payload, byteorder='big')

    if keycode == 0xFFFF:
        #TODO: define ID in request_id.py
        emergeny_stop_rpc_cmd = {
            "jsonrpc": "2.0",
            "method": "printer.emergency_stop",
            "id": 4564
        }
        global websock
        websock.ws_app.send(json.dumps(emergeny_stop_rpc_cmd))
 

if __name__ == "__main__":
      
    
    
    logger.info("Using config directory: %s", config_dir)

    PRINTER_IP = "10.0.1.69"
    PORT = 7125
    websock = WebsocketInterface(PRINTER_IP, PORT)

    SERIAL_PORT = "/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0"
    serial_com = SerialCommunication(SERIAL_PORT)

    
    serial_config_file = os.path.join(config_dir, "serial_config.json")
    serial_configuration_read = serial_com.read_json_config(serial_config_file)

    websocket_config_file = os.path.join(config_dir, "websocket.json")
    websocket_configuration_read = websock.read_json_config(websocket_config_file)

    if not serial_configuration_read or not websocket_configuration_read:
        if not serial_configuration_read:
            logger.critical("Failed to read serial configuration! file: %s", serial_config_file)

        if not websocket_configuration_read:
            logger.critical("Failed to read websocket configuration! file: %s", websocket_config_file)

        sys.exit(1)
    
    serial_com.register_spontaneous_callback(0x0000, emergency_stop_pressed)

    # Triggered when serial port has been reopened (e.G. USB-TTL reconnected)
    def serial_port_state_changed(openend):

        if openend:
            print("Serial port openend...")
            act_mask = display.get_active_mask()
            
            mask_idx = 0
            if act_mask is not None:
                mask_idx = act_mask.mask_no
            
            display.switch_to_mask(mask_idx, False)
    serial_com._serial_port_com_event_changed_receiver  = serial_port_state_changed

    run_main_thread = True

    display = Display(serial_com)

    def handleSIGINT(signum, frame):
        #TODO: Add function in Display to retrieve active mask!
        if display._active_mask is not None:
            display._active_mask.mask_suppressed()

        websock.stop()
        websock.write_json_config(os.path.join(config_dir, "websocket.json"))
        serial_com.stop()
        global run_main_thread
        run_main_thread = False

    signal(SIGINT, handleSIGINT)

    websock.start()

    startupMask = StartupMask(serial_com, websock)
    display.add_mask(startupMask)
      
    overviewMask = OverviewDisplayMask(serial_com, websock)
    display.add_mask(overviewMask)
    
    mainMenuMask = Mask(30, serial_com)
    display.add_mask(mainMenuMask)

    axesMask =  AxesDisplayMask(serial_com, websock, display)
    display.add_mask(axesMask)

    tuningMask = TuningMask(serial_com, websock)
    display.add_mask(tuningMask)

    extruderMask = ExtruderMask(serial_com, websock, display)
    display.add_mask(extruderMask)

    fanMask = FanMask(serial_com, websock)
    display.add_mask(fanMask)

    homeingInProgress = HomeingDisplayMask(51, serial_com, websock)
    display.add_mask(homeingInProgress)

    extruder_temp_to_low_mask = ExtruderTemperatureToLowMask(serial_com, websock)
    display.add_mask(extruder_temp_to_low_mask)


    if serial_com.start_com_thread():
        display.read_config_data_for_all_controls()
        #display.write_config_data_for_all_controls()

        display.switch_to_mask(50)

        #display.switch_to_mask(30)
        #display.switch_to_mask(0)


    def klippy_state_changed(state : KlippyState, state_message : str):
        if state == KlippyState.READY:
            display.switch_to_mask(30, False)
            display.switch_to_mask(0)

        else:# state == KlippyState.ERROR or state == KlippyState.SHUTDOWN:
            display.switch_to_mask(50, False)

    websock.register_klippy_state_event_receiver(klippy_state_changed)

    while(run_main_thread):
        display.update_current_mask()
        sleep(0.2)
