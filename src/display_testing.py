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

from dgus.display.communication.communication_interface import SerialCommunication
from dgus.display.communication.request import Request
from dgus.display.communication.protocol import build_write_vp, build_mask_switch_request

def get_request_data_cb() -> bytes:
    return build_write_vp(0x5010, [0x00, 0x08])

def get_switch_mask_cb() -> bytes:
    return build_mask_switch_request(1)

def response_received_cb(response : bytes):
    pass

switch_mask_req = Request(get_switch_mask_cb, response_received_cb, "Switch Mask")

req = Request(get_request_data_cb, response_received_cb, "Testing")

SERIAL_PORT = "/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0"
com_interface = SerialCommunication(SERIAL_PORT)

com_interface.start_com_thread()

com_interface.queue_request(switch_mask_req)
com_interface.queue_request(req)

