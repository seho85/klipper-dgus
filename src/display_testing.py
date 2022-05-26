from dgus.display.communication.communication_interface import SerialCommunication
from dgus.display.communication.request import Request
from dgus.display.communication.protocol import build_write_vp, build_mask_switch_request

def get_request_data_cb() -> bytes:
    return build_write_vp(0x5010, [0x00, 0x08])

def get_switch_mask_cb() -> bytes:
    return build_mask_switch_request(1)

def response_received_cb(response : bytes):
    pass

switch_mask_req = Request(get_switch_mask_cb, response_received_cb, "Switch Mask")

req = Request(get_request_data_cb, response_received_cb, "Testing")

SERIAL_PORT = "/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0"
com_interface = SerialCommunication(SERIAL_PORT)

com_interface.start_com_thread()

com_interface.queue_request(switch_mask_req)
com_interface.queue_request(req)

