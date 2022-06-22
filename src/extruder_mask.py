import json

from dgus.display.mask import Mask
from dgus.display.communication.communication_interface import SerialCommunication
from dgus.display.onscreen_keyboard import OnScreenKeyBoard
from dgus.display.communication.protocol import build_write_vp
from dgus.display.communication.request import Request
from dgus.display.display import Display
from keycodes import KeyCodes

from moonraker.websocket_interface import WebsocketInterface
from controls.moonraker_data_variable import MoonrakerDataVariable
from data_addresses import DataAddress
from moonraker.request_id import WebsocktRequestId

class ExtruderMask(Mask):

    web_socket : WebsocketInterface = None


    temp_extruder = MoonrakerDataVariable
    target_temp_extruder = MoonrakerDataVariable
    display : Display 


    feed_amount_setpoint : int = 1
    feed_rate_setpoint : int = 1

    def __init__(self, com_interface: SerialCommunication, web_socket : WebsocketInterface, display : Display) -> None:
        super().__init__(4, com_interface)
        self.web_socket = web_socket
        self.display = display

        #0
        self.temp_extruder = MoonrakerDataVariable(self._com_interface, DataAddress.TEMPERATURE_EXTRUDER, 2, DataAddress.UNDEFINED, self.web_socket)
        self.temp_extruder.set_klipper_data([ "extruder", "temperature"])
        self.controls.append(self.temp_extruder)

        #1
        self.target_temp_extruder = MoonrakerDataVariable(self._com_interface, DataAddress.TARGET_TEMPERATURE_EXTRUDER, 2, DataAddress.UNDEFINED, self.web_socket)
        self.target_temp_extruder.set_klipper_data([ "extruder", "target"])
        self.controls.append(self.target_temp_extruder)

        #TODO: Registering the for extruder target temperature setpoint call would lead to double executed callback... Think about executing callbacks only when page is active (should be optional)
        #self._com_interface.register_spontaneous_callback(DataAddress.SPONT_EXTRUDER_TEMP_SETPOINT , self.extruder_target_temp_data_changed)

        self._com_interface.register_spontaneous_callback(DataAddress.SPONT_EXTRUDER_FEED_AMOUNT_SETPOINT, self.extruder_feed_amount_changed)
        self._com_interface.register_spontaneous_callback(DataAddress.SPONT_EXTRUDER_FEED_RATE_SETPOINT, self.extruder_feed_rate_changed)

        self._com_interface.register_spontaneous_callback(DataAddress.SPONT_EXTRUDER_MASK_BUTTON, self.self_extruder_mask_btn_pressed)

        self.update_feed_amount_biticon(self.feed_amount_setpoint)
        self.update_feed_rate_biticon(self.feed_rate_setpoint)



    def extruder_feed_amount_changed(self, response : bytes) -> None:
        address = int.from_bytes(response[4:6], byteorder='big', signed=False)
        feed_amount_setp = int.from_bytes(response[7:], byteorder='big', signed=False)

        print(f'Feed Amount Changed: {feed_amount_setp} mm')

        self.update_feed_amount_biticon(feed_amount_setp)


    def update_feed_amount_biticon(self, setpoint_value : int) -> None:

        valid_set_point = False
        biticon_value = 0

        if setpoint_value == 1:
            valid_set_point = True
            biticon_value = 1
        
        if setpoint_value == 5:
            valid_set_point = True
            biticon_value = 2

        if setpoint_value == 10:
            valid_set_point = True
            biticon_value = 4

        if setpoint_value == 25:
            valid_set_point = True
            biticon_value = 8

        if setpoint_value == 50:
            valid_set_point = True
            biticon_value = 16

        if not valid_set_point:
            print(f'Error: Invalid Setpoint for Extruder Feed Amount ({setpoint_value}mm!)')
            return

        self.feed_amount_setpoint = setpoint_value

        def get_update_bitcon_request() -> bytes:
            nonlocal setpoint_value

            req = build_write_vp(DataAddress.FEED_AMOUNT_BITICON, biticon_value.to_bytes(byteorder='big', length=2, signed=False))
            return req

        request = Request(get_update_bitcon_request, None, "Update Feed Amount Biticon")
        self._com_interface.queue_request(request)


    def extruder_feed_rate_changed(self, response : bytes) -> None:
        address = int.from_bytes(response[4:6], byteorder='big', signed=False)
        setpoint = int.from_bytes(response[7:], byteorder='big', signed=False)

        print(f'Feed Rate Changed: {setpoint} mm/s')

        self.update_feed_rate_biticon(setpoint)


    def update_feed_rate_biticon(self, setpoint_value : int) -> None:

        valid_set_point = False
        biticon_value = 0

        if setpoint_value == 1:
            valid_set_point = True
            biticon_value = 1
        
        if setpoint_value == 2:
            valid_set_point = True
            biticon_value = 2

        if setpoint_value == 5:
            valid_set_point = True
            biticon_value = 4

        if setpoint_value == 10:
            valid_set_point = True
            biticon_value = 8

        if setpoint_value == 15:
            valid_set_point = True
            biticon_value = 16

        if not valid_set_point:
            print(f'Error: Invalid Setpoint for Extruder Feed Rate ({setpoint_value}mm/s!)')
            return

        self.feed_rate_setpoint = setpoint_value


        def get_update_bitcon_request() -> bytes:
            req = build_write_vp(DataAddress.FEED_RATE_BITICON, biticon_value.to_bytes(byteorder='big', length=2, signed=False))
            return req

        request = Request(get_update_bitcon_request, None, "Update Feed Rate Biticon")
        self._com_interface.queue_request(request)


    def self_extruder_mask_btn_pressed(self, response : bytes) -> None:
        
        keycode = int.from_bytes(response[7:], byteorder='big', signed=False)

        feed_amount_sign = ""
        if keycode == KeyCodes.EXTRUDE:
            pass

        if keycode == KeyCodes.RETRACT:
            feed_amount_sign = "-"
            pass

        extruder_temp = float(self.web_socket.get_klipper_data(["extruder", "temperature"]))
        min_extruder_temp = float(self.web_socket.get_klipper_data(["configfile", "settings", "extruder", "min_extrude_temp"]))

        if extruder_temp > min_extruder_temp:

            gcode_cmd = f"M82\nG1 E{feed_amount_sign}{self.feed_amount_setpoint} F{self.feed_rate_setpoint*60}"

            extruder_rpc_request = {
                "jsonrpc": "2.0",
                "method": "printer.gcode.script",
                "params": {
                    "script": gcode_cmd
                },
                "id": WebsocktRequestId.EXTRUDE_FILAMENT_CMD
            }

            print(json.dumps(extruder_rpc_request, indent=3))

            self.web_socket.ws_app.send(json.dumps(extruder_rpc_request))

        else:
            self.display.switch_to_mask(52, True)


        


