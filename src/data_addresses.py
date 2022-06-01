from enum import IntEnum

#TODO: Rename to DGUS RAM 
class DataAddress(IntEnum):
    
    #Spontanous Transmission
    SPONT_MOVE_DISTANCE = 0x0005


    SPONT_EXTRUDER_TEMP_SETPOINT = 0x0010
    SPONT_BED_TEMP_SETPOINT = 0x0011

    SPONT_MOVE_BUTTON = 0x0012

    SPONT_ZOFFET_DISTANCE = 0x0014
    SPONT_ZOFFSET_BUTTON = 0x0013
    SPONT_SPEED_FACTOR_SETPOINT = 0x0015
    SPONT_EXTRUSION_FACTOR_SETPOINT = 0x0016
    

    ########################################

    #OverView Mask
    TEMPERATURE_EXTRUDER = 0x1000
    TARGET_TEMPERATURE_EXTRUDER = 0x1010

    TEMPERATURE_BED = 0x1020
    TARGET_TEMPERATURE_BED = 0x1030

    KLIPPY_STATE = 0x1060
    PRINTER_STATE = 0x1080

    PRINT_TIME_TOTAL = 0x2000
    PRINT_TIME_TILL_FINISHED = 0x2010
    PRINT_PERCENT = 0x2020


    LIVE_X_POS = 0x2030
    LIVE_Y_POS = 0x2032
    LIVE_Z_POS = 0x2034

    #HomingMask
    HOMED_AXES = 0x2040

    #TuningMask
    SPEED_FACTOR = 0x5001
    EXTRUSION_FACTOR = 0x5010
    Z_OFFSET_BITICON = 0x5030

    Z_OFFSET = 0x5020

    UNDEFINED = 0xFFFF


    #AxesDisplayMask

    MOVE_DISTANCE_BITICON = 0x2036