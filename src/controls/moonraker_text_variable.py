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

from sys import byteorder
from dgus.display.controls.text_variable import TextVariable
from dgus.display.communication.communication_interface import SerialCommunication
from moonraker.websocket_interface import WebsocketInterface

class MoonrakerTextVariable(TextVariable):

    web_sock : WebsocketInterface = None
    klipper_data = []

    def __init__(self, comInterface: SerialCommunication, dataAddress: int, configAddress: int, TextLength: int, web_sock : WebsocketInterface) -> None:
        super().__init__(comInterface, dataAddress, configAddress, TextLength)
        self.get_control_data_cb = self.get_text
        
        self.web_sock = web_sock

    def set_klipper_data(self, klipper_data):
        self.klipper_data = klipper_data
        

    def get_text(self) -> bytes:

        json_obj = self.web_sock.get_klipper_data(self.klipper_data)

        text = str(json_obj)

        #print(f'TextVariable Text: {text}')
               
        if len(text) > self.data_length:
            text = text[:self.data_length]
            print(f'Text is been cutted after {self.data_length} chars...')
        
        str_data =bytearray(text.encode())

        chars_to_append = self.data_length - len(text)
        
        while chars_to_append > 0:
            str_data.append(0x00)
            chars_to_append -= 1

        return str_data