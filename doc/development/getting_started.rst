.. _dev-getting-started:

***************
Getting started
***************

Project overview
================
The *klipper-dgus* project consists of two main parts:

* :ref:`Display control application <display-control-application>` (python code)
    * controls the display over the serial interface
        * using the `python-dgus <https://github.com/seho85/python-dgus>`_ library
    * reads data from klipper using the Moonraker Websocket.
* :ref:`Display application <display-application>` (created in DGUS Tool)
    * defines which controls are on each DisplayMask
    * how the controls look like (text color, number format, a.s.o)

Tools
=====

Display Control Application
---------------------------

The python sources are developed in Visual Studio Code.


DGUS Display Application
------------------------

The Display Application is with the DGUS Tool v8.2.1.14