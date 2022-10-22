******************
Display Connection
******************

The display is connected to an :ref:`USB-TTL <connection_usb_ttl>` that is capable of putting out 5V.
The :ref:`RaspberryPI Serial Interface <connection_pi_gpio_header>` is also usable.


.. warning::
    It's heavily recommended to connect, the display when the Raspberry Pi is powered off!


Display Connector
=================

.. image:: ../../img/DisplayConnector.jpg

Connection
==========

.. _connection_usb_ttl:

Using USB-TTL
-------------

.. csv-table::
    :header-rows: 1

    Display Connector, USB-TTL
    5V, 5V
    GND, GND
    TX2, RXD
    RX2, TXD

.. note::
    On some of the USB-TTL RXD means RXD should be connected here, and some other
    it means that this pin is RXD. If the display just shows a static mask without
    any values: RXD and TXD needs to be swapped.


.. _connection_pi_gpio_header:

Using Pi Serial interface
-------------------------

#) Activate serial interface on Raspberry Pi

    .. code-block::

        sudo raspi-config

    * *3) Interface Options*
    * *6) Serial Port*

    * Would you like a login shell to be accessible over serial?
 
        * No

    * Would you like the serial port hardware to be enabled?
 
        * Yes

#) **Disconnect Raspberry Pi from Power**

#) Connect Display to Raspberry PI GPIO Pin Header

    .. list-table::
        :header-rows: 1

        * - RaspberryPI PIN 
          - Display
        * - 5V
          - 5V
        * - GND
          - GND
        * - Pin 8
          - RX2
        * - Pin 10
          - TX2

#) Tweak :ref:`serial_config.json <serial_config_json>`

    * set *"serial_port": "/dev/ttyAMA0"*

#) Tweak :ref:`websocket.json <websocket_json>`

    * set *"ip": "10.0.1.69"*

