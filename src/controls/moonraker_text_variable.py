from sys import byteorder
from dgus.display.controls.text_variable import TextVariable
from dgus.display.communication.communication_interface import SerialCommunication
from moonraker.websocket_interface import WebsocketInterface

class MoonrakerTextVariable(TextVariable):

    web_sock : WebsocketInterface = None
    klipper_data = []

    def __init__(self, comInterface: SerialCommunication, dataAddress: int, configAddress: int, TextLength: int, web_sock : WebsocketInterface) -> None:
        super().__init__(comInterface, dataAddress, configAddress, TextLength)
        self.get_control_data_cb = self.get_text
        
        self.web_sock = web_sock

    def set_klipper_data(self, klipper_data):
        self.klipper_data = klipper_data
        

    def get_text(self) -> bytes:

        json_obj = self.web_sock.get_klipper_data(self.klipper_data)

        text = str(json_obj)
        #text = "12345678901234567890"
        #str_data =bytearray(text.encode(encoding='gbk'))

        #text = "0123456789012345678901234567890"
        #text = "ich bin ein "#doll3er text der supper lang is du sack!"
        #text = "1234"
        
        if len(text) > self.data_length:
            text = text[:self.data_length]
            print(f'Text is been cutted after {self.data_length} chars...')
        text_to_encode = f'{text:<{self.data_length}}'

        #str_data =bytearray(text_to_encode.encode())
        str_data =bytearray(text.encode())

        chars_to_append = self.data_length - len(text)
        
        while chars_to_append > 0:
            str_data.append(0x00)
            chars_to_append -= 1

        return str_data