import json
from dgus.display.mask import Mask
from dgus.display.communication.communication_interface import SerialCommunication
from moonraker.websocket_interface import WebsocketInterface
from dgus.display.controls.text_variable import TextVariable
from data_addresses import DataAddress
from keycodes import KeyCodes
from moonraker.request_id import WebsocktRequestId
from moonraker.klippy_state import KlippyState
from controls.moonraker_text_variable import MoonrakerTextVariable

class StartupMask(Mask):

    websock : WebsocketInterface = None

    klippy_state_text : str = ""

    KLIPPY_STATE_TEXT_LENGTH = 110
    
    def __init__(self, com_interface: SerialCommunication, websock : WebsocketInterface) -> None:
        super().__init__(50, com_interface)
        self.websock = websock

        websock.register_klippy_state_event_receiver(self.klippy_state_changed)


        klippy_state_text = TextVariable(com_interface, DataAddress.KLIPPY_STATE_TEXT, DataAddress.UNDEFINED, self.KLIPPY_STATE_TEXT_LENGTH)
        klippy_state_text.get_control_data_cb = self.get_klippy_state_text_cb
        self.controls.append(klippy_state_text)

        klippy_state = MoonrakerTextVariable(self._com_interface, DataAddress.KLIPPY_STATE, DataAddress.UNDEFINED, 24, self.websock)
        klippy_state.set_klipper_data(["server_info", "klippy_state"])
        self.controls.append(klippy_state)

        printer_state = MoonrakerTextVariable(self._com_interface, DataAddress.PRINTER_STATE, DataAddress.UNDEFINED, 24, self.websock)
        printer_state.set_klipper_data(["print_stats", "state"])
        self.controls.append(printer_state)

        com_interface.register_spontaneous_callback(DataAddress.START_MASK_BUTTON, self.button_pressed)

    def klippy_state_changed(self, state : KlippyState, state_message : str):
        self.klippy_state_text = state_message

    def get_klippy_state_text_cb(self) -> bytes:

        text = self.klippy_state_text
        text = text.replace("\n", ". ")

        
        
        if len(text) > self.KLIPPY_STATE_TEXT_LENGTH:
            text = text[:self.KLIPPY_STATE_TEXT_LENGTH]
            #print(f'KlippyStateText is been cutted after {CTRL_TEXT_LENGTH} chars...')
        
        str_data = bytearray(text.encode())

        chars_to_append = self.KLIPPY_STATE_TEXT_LENGTH - len(text)
        
        while chars_to_append > 0:
            str_data.append(0x00)
            chars_to_append -= 1

        return str_data


    def button_pressed(self, response : bytes):
        keycode = int.from_bytes(response[7:], byteorder='big', signed=False)

        if keycode == KeyCodes.FW_RESTART:
            self.send_fw_restart()

        if keycode == KeyCodes.RESTART:
            self.send_restart()


    def send_fw_restart(self):
        fw_reset_rpc_request = {
            "jsonrpc": "2.0",
            "method": "printer.firmware_restart",
            "id": WebsocktRequestId.FIRMWARE_RESTART
        }

        self.websock.ws_app.send(json.dumps(fw_reset_rpc_request))


    def send_restart(self):
        fw_reset_rpc_request = {
            "jsonrpc": "2.0",
            "method": "printer.restart",
            "id": WebsocktRequestId.RESTART
        }

        self.websock.ws_app.send(json.dumps(fw_reset_rpc_request))