from json import dumps
from dgus.display.communication.request import Request
from dgus.display.mask import Mask
from dgus.display.communication.communication_interface import SerialCommunication
from controls.moonraker_data_variable import MoonrakerDataVariable
from moonraker.websocket_interface import WebsocketInterface
from dgus.display.communication.protocol import build_write_vp
from keycodes import KeyCodes

class AxesDisplayMask(Mask):
    
    web_socket : WebsocketInterface = None

    distance : int = 10


    def __init__(self, com_interface: SerialCommunication, web_sock : WebsocketInterface) -> None:
        super().__init__(1, com_interface)
        self.web_socket = web_sock

        com_interface.register_spontaneous_callback(0x0005, self.move_distance_changed)
        com_interface.register_spontaneous_callback(0x0012, self.key_pressed)

    
        self.xpos = MoonrakerDataVariable(self._com_interface, 0x2030, 2, 0xffff, self.web_socket)
        #self.xpos.set_klipper_data(["toolhead", "position"], 0)
        self.xpos.set_klipper_data(["motion_report", "live_position"], 0)
        self.controls.append(self.xpos)

        self.ypos = MoonrakerDataVariable(self._com_interface, 0x2032, 2, 0xffff, self.web_socket)
        #self.ypos.set_klipper_data(["toolhead", "position"], 1)
        self.ypos.set_klipper_data(["motion_report", "live_position"], 1)
        self.controls.append(self.ypos)

        self.zpos = MoonrakerDataVariable(self._com_interface, 0x2034, 2, 0xffff, self.web_socket)
        #self.zpos.set_klipper_data(["toolhead", "position"], 2)
        self.zpos.set_klipper_data(["motion_report", "live_position"], 2)
        self.controls.append(self.zpos)

    def move_distance_changed(self, data):
        response_payload = data[7:]

        self.distance = int.from_bytes(response_payload, byteorder='big')

        biticon_val = 0
        
        if self.distance == 1:
            biticon_val = 1

        if self.distance == 10:
            biticon_val = 2

        if self.distance == 100:
            biticon_val = 4

        if self.distance == 1000:
            biticon_val = 8

        def send_biticon_state():
            req_bytes = build_write_vp(0x2036, biticon_val.to_bytes(byteorder='big', length=2))
            return req_bytes
            

        req = Request(send_biticon_state, None, "SendBit IconState")
        self._com_interface.queue_request(req)

        print(f'Move Distance changed to {self.distance}')


    def key_pressed(self, data):
        response_payload = data[7:]
        keycode = int.from_bytes(response_payload, byteorder='big')

        print(f'keycode: {keycode}')
        

        move_key_pressed = False
        home_key_pressed = False
        axe = "Y"
        move_sign = "-"
        move_distance = str(self.distance / 10)
        accell = 1000

        if keycode == KeyCodes.MoveXPlus:
            axe = "X"
            move_sign = "+"
            accell = 6000
            move_key_pressed = True

        if keycode == KeyCodes.MoveXMinus:
            axe = "X"
            move_sign = "-"
            accell = 6000
            move_key_pressed = True

        if keycode == KeyCodes.MoveYPlus:
            axe = "Y"
            move_sign = "+"
            accell = 6000
            move_key_pressed = True

        if keycode == KeyCodes.MoveYMinus:
            axe = "Y"
            move_sign = "-"
            accell = 6000
            move_key_pressed = True

        if keycode == KeyCodes.MoveZPlus:
            axe = "Z"
            move_sign = "+"
            accell = 1500
            move_key_pressed = True

        if keycode == KeyCodes.MoveZMinus:
            axe = "Z"
            move_sign = "-"
            accell = 1500
            move_key_pressed = True

        if keycode == KeyCodes.HomeAll or keycode == KeyCodes.HomeXY or keycode == KeyCodes.HomeZ:
            home_key_pressed = True
            
        if move_key_pressed:
            print(f'G1 {axe}{move_sign}{move_distance} F{accell}')
        
        #G91
        #G1 Z+0.1 F1500
        #G90

            move_cmd = {
                "jsonrpc": "2.0",
                "method": "printer.gcode.script",
                "params": {
                    "script": f'G91\n G1 {axe}{move_sign}{move_distance} F{accell}\n G90',
                                    
                },
                "id": 5555
            }

            self.web_socket.ws_app.send(dumps(move_cmd))

        if home_key_pressed:
            home_cmd = {
                "jsonrpc": "2.0",
                "method": "printer.gcode.script",
                "params": {
                    "script": 'G28',
                                    
                },
                "id": 5555
            }

            self.web_socket.ws_app.send(dumps(home_cmd))
