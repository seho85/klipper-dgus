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

from dgus.display.mask import Mask
from dgus.display.communication.communication_interface import SerialCommunication
from moonraker.websocket_interface import WebsocketInterface
from controls.moonraker_text_variable import MoonrakerTextVariable, TextVariable
from data_addresses import DataAddress

class HomeingDisplayMask(Mask):
    
    web_socket : WebsocketInterface = None

    homed_axes : TextVariable = None

    def __init__(self, mask_no, com_interface: SerialCommunication, web_sock : WebsocketInterface) -> None:
        super().__init__(mask_no, com_interface)
        self.web_socket = web_sock

        self.homed_axes = MoonrakerTextVariable(com_interface, DataAddress.HOMED_AXES, DataAddress.UNDEFINED, 9, web_sock)
        self.controls.append(self.homed_axes)
        self.homed_axes.set_klipper_data(["toolhead", "homed_axes"])