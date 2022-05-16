from ast import Bytes
from typing import List
from dgus.display.controls.data_variable import DataVariable
from dgus.display.communication.communication_interface import SerialCommunication

from moonraker.websocket_interface import WebsocketInterface

class MoonrakerDataVariable(DataVariable):

    websock : WebsocketInterface = None
    klipper_data : List = []
    data = None

    static_data = 1

    def __init__(self, comInterface: SerialCommunication, dataAddress: int, dataLength: int, configAddress: int, websock : WebsocketInterface) -> None:
        super().__init__(comInterface, dataAddress, dataLength, configAddress)
        self.websock = websock


    def set_klipper_data(self, klipper_data):
        
        self.klipper_data = klipper_data
        #self.data = json_obj
        
        #self.klipper_data = klipper_data
        #self.read_config_data_callback = self.static_value_value_cb
        #super().read_data_callback = self.read_moonraker_data_callback

        self.read_data_callback = self.read_moonraker_data_callback

    def value_to_fixed_point(self, data, decimal_places):
        temp_float = float(data) * pow(10, decimal_places)
        return int(temp_float)


    def read_moonraker_data_callback(self):
        json_obj = self.websock.json_data_modell
        for dp in self.klipper_data:
            json_obj = json_obj.get(dp)
            if json_obj is None:
                print("Error Invalid Klipper Data")

        val = self.value_to_fixed_point(json_obj, 1)
        return val.to_bytes(length=2, byteorder='big')

    def static_value_value_cb(self):
        self.static_data += 1

        return self.static_data.to_bytes(length=2, byteorder='big')
