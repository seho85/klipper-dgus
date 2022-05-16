from dgus.display.communication.communication_interface import SerialCommunication
from controls.moonraker_data_variable import MoonrakerDataVariable
from dgus.display.mask import Mask

from moonraker.websocket_interface import WebsocketInterface

class OverviewDisplayMask(Mask):
    websock : WebsocketInterface = None
    
    temp_extruder = MoonrakerDataVariable
    target_temp_extruder = MoonrakerDataVariable
    temp_bed = MoonrakerDataVariable
    target_temp_bed = MoonrakerDataVariable

    data = 0
    
    def __init__(self, com_interface: SerialCommunication, websock : WebsocketInterface) -> None:
        super().__init__(0, com_interface)

        self.websock = websock
        
        self.temp_extruder = MoonrakerDataVariable(self.com_interface, 0x1000, 2, 0x2000, self.websock)
        self.temp_extruder.set_klipper_data([ "extruder", "temperature"])
        self.controls.append(self.temp_extruder)

        self.target_temp_extruder = MoonrakerDataVariable(self.com_interface, 0x1020,2, 0x2020, self.websock)
        self.target_temp_extruder.set_klipper_data([ "extruder", "target"])
        self.controls.append(self.target_temp_extruder)

        self.temp_bed = MoonrakerDataVariable(self.com_interface, 0x1010, 2, 0x2010, self.websock)
        self.temp_bed.set_klipper_data([ "heater_bed", "temperature"])
        self.controls.append(self.temp_bed)

        self.target_temp_bed = MoonrakerDataVariable(self.com_interface, 0x1030,2, 0x2030, self.websock)
        self.target_temp_bed.set_klipper_data([ "heater_bed", "target"])
        self.controls.append(self.target_temp_bed)
