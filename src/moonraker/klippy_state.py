from enum import Enum


class KlippyState(Enum):
    UNKOWN = 0,
    READY = 1,
    ERROR = 2,
    SHUTDOWN = 3,
    STARTUP = 4,
    DISCONNECTED = 5

    @staticmethod
    def get_state_for_string(state_string):
        if state_string == "ready":
            return KlippyState.READY
        
        if state_string == "error":
            return KlippyState.ERROR

        if state_string == "shutdown":
            return KlippyState.SHUTDOWN

        if state_string == "startup":
            return KlippyState.STARTUP

        raise ValueError("Invalid klippy_state string!", state_string)