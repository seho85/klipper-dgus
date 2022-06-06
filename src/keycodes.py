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


class KeyCodes(IntEnum):
    MoveXPlus = 0x0010
    MoveXMinus = 0x0011
    MoveYPlus = 0x0012
    MoveYMinus = 0x0013
    MoveZPlus = 0x0014
    MoveZMinus = 0x0015
    HomeXY = 0x0016
    HomeZ = 0x0017
    HomeAll = 0x0018
    