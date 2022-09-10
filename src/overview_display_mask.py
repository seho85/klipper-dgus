
 # 
 # This file is part of python-dgus (https://github.com/seho85/python-dgus).
 # Copyright (c) 2022 Sebastian Holzgreve
 # 
 # This program is free software: you can redistribute it and/or modify  
 # it under the terms of the GNU General Public License as published by  
 # the Free Software Foundation, version 3.
 #
 # This program is distributed in the hope that it will be useful, but 
 # WITHOUT ANY WARRANTY; without even the implied warranty of 
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
 # General Public License for more details.
 #
 # You should have received a copy of the GNU General Public License 
 # along with this program. If not, see <http://www.gnu.org/licenses/>.
 #
 
import json
from dgus.display.communication.communication_interface import SerialCommunication
from dgus.display.mask import Mask
from dgus.display.onscreen_keyboard import OnScreenKeyBoard
import logging

from controls.moonraker_data_variable import MoonrakerDataVariable
from controls.moonraker_text_variable import MoonrakerTextVariable
from controls.moonraker_printtime_text_variable import MoonrakerPrintTimeTextVariable, PrintTimeDisplay


from moonraker.websocket_interface import WebsocketInterface
from controls.klipper_value_format import KlipperValueType

from data_addresses import DataAddress
from moonraker.request_id import WebsocktRequestId
from keycodes import KeyCodes
from moonraker.moonraker_request import MoonrakerRequest
from moonraker.printer_state import PrinterState

class OverviewDisplayMask(Mask):
    websock : WebsocketInterface = None
    
    temp_extruder = MoonrakerDataVariable
    target_temp_extruder = MoonrakerDataVariable
    temp_bed = MoonrakerDataVariable
    target_temp_bed = MoonrakerDataVariable
    klippy_state = MoonrakerTextVariable
    printer_state = MoonrakerTextVariable
    print_time_total = MoonrakerPrintTimeTextVariable
    print_time_till_finished = MoonrakerPrintTimeTextVariable
    print_completed_percent = MoonrakerDataVariable

    xpos : MoonrakerDataVariable
    ypos : MoonrakerDataVariable

    data = 0

    state_change_pending : bool = False
    printer_state_value : PrinterState = PrinterState.UNKNOWN

    _logger = logging.getLogger(__name__)
    
    def __init__(self, com_interface: SerialCommunication, websock : WebsocketInterface) -> None:
        super().__init__(0, com_interface)

        self.websock = websock
        websock.register_printer_state_event_receiver(self.printer_state_changed)
        
        #0
        self.temp_extruder = MoonrakerDataVariable(self._com_interface, DataAddress.TEMPERATURE_EXTRUDER, 2, DataAddress.UNDEFINED, self.websock)
        self.temp_extruder.set_klipper_data([ "extruder", "temperature"])
        self.controls.append(self.temp_extruder)

        #1
        self.target_temp_extruder = MoonrakerDataVariable(self._com_interface, DataAddress.TARGET_TEMPERATURE_EXTRUDER, 2, DataAddress.UNDEFINED, self.websock)
        self.target_temp_extruder.set_klipper_data([ "extruder", "target"])
        self.controls.append(self.target_temp_extruder)

        #2
        self.temp_bed = MoonrakerDataVariable(self._com_interface, DataAddress.TEMPERATURE_BED, 2, DataAddress.UNDEFINED, self.websock)
        self.temp_bed.set_klipper_data([ "heater_bed", "temperature"])
        self.controls.append(self.temp_bed)

        #3
        self.target_temp_bed = MoonrakerDataVariable(self._com_interface, DataAddress.TARGET_TEMPERATURE_BED,2, DataAddress.UNDEFINED, self.websock)
        self.target_temp_bed.set_klipper_data([ "heater_bed", "target"])
        self.controls.append(self.target_temp_bed)

        #4
        self.klippy_state = MoonrakerTextVariable(self._com_interface, DataAddress.KLIPPY_STATE, DataAddress.UNDEFINED, 24, self.websock)
        self.klippy_state.set_klipper_data(["server_info", "klippy_state"])
        self.controls.append(self.klippy_state)

        #5
        self.printer_state = MoonrakerTextVariable(self._com_interface, DataAddress.PRINTER_STATE, DataAddress.UNDEFINED, 24, self.websock)
        self.printer_state.set_klipper_data(["print_stats", "state"])
        self.controls.append(self.printer_state)

        #6
        self.print_time_total = MoonrakerPrintTimeTextVariable(self._com_interface, DataAddress.PRINT_TIME_TOTAL, DataAddress.UNDEFINED, 8, self.websock, PrintTimeDisplay.TOTAL_TIME)
        self.controls.append(self.print_time_total)

        #7
        self.print_time_till_finished = MoonrakerPrintTimeTextVariable(self._com_interface, DataAddress.PRINT_TIME_TILL_FINISHED, DataAddress.UNDEFINED, 8, self.websock, PrintTimeDisplay.TIME_TILL_FINISH)
        self.controls.append(self.print_time_till_finished)
        
        #8
        self.print_completed_percent = MoonrakerDataVariable(self._com_interface, DataAddress.PRINT_PERCENT, 2, DataAddress.UNDEFINED, self.websock, KlipperValueType.PERCENTAGE)
        self.print_completed_percent.fixed_point_decimal_places = 0
        self.print_completed_percent.set_klipper_data([ "virtual_sdcard", "progress"])
        self.controls.append(self.print_completed_percent)


        self.xpos = MoonrakerDataVariable(self._com_interface, DataAddress.LIVE_X_POS, 2, DataAddress.UNDEFINED, self.websock)
        #self.xpos.set_klipper_data(["toolhead", "position"], 0)
        self.xpos.set_klipper_data(["motion_report", "live_position"], 0)
        self.controls.append(self.xpos)

        self.ypos = MoonrakerDataVariable(self._com_interface, DataAddress.LIVE_Y_POS, 2, DataAddress.UNDEFINED, self.websock)
        #self.ypos.set_klipper_data(["toolhead", "position"], 1)
        self.ypos.set_klipper_data(["motion_report", "live_position"], 1)
        self.controls.append(self.ypos)

        self.zpos = MoonrakerDataVariable(self._com_interface, DataAddress.LIVE_Z_POS, 2, DataAddress.UNDEFINED, self.websock)
        #self.zpos.set_klipper_data(["toolhead", "position"], 2)
        self.zpos.set_klipper_data(["motion_report", "live_position"], 2)
        self.controls.append(self.zpos)


        # Percent complete ["virtual_sd", "progress"]
        # Print time ["print_stats", "print_duration"]

        self._com_interface.register_spontaneous_callback(DataAddress.SPONT_EXTRUDER_TEMP_SETPOINT , self.extruder_target_temp_data_changed)
        self._com_interface.register_spontaneous_callback(DataAddress.SPONT_BED_TEMP_SETPOINT, self.bed_target_temp_data_changed)
        self._com_interface.register_spontaneous_callback(DataAddress.SPONT_OVERVIEW_MASK_BUTTON, self.button_pressed)



    def extruder_target_temp_data_changed(self, response : bytes):
        address = int.from_bytes(response[4:6], byteorder='big', signed=False)
        data = response[7:]
                
        temp_str = OnScreenKeyBoard.decode_numeric_oskbd_value(data)# self.decode_numeric_oskbd_value(data)

        self.send_temperature_cmd("extruder", temp_str)
     

    def bed_target_temp_data_changed(self, response : bytes):
        address = int.from_bytes(response[4:6], byteorder='big', signed=False)
        data = response[7:]
                
        
        temp_str = OnScreenKeyBoard.decode_numeric_oskbd_value(data)
        #temp_str = self.decode_numeric_oskbd_value(data)

        self.send_temperature_cmd("heater_bed", temp_str)

    
    def send_temperature_cmd(self, heater, temperature):
        if temperature != "":
            if heater != "":
                set_extruder_temp = {
                    "jsonrpc": "2.0",
                    "method": "printer.gcode.script",
                    "params": {
                        "script": f"SET_HEATER_TEMPERATURE HEATER={heater} TARGET={temperature}"
                    },
                    "id": WebsocktRequestId.SET_HEATER_TEMPERATURE_CMD
                }
   
                self.websock.ws_app.send(json.dumps(set_extruder_temp))


    def button_pressed(self, response:bytes):
        response_payload = response[7:]
        keycode = int.from_bytes(response_payload, byteorder='big')

        if keycode == KeyCodes.PAUSE_PRINT:
            self._logger.info("Pause Button Pressed...")
            self.send_pause()

        if keycode == KeyCodes.RESUME_PRINT:
            self._logger.info("Resume Button Pressed...")
            self.send_resume()

        if keycode == KeyCodes.CANCEL_PRINT:
            self._logger.info("Cancel Button Pressed...")
            self.send_cancel()

    def send_pause(self):
        self._logger.debug("PrinterState: %s", self.printer_state_value)
        if self.printer_state_value == PrinterState.UNKNOWN:
            return

        if self.state_change_pending:
            self._logger.debug("aborting: Last state change is still pending..")
            return
        
        if self.printer_state_value == PrinterState.PRINTING:

            self.state_change_pending = True

            send_pause_rpc_command = {
                "jsonrpc": "2.0",
                "method": "printer.print.pause",
                "id": WebsocktRequestId.PRINT_PAUSE
            }

            self.websock.ws_app.send(json.dumps(send_pause_rpc_command))



    def send_resume(self):
        self._logger.debug("PrinterState: %s", self.printer_state_value)

        if self.printer_state_value == PrinterState.UNKNOWN:
            return

        if self.state_change_pending:
            self._logger.debug("aborting: Last state change is still pending..")
            return
        
        if self.printer_state_value == PrinterState.PAUSED:

            self.state_change_pending = True

            send_resume_rpc_command = {
                "jsonrpc": "2.0",
                "method": "printer.print.resume",
                "id": WebsocktRequestId.PRINT_RESUME
            }

            self.websock.ws_app.send(json.dumps(send_resume_rpc_command))
  
      

    def send_cancel(self):
        self._logger.debug("PrinterState: %s", self.printer_state_value)

        if self.printer_state_value == PrinterState.UNKNOWN:
            return
        if self.state_change_pending:
            self._logger.debug("aborting: Last state change is still pending..")
            return
        
        if self.printer_state_value == PrinterState.PAUSED or self.printer_state_value == PrinterState.PRINTING:

            self.state_change_pending = True

            send_cancel_rpc_command = {
                "jsonrpc": "2.0",
                "method": "printer.print.cancel",
                "id": WebsocktRequestId.PRINT_CANCEL
            }

            self.websock.ws_app.send(json.dumps(send_cancel_rpc_command))


    def printer_state_changed(self, state : PrinterState, error_msg: str):
        self._logger.debug("PrinterState: %s", self.printer_state_value)
        self.printer_state_value = state
        self.state_change_pending = False
