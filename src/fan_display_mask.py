import json
import math
import datetime
from threading import Thread, Lock
from time import sleep

from dgus.display.communication.request import Request
from dgus.display.communication.communication_interface import SerialCommunication
from dgus.display.mask import Mask
from dgus.display.communication.protocol import build_read_vp, build_write_vp
from dgus.display.onscreen_keyboard import OnScreenKeyBoard

from moonraker.websocket_interface import WebsocketInterface
from moonraker.moonraker_request import MoonrakerRequest
from data_addresses import DataAddress
from keycodes import KeyCodes
from moonraker.request_id import WebsocktRequestId

class FanMask(Mask):

    run_fan_state_query_thread : bool = False
    fan_state_query_thread : Thread  = None
    websock : WebsocketInterface  = None

    fan_speed_mutex = Lock()

    def __init__(self, com_interface: SerialCommunication, websocket : WebsocketInterface) -> None:
        super().__init__(5, com_interface)

        com_interface.register_spontaneous_callback(DataAddress.SPONT_LED_CONTROL_BUTTON, self.led_button_pressed)
        com_interface.register_spontaneous_callback(DataAddress.SPONT_EXTRUDER_FAN_SPEED_SETPOINT_ASCII, self.received_ascii_led_setpoint)
        self.websock = websocket

    def led_button_pressed(self, response : bytes) -> None:
        keycode = int.from_bytes(response[7:], byteorder='big', signed=False)

        print(f'KeyCode {keycode}')

        if keycode == KeyCodes.LED_ON:
            print("LED ON Button")
            self.send_led_state_command(True)

        if keycode == KeyCodes.LED_OFF:
            print("LED Off Button")
            self.send_led_state_command(False)

    def received_ascii_led_setpoint(self, response : bytes):
        address = int.from_bytes(response[4:6], byteorder='big', signed=False)
        data = response[7:]
                
        fan_speed_percent = OnScreenKeyBoard.decode_numeric_oskbd_value(data)

        print(f'ASCII Decoded Setpoint {fan_speed_percent}')

        fan_speed = float(fan_speed_percent) / 100

        #with self.fan_speed_mutex:
            #self.write_fan_speed_to_display(fan_speed)
            #self.write_fan_speed_to_klipper(fan_speed)

        speed_as_int = int(fan_speed * 100)

        def get_send_fan_speed_request():
            nonlocal speed_as_int
            return build_write_vp(DataAddress.EXTRUDER_FAN_SPEED_SETPOINT, speed_as_int.to_bytes(byteorder="big", signed=False, length=2))
        

        req = Request(get_send_fan_speed_request, None, "Set FAN Speed")
        self._com_interface.queue_request(req)



    def send_led_state_command(self, led_on : bool):
        set_led_state_rpc_request = {
            "jsonrpc": "2.0",
            "method": "printer.gcode.script",
            "params": {
                "script": "DGUS_LED_OFF"
            },
            "id": WebsocktRequestId.LED_CMD
        }

        if led_on:
            set_led_state_rpc_request["params"]["script"] = "DGUS_LED_ON"

        self.websock.ws_app.send(json.dumps(set_led_state_rpc_request))


    def mask_shown(self):
        print(f"Mask {self.mask_no} is now shown")

        self.run_fan_state_query_thread = True
        self.fan_state_query_thread = Thread(target=self.query_fan_state_thread_function)
        self.fan_state_query_thread.start()
        

    def query_fan_state_thread_function(self):
        print("Query FAN State thread started...")

        begin_fan_speed = self.websock.get_klipper_data(["fan", "speed"])
        self.write_fan_speed_to_display(begin_fan_speed)

        last_fan_speed_klipper = begin_fan_speed
        last_fan_speed_display = begin_fan_speed
        
        while(self.run_fan_state_query_thread):
            fan_speed_klipper = self.websock.get_klipper_data(["fan", "speed"])
            fan_speed_display = self.read_fan_speed_from_display()

            print(f'Act  FAN Klipper: {fan_speed_klipper}')
            print(f'Last FAN Klipper: {last_fan_speed_klipper}')

            speed_in_klipper_changed = False
            speed_in_display_changed = False

            #if fan_speed_display != last_fan_speed_display:
            if not math.isclose(fan_speed_display,last_fan_speed_display, rel_tol=1e-3):
                speed_in_display_changed = True

            #if fan_speed_klipper != last_fan_speed_klipper:
            if not math.isclose(fan_speed_klipper, last_fan_speed_klipper, rel_tol=0.1):
                speed_in_klipper_changed = True

            
            with self.fan_speed_mutex:
                if speed_in_display_changed and speed_in_klipper_changed:
                    self.write_fan_speed_to_klipper(fan_speed_display)
                elif speed_in_klipper_changed:
                    self.write_fan_speed_to_display(fan_speed_klipper)
                elif speed_in_display_changed:
                    self.write_fan_speed_to_klipper(fan_speed_display)
            
            last_fan_speed_klipper = fan_speed_klipper
            last_fan_speed_display = fan_speed_display

            sleep(0.5)

        print("Query FAN State Thread finished...")

    def write_fan_speed_to_display(self, speed : float):
        fan_speed_written : bool = False

        speed_as_int = int(speed * 100)

        def get_send_fan_speed_request():
            nonlocal speed_as_int
            return build_write_vp(DataAddress.EXTRUDER_FAN_SPEED_SETPOINT, speed_as_int.to_bytes(byteorder="big", signed=False, length=2))

        def fan_speed_written_callback(data : bytes):
            nonlocal fan_speed_written
            fan_speed_written = True

        req = Request(get_send_fan_speed_request, fan_speed_written_callback, "Set FAN Speed")
        self._com_interface.queue_request(req)

        request_time_out = datetime.datetime.now() + datetime.timedelta(seconds=2)

        while not fan_speed_written:
            sleep(0.5)
            if datetime.datetime.now() > request_time_out:
                print("read_fan_speed_from_display timed out....")
                return

        print("Fan Speed was written to display...")

    def read_fan_speed_from_display(self):
        fan_speed_has_been_read : bool = False
        fan_speed : float = 0.0

        def get_read_fan_speed_request():
            return build_read_vp(DataAddress.EXTRUDER_FAN_SPEED_SETPOINT, 1)

        def fan_speed_read_callback(response : bytes):
            val = int.from_bytes(response[7:], byteorder='big')
            nonlocal fan_speed
            fan_speed = float(val) / 100
            nonlocal fan_speed_has_been_read
            fan_speed_has_been_read = True

        read_fan_speed_request = Request(get_read_fan_speed_request, fan_speed_read_callback, "Read Fan Speed")
        self._com_interface.queue_request(read_fan_speed_request)

        while not fan_speed_has_been_read:
            sleep(0.5)

        return fan_speed

    def write_fan_speed_to_klipper(self, speed : float):
        response_received = False
        
        def response_received_callback(dict):
            nonlocal response_received
            response_received = True

        def response_send_cb():
            pass
        
        if speed == 0.0:
            speed = 0.0000001
        
        cmd = f'M106 S{int(255.0 / (1.0 / speed))}'

        set_fan_speed_rpc_request = {
            "jsonrpc": "2.0",
            "method": "printer.gcode.script",
            "params": {
                "script": cmd
            },
            "id": WebsocktRequestId.SET_FAN_SPEED_CMD
        }

        #print(json.dumps(set_fan_speed_rpc_request, indent=3))
        

        moonraker_request = MoonrakerRequest(
            response_received_callback=response_received_callback,
            request_was_send_callback=response_send_cb,
            request=set_fan_speed_rpc_request
        )

        self.websock.queue_request(moonraker_request)

        while not response_received:
            sleep(0.5)

        

    def mask_suppressed(self):
        print(f'Mask {self.mask_no} is now suppressed')
        
        self.run_fan_state_query_thread = False
        def close_thread_func():
            self.fan_state_query_thread.join()

        close_thread = Thread(target=close_thread_func)
        close_thread.start()
       
        
        
