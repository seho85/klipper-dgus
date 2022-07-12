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

import json
import sys
import os
import logging
import logging.config

logger_json_file = os.path.join(os.getcwd(), "..", "config", "logging.json")
with open(logger_json_file) as json_file:
    json_data = json.load(json_file)
    logging.config.dictConfig(json_data)


from datetime import datetime, timedelta
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

from moonraker.websocket_interface import WebsocketInterface

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
    
    
    
    PRINTER_IP = "10.0.1.69"
    PORT = 7125
    websock = WebsocketInterface(PRINTER_IP, PORT)

    SERIAL_PORT = "/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0"
    serial_com = SerialCommunication(SERIAL_PORT)

    if not serial_com.read_json_config():
        print("Failure on loading Serial Configuration!")
        sys.exit(1)
    

    serial_com.register_spontaneous_callback(0x0000, emergency_stop_pressed)

    run_main_thread = True

    display = Display(serial_com)

    def handleSIGINT(signum, frame):
        #TODO: Add function in Display to retrieve active mask!
        if display._active_mask is not None:
            display._active_mask.mask_suppressed()

        websock.stop()
        websock.write_json_config()
        serial_com.stop()
        global run_main_thread
        run_main_thread = False

    signal(SIGINT, handleSIGINT)


    if websock.read_json_config():
        websock.start()
    else:
        print("Failed to read websocket configuration... Aborting..")

      
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
        display.switch_to_mask(30)
        display.switch_to_mask(0)


        while(run_main_thread):
            display.update_current_mask()
            sleep(0.2)
