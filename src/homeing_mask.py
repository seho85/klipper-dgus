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