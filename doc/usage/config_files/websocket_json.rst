.. _websocket_json:

**************
websocket.json
**************

The *websocket.json* file contain the settings for the websocket connection that is used to talk to Klipper over the Moonraker Socket.

Usually only the first two parameters *ip* and *port* need to be changed.

Content
=======

Beneath the *ip* and *port* settings there are a few other objects which will be described here.

.. code-block:: json

    {
        "websocket": {
            "ip": "10.0.1.69",
            "port": 7125,
            
            "printer_objects": {
                "some_more_entries" : "..."
            },

            "data_model": {
                "some_more_entries" : "..."
            }
        }
    }


ip
--
IP-Address of the machine were Moonraker is running on. If you use MainsailOS it's the same IP-Adress that you to connect to the Webinterface.


port
----
The port on which moonraker is listening. By default it's running on 7125 and no changes are needed.





printer_objects
---------------

Here are the *printer objects* which will be used by display defined.

See [Moonraker - Printer Objects](https://moonraker.readthedocs.io/en/latest/printer_objects/)

Changes made here may be needed if a new information should be used in the display.

data_model
----------

In *data_model* the latest exchanged data with moonraker is located. This sections doesn't need any manual tweaks at all. Its generated by display controller application. Manual changes will be overwritten on startup/shutdown of the controller application.

