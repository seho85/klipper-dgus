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

from datetime import datetime, timedelta
import json
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
    serial_com.show_transmission_data = True


    """
    def send_bit_icon():
        value = 15
        val_bytes = value.to_bytes(length=2, byteorder='big')

        return build_write_vp(0x2036, val_bytes)

    serial_com.queue_request(Request(send_bit_icon, None, "Test"))

    serial_com.start_com_thread()
    """

    

    serial_com.register_spontaneous_callback(0x0000, emergency_stop_pressed)

    run_main_thread = True

    display = Display(serial_com)

    def handleSIGINT(signum, frame):
        if display.active_mask is not None:
            display.active_mask.mask_suppressed()

        websock.stop()
        websock.write_json_config()
        serial_com.stop()
        global run_main_thread
        run_main_thread = False

    signal(SIGINT, handleSIGINT)


    if websock.read_json_config():
        websock.start()

      
    overviewMask = OverviewDisplayMask(serial_com, websock)
    display.add_mask(overviewMask)
    
    mainMenuMask = Mask(30, serial_com)
    display.add_mask(mainMenuMask)

    axesMask =  AxesDisplayMask(serial_com, websock, display)
    display.add_mask(axesMask)

    tuningMask = TuningMask(serial_com, websock)
    display.add_mask(tuningMask)

    extruderMask = Mask(4, serial_com)
    display.add_mask(extruderMask)

    fanMask = Mask(5, serial_com)
    display.add_mask(fanMask)

    homeingInProgress = HomeingDisplayMask(51, serial_com, websock)
    display.add_mask(homeingInProgress)


    if serial_com.start_com_thread():
        display.read_config_data_for_all_controls()
        #display.write_config_data_for_all_controls()

        display.switch_to_mask(0, previous_mask_idx=30)

        

        """
        display.active_mask.controls[7].font_width = 24
        display.active_mask.controls[7].font_height = 44
        display.active_mask.controls[7].hor_dis = 3
        display.active_mask.controls[7].ver_dis = 1
        #display.active_mask.controls[0].text_length = 8

        display.active_mask.controls[7].send_config_data()
        """


        
        #display.active_mask.controls[0].send_data()
        

        


        while(run_main_thread):
            display.update_current_mask()
            sleep(0.2)
            
            """
            progress = websock.get_klipper_data(["virtual_sdcard", "progress"])
            duration = websock.get_klipper_data(["print_stats", "print_duration"])

            
            
            #if progress is None | duration is None:
            #    continue

            if progress >= 0.00001 and duration >= 0.0000001:

                time_total = duration / progress
                time_left = time_total - duration

                time_total_delta = timedelta(seconds=int(time_total))
                time_left_delta = timedelta(seconds=int(time_left))

                #time_total_delta = timedelta(seconds=int(time_total_delta.total_seconds()))
                #time_left_delta = timedelta(seconds=int(time_left_delta.total_seconds()))

                print(f'TotalTime: {str(time_total_delta)}')
                print(f'Time Left: {str(time_left_delta)}')

            sleep(0.5)
            """

    
