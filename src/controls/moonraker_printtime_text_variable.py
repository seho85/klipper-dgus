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

from datetime import timedelta
from enum import IntEnum
from dgus.display.controls.text_variable import TextVariable
from dgus.display.communication.communication_interface import SerialCommunication
#from src.moonraker.websocket_interface import WebsocketInterface

from moonraker.websocket_interface import WebsocketInterface

class PrintTimeDisplay(IntEnum):
    TOTAL_TIME = 0
    TIME_TILL_FINISH = 1

class MoonrakerPrintTimeTextVariable(TextVariable):

    web_sock : WebsocketInterface = None
    klipper_data = []
    time_type : PrintTimeDisplay = PrintTimeDisplay.TOTAL_TIME

    def __init__(self, comInterface: SerialCommunication, dataAddress: int, configAddress: int, TextLength: int, web_sock : WebsocketInterface, time_type: PrintTimeDisplay) -> None:
        super().__init__(comInterface, dataAddress, configAddress, TextLength)
        self.get_control_data_cb = self.get_text
        self.time_type = time_type
        self.web_sock = web_sock

    def set_klipper_data(self, klipper_data):
        self.klipper_data = klipper_data
        

    def get_text(self) -> bytes:

        json_obj = self.web_sock.get_klipper_data(self.klipper_data)

        text = str(json_obj)

        progress = self.web_sock.get_klipper_data(["virtual_sdcard", "progress"])
        duration = self.web_sock.get_klipper_data(["print_stats", "print_duration"])
        print_state = self.web_sock.get_klipper_data(["print_stats", "state"])

        if print_state == "printing":

            if progress >= 0.00001 and duration >= 0.0000001:

                time_total = duration / progress
                time_left = time_total - duration

                time_total_delta = timedelta(seconds=int(time_total))
                time_left_delta = timedelta(seconds=int(time_left))

                #time_total_delta = timedelta(seconds=int(time_total_delta.total_seconds()))
                #time_left_delta = timedelta(seconds=int(time_left_delta.total_seconds()))

                print(f'TotalTime: {str(time_total_delta)}')
                print(f'Time Left: {str(time_left_delta)}')

                if self.time_type == PrintTimeDisplay.TOTAL_TIME:
                    text = str(time_total_delta)

                if self.time_type == PrintTimeDisplay.TIME_TILL_FINISH:
                    text = str(time_left_delta)
            else:
                text = "00:00:00"

        else:
            text = "00:00:00"

        
        #text = "hase"

        if len(text) > self.data_length:
            text = text[:self.data_length]
            print(f'Text is been cutted after {self.data_length} chars...')
        #text_to_encode = f'{text:<{self.data_length}}'

        #str_data =bytearray(text_to_encode.encode())
        str_data =bytearray(text.encode())

        chars_to_append = self.data_length - len(text)
        
        while chars_to_append > 0:
            str_data.append(0x00)
            chars_to_append -= 1

        return str_data