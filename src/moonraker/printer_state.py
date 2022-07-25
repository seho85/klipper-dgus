from enum import IntEnum


class PrinterState(IntEnum):
    UNKNOWN = -1,
    STANDBYE = 0,
    PRINTING = 1
    PAUSED = 2,
    COMPLETE = 3,
    CANCELLED = 4,
    ERROR = 5


    @staticmethod
    def get_state_for_string(state : str):
        
        if state == "standby":
            return PrinterState.STANDBYE

        if state == "printing":
            return PrinterState.PRINTING
        
        if state == "paused":
            return PrinterState.PAUSED
        
        if state == "complete":
            return PrinterState.COMPLETE

        if state == "cancelled":
            return PrinterState.CANCELLED

        if state == "error":
            return PrinterState.ERROR

        
