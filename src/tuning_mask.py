from time import sleep
from dgus.display.communication.request import Request
from dgus.display.mask import Mask
from dgus.display.communication.communication_interface import SerialCommunication
from dgus.display.communication.protocol import build_read_vp, build_write_vp
import json

from controls.moonraker_data_variable import MoonrakerDataVariable
from moonraker.websocket_interface import WebsocketInterface
from controls.klipper_value_format import KlipperValueType

from threading import Thread

from moonraker.moonraker_request import MoonrakerRequest

class TuningMask(Mask):

    web_sock : WebsocketInterface = None

    speed : MoonrakerDataVariable = None
    extrusion : MoonrakerDataVariable = None
    z_offset : MoonrakerDataVariable = None

    query_slider_value_thread : Thread = None
    run_query_slider_value = False

    SPEED_FACTOR_ADDRESS = 0x5001
    EXTRUSION_FACTOR_ADDRESS = 0x5010
    Z_OFFSET_BITICON_ADDRESS = 0x5030

    SPEED_FACTOR = 0
    EXTRUSION_FACTOR = 1

    z_offset_move_distance = 0.01

    def __init__(self, com_interface: SerialCommunication, web_sock : WebsocketInterface) -> None:
        super().__init__(3, com_interface)
        self.web_sock = web_sock

        self.speed = MoonrakerDataVariable(com_interface, self.SPEED_FACTOR_ADDRESS, 2, 0xFFFF, web_sock, KlipperValueType.PERCENTAGE)
        self.speed.set_klipper_data(["gcode_move", "speed_factor"])
        self.speed.fixed_point_decimal_places = 0
        #self.controls.append(self.speed)


        self.extrusion = MoonrakerDataVariable(com_interface, self.EXTRUSION_FACTOR_ADDRESS, 2, 0xFFFF, web_sock, KlipperValueType.PERCENTAGE)
        #self.extrusion.set_klipper_data(["gcode_move", "extrude_factor"])
        self.extrusion.fixed_point_decimal_places = 0
        #self.controls.append(self.extrusion)

        self.z_offset = MoonrakerDataVariable(com_interface, 0x5020, 2, 0xFFFF, web_sock)
        self.z_offset.fixed_point_decimal_places = 3
        self.z_offset.set_klipper_data(["gcode_move", "homing_origin"], 2)
        self.controls.append(self.z_offset)


        #com_interface.register_spontaneous_callback(0x0ff1,  self.speed_factor_changed)

        com_interface.register_spontaneous_callback(0x0014, self.z_offset_distance_changed)
        com_interface.register_spontaneous_callback(0x0013, self.z_offset_button_pressed)
        com_interface.register_spontaneous_callback(0x0015, self.speed_factor_keyboard_value_entered)
        com_interface.register_spontaneous_callback(0x0016, self.extrusion_factor_keyboard_value_entered)

    def speed_factor_keyboard_value_entered(self, response):
        data = response[7:]
        speed_factor = float(self.decode_numeric_oskbd_value(data))
        print(f'SpeedFactor: Keyboard Input: {speed_factor}')

        if speed_factor >= 10 and speed_factor <= 200:
            self.write_factor_to_klipper(speed_factor / 100, self.SPEED_FACTOR)

    def extrusion_factor_keyboard_value_entered(self, response):
        data = response[7:]
        extrusion_factor = float(self.decode_numeric_oskbd_value(data))
        print(f'ExtrusionFactor: Keyboard Input: {extrusion_factor}')

        if extrusion_factor >= 10 and extrusion_factor <= 200:
            self.write_factor_to_klipper(extrusion_factor / 100, self.EXTRUSION_FACTOR)

    #TODO: Move to own module..
    def decode_numeric_oskbd_value(self, data : bytes):
        # The data entered with the onscreen keyboard arives ascii coded.
        # And 0xff is appended to terminate the string.
        # But 0xff is not ascii decodable to we just use the data before
        # the first appearance of 0xff
        new_data = bytearray()
        for byte in data:
            if byte != 0xff:
                new_data.append(byte)
            else:
                break

        temperature_str = str(new_data, encoding='ascii')
        temperature_str = temperature_str.replace(",",".")

        return temperature_str
    
    def z_offset_distance_changed(self, response):
        val = int.from_bytes(response[7:], byteorder='big')
        float_val = float(val) / 1000
        print(f'z_offset: {val} = {float_val}mm')

        biticon_bit_pattern = 0

        if val == 10:
            biticon_bit_pattern = 1
        elif val == 50:
            biticon_bit_pattern = 2

        elif val == 100:
            biticon_bit_pattern = 4

        def get_set_biticon_request():
            nonlocal biticon_bit_pattern
            return build_write_vp(self.Z_OFFSET_BITICON_ADDRESS, biticon_bit_pattern.to_bytes(byteorder='big', length=2))

        if biticon_bit_pattern != 0:
            req = Request(get_set_biticon_request, None, "Set Z-Offset Biticon")
            self._com_interface.queue_request(req)

            self.z_offset_move_distance = float_val

    def z_offset_button_pressed(self, response):
        print(f"ZOffsetButton Response {response}")
        val = int.from_bytes(response[7:], byteorder='big')

        z_offset_adjust : str = "0.0"
        if val == 0:
            print("Z-Offset Raise")
            z_offset_adjust = f'{self.z_offset_move_distance}'
        elif val == 1:
            print("Z-Offset Lower")
            z_offset_adjust = f'-{self.z_offset_move_distance}'

        
        adjust_zoffset_rpc_request = {
            "jsonrpc": "2.0",
            "method": "printer.gcode.script",
            "params": {
                "script": f'SET_GCODE_OFFSET Z_ADJUST={z_offset_adjust} MOVE=1'
            },
            "id": 8000
        }

        print(json.dumps(adjust_zoffset_rpc_request, indent=3))

        self.web_sock.ws_app.send(json.dumps(adjust_zoffset_rpc_request))


        



    def write_factor_to_display(self, address, speed_val):
        
        #actual_percentange = float(self.web_sock.json_data_modell["gcode_move"]["speed_factor"])
        act_speed_as_int = int(speed_val * 100)

        factor_wrote_to_display = False

        def get_set_factor_on_display_request():
            nonlocal act_speed_as_int
            req = build_write_vp(address, act_speed_as_int.to_bytes(byteorder='big', length=2))

            return req

        def set_factor_on_display_response(data):
            nonlocal factor_wrote_to_display
            factor_wrote_to_display = True

        req = Request(get_set_factor_on_display_request, set_factor_on_display_response, "Set Actual Speed Factor")
        self._com_interface.queue_request(req)

        while not factor_wrote_to_display:
            sleep(0.5)

        print("Factor was written to display...")

        
    def read_factor_from_display(self, address):
        factor_was_read = False
        read_factor_float  : float = 0.0

        def get_query_factor_request():
            return build_read_vp(address, 1)

        def factor_query_response(response):
            val = int.from_bytes(response[7:], byteorder='big')
            nonlocal factor_was_read
            factor_was_read = True
            nonlocal read_factor_float
            read_factor_float = float(val) / 100

        req_query_speed_factor = Request(
            request_data_func=get_query_factor_request,
            response_callback=factor_query_response,
            name="Read Factor"
        )

        self._com_interface.queue_request(req_query_speed_factor)

        while not factor_was_read:
            sleep(0.5)

        return read_factor_float

    def write_factor_to_klipper(self, speed_factor, factor_type):
        
        response_received = False

        def response_received_callback(dict):
            nonlocal response_received
            response_received = True

        def response_send_cb():
            pass
            
                
        set_speed_factor_rpc_request = {
            "jsonrpc": "2.0",
            "method": "printer.gcode.script",
            "params": {
                "script": ""
            },
            "id": 8000
        }

        if factor_type == self.SPEED_FACTOR:
            set_speed_factor_rpc_request["params"]["script"] = f"M220 S{str(speed_factor * 100)}\n"

        if factor_type == self.EXTRUSION_FACTOR:
            set_speed_factor_rpc_request["params"]["script"] = f"M221 S{str(speed_factor * 100)}\n"

        moonraker_request = MoonrakerRequest(
            response_received_callback=response_received_callback,
            request_was_send_callback=response_send_cb,
            request=set_speed_factor_rpc_request
        )

        self.web_sock.queue_request(moonraker_request)

        while not response_received:
            sleep(0.5)


        print("factor was written to klipper...")



    def mask_shown(self):
        print(f"Tuning Mask is now shown")

        self.run_query_slider_value = True
        self.query_slider_value_thread = Thread(target=self.query_slider_value_thread_function)
        self.query_slider_value_thread.start()


    def query_slider_value_thread_function(self):
                       
        begin_speed_factor = float(self.web_sock.json_data_modell["gcode_move"]["speed_factor"])
        self.write_factor_to_display(self.SPEED_FACTOR_ADDRESS, begin_speed_factor)

        last_speed_factor_klipper : float = begin_speed_factor
        last_speed_factor_display : float = begin_speed_factor

        begin_extrusion_factor = float(self.web_sock.json_data_modell["gcode_move"]["extrude_factor"])
        self.write_factor_to_display(self.EXTRUSION_FACTOR_ADDRESS, begin_extrusion_factor)

        last_extrusion_factor_klipper : float = begin_extrusion_factor
        last_extrusion_factor_display : float = begin_extrusion_factor
        
        while(self.run_query_slider_value):

            speed_factor_display = self.read_factor_from_display(self.SPEED_FACTOR_ADDRESS)
            speed_factor_klipper = float(self.web_sock.json_data_modell["gcode_move"]["speed_factor"])

            self.handle_speed_factor(speed_factor_display, speed_factor_klipper, last_speed_factor_display, last_speed_factor_klipper)

            last_speed_factor_klipper = speed_factor_klipper
            last_speed_factor_display = speed_factor_display

            extrusion_factor_klipper = float(self.web_sock.json_data_modell["gcode_move"]["extrude_factor"])
            extrusion_factor_display = speed_factor_display = self.read_factor_from_display(self.EXTRUSION_FACTOR_ADDRESS)

            self.handle_extrusion_factor(extrusion_factor_display, extrusion_factor_klipper, last_extrusion_factor_display, last_extrusion_factor_klipper)

            last_extrusion_factor_display = extrusion_factor_display
            last_extrusion_factor_klipper = extrusion_factor_klipper
         
            sleep(0.5)

    def handle_speed_factor(self, speed_factor_display, speed_factor_klipper,last_speed_factor_display, last_speed_factor_klipper):
        speed_factor_in_display_changed = False
        speed_factor_in_klipper_changed = False

        if speed_factor_display != last_speed_factor_display:
            print('SpeedFactor on display changed...')
            speed_factor_in_display_changed = True

        if speed_factor_klipper != last_speed_factor_klipper:
            print('Speedfactor in Klipper changed...')
            speed_factor_in_klipper_changed = True

        if speed_factor_in_display_changed and speed_factor_in_klipper_changed:
            print("Speedfactor in Display + Klipper changed.. Using speedfactor from Display")
            self.write_factor_to_klipper(speed_factor_display, self.SPEED_FACTOR)
        
        elif speed_factor_in_klipper_changed:
            self.write_factor_to_display(self.SPEED_FACTOR_ADDRESS,speed_factor_klipper)

        elif speed_factor_in_display_changed:
            self.write_factor_to_klipper(speed_factor_display, self.SPEED_FACTOR)

    def handle_extrusion_factor(self, extrusion_factor_display, extrusion_factor_klipper,  last_extrusion_factor_display, last_extrusion_factor_klipper):
        extrusion_factor_in_display_changed = False
        extrusion_factor_in_klipper_changed = False

        if extrusion_factor_display != last_extrusion_factor_display:
            extrusion_factor_in_display_changed = True

        if extrusion_factor_klipper != last_extrusion_factor_klipper:
            extrusion_factor_in_klipper_changed = True

        if extrusion_factor_in_display_changed and extrusion_factor_in_klipper_changed:
            self.write_factor_to_klipper(extrusion_factor_display, self.EXTRUSION_FACTOR)

        elif extrusion_factor_in_klipper_changed:
            self.write_factor_to_display(self.EXTRUSION_FACTOR_ADDRESS, extrusion_factor_klipper)

        elif extrusion_factor_in_display_changed:
            self.write_factor_to_klipper(extrusion_factor_display, self.EXTRUSION_FACTOR)



    def mask_suppressed(self):
        print(f'Tuning Mask {self.mask_no} is now suppressed')
        self.run_query_slider_value = False
        self.query_slider_value_thread.join()

    
