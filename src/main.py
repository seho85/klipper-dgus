
from signal import signal, SIGINT
from time import sleep
from dgus.display.communication.communication_interface import SerialCommunication
from dgus.display.display import Display

from overview_display_mask import OverviewDisplayMask

from moonraker.websocket_interface import WebsocketInterface

 

if __name__ == "__main__":
    
    PRINTER_IP = "10.0.1.69"
    PORT = 7125
    websock = WebsocketInterface(PRINTER_IP, PORT)


    SERIAL_PORT = "/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0"
    serial_com = SerialCommunication(SERIAL_PORT)

    run_main_thread = True

    def handleSIGINT(signum, frame):
        websock.stop()
        websock.write_json_config()
        serial_com.stop()
        global run_main_thread
        run_main_thread = False

    signal(SIGINT, handleSIGINT)


    if websock.read_json_config():
        websock.start()


    display = Display(serial_com)
        
    overviewMask = OverviewDisplayMask(serial_com, websock)

    display.add_mask(overviewMask)


    if serial_com.start_com_thread():
        display.read_config_data_for_all_controls()

        display.switch_to_mask(0)

        while(run_main_thread):
            display.update_current_mask()
            sleep(0.5)

    
