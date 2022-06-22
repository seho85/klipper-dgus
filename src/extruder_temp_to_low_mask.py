from dgus.display.mask import Mask
from dgus.display.communication.communication_interface import SerialCommunication
from controls.moonraker_data_variable import MoonrakerDataVariable
from data_addresses import DataAddress
from moonraker.websocket_interface import WebsocketInterface

class ExtruderTemperatureToLowMask(Mask):

    
    def __init__(self, com_interface: SerialCommunication, web_socket : WebsocketInterface) -> None:
        super().__init__(52, com_interface)

        min_extrude_temp = MoonrakerDataVariable(
            comInterface=com_interface,
            dataAddress=DataAddress.MIN_EXTRUDE_TEMPERATURE,
            dataLength=1,
            configAddress=DataAddress.UNDEFINED,
            websock=web_socket
        )

        min_extrude_temp.set_klipper_data(["configfile", "settings", "extruder", "min_extrude_temp"])

        self.controls.append(min_extrude_temp)


        