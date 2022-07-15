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

from enum import IntEnum



class WebsocktRequestId(IntEnum):
    QUERY_PRINTER_OBJECTS = 0
    SUBSCRIBE_REQUEST = 1,
    QUERY_SERVER_INFO = 2,
    ADJUST_ZOFFSET = 3,
    WRITE_SPEED_FACTOR = 4,
    EXTRUDE_FILAMENT_CMD = 5,
    PERFORM_MOVE_CMD = 6,
    TURN_MOTORS_OFF_CMD = 7,
    LED_CMD = 8,
    SET_FAN_SPEED_CMD = 9,
    SET_HEATER_TEMPERATURE_CMD=10,
    UNSUBSCRIBE_PRINTER_OBJECTS=11,
    QUERY_PRINTER_INFO = 12,
    FIRMWARE_RESTART = 13,
    RESTART = 14
