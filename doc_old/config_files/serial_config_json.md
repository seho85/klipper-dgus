serial_config.json
==================
The serial *serial_config.json* file contains the settings for the serial interface which is used to communicate with the DGUS Display.

Currently it contains only a single configuration option.

<pre>
{
   "com_interface": {
      "serial_port": "/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0"
   }
}</pre>

serial_port
-----------
*serial_port* needs to be adapted to match the tty inteface created for your USB-TTL adapter.

If your USB TTL was detected properly it should be listed under */dev/serial/by-id*

<pre>
$ ls /dev/serial/by-id/
usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0
</pre>