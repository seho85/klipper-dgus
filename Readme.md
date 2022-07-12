klipper_dgus
============
A python project that connects a DGUS display to [Klipper](https://www.klipper3d.org/)

The display i'm using here is a *DMG80480C043_02WTRZ07* (Stock Display of Anycubic Vyper 3D-Printer) which has a resolution 480x800. For this Display you can find the DGUS Project in the *dgus_project* folder.

For Displays with other resolution, the Project must be recreated.


How to use
----------
1) Flash Display project provided.
1) The display is connected over and USB-TTL to Klipper host machine.
2) Application needs to be started on the Klipper machine.


See [How to use](./doc/HowToUse.md) for details.

Development
-----------
1) create python virtual environment<pre>python -m venv venv</pre>
2) install dependecies<pre>pip install -r requirements.txt</pre>
3) create python-dgus library (See [python-dgus](https://github.com/seho85/python-dgus))
4) Install python-dgus<pre>pip install <path_to_python_dgus>/dist/libdgus-0.0.2-py3-none-any.whl</pre>


License
-------
The whole project is licensed under GPLv3.

See [license](./License)

References
----------
This projects uses Graphics from:

* [Klipper](https://github.com/Klipper3d/klipper)
* [KlipperScreen](https://github.com/jordanruthe/KlipperScreen)
