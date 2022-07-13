How to use DGUS Display with Klipper
==================================
The whole Application is able to run as standalone. It doesn't need to be run on the Klipper host machine (e.G. Raspberry PI)

You can just connect the display using an USB-TTL converter to any machine that is capable running python, and has a network connection to reach Moonraker running on your klipper host machine.


Connect display and USB-TTL
---------------------------
For usage with Klipper the Display has to be connected to an USB-TTL converter.

![Display Connector Pinout](img/DisplayConnector_PinOut.png)

| Display Connector | USB-TTL |
|-------------------|---------|
| 5V                | 5V      |
| GND               | GND     |
| TX2               | RXD     |
| RX2               | TXD     |

I just took the display appart and solder a few Dupont wires to connector on the display pcb. This Dupont wires are connected to the USB-TTL converter.


Flash the display
-----------------

You can use the *DWIN_SET* folder which can be found in the *dgus_project* folder, and follow [this guide](https://github.com/seho85/python-dgus/wiki/Flash-Display#microsd)


Install the display control application
---------------------------------------
Do the following steps on the machine on which you want to use run the display. 
For normal usage this will be the machine running Klipper and Moonraker (MainsailOS).

1)  Copy the *dgus-klipper* folder to your machine or directly clone it to the machine <pre>git clone https://github.com/seho85/klipper-dgus.git</pre>
2)  SSH into the machine were you liked to run the display controll application.
3) install python-venv package <pre>sudo apt-get install python3-venv</pre> 
4)  Switch into the copied (cloned) *dgus-klipper* folder
   
    1)  Create a python virtual environment <pre>python3 -m venv venv</pre>
    2)  Source the virtual enviroment <pre>source ./venv/bin/activate</pre>
    3)  Install all needed dependencies <pre>pip3 install -r requirements.txt</pre>
    4)  Tweak  [*serial_config.json*](config_files/serial_config_json.md)
    5)  Tweak [*websocket.json*](config_files/websocket_json.md)


Start the display control application
-------------------------------------

1)  Source source virtual python environment<pre>source ./venv/bin/activate</pre>
2)  Switch to *src* folder <pre>cd src</pre>
3)  Run application <pre>python3 main.py</pre>