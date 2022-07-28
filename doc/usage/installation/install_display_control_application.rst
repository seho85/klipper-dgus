***********************************
Install Display Control Application
***********************************

Automatic Install Script
========================
For easy installation on `MainsailOS <https://docs.mainsail.xyz/setup/mainsail-os>`_ 
a setup script named *install_for_mainsailos.sh* can be found in root of the project 
folder.

The script is consists of two major parts:

* :ref:`installation <easy_install_script_installation>`
* :ref:`configuration <easy_install_script_installation>`

On the configuration you will be asked to perform some actions.

Get the project sources to your machine either by copying them per scp or just run

.. code-block:: shell

    git clone https://github.com/seho85/klipper-dgus.git


change into the directory

.. code-block:: shell

    cd klipper-dgus

And run the install script:

.. code-block:: shell

    $ ./install_for_mainsailos.sh

And after installation tweak :ref:`dgus_display_macros.cfg <dgus_display_macros_cfg>`

.. note::
    You will prompted for entering your sudo password.


.. _easy_install_script_installation:

Installation
------------

.. code-block:: shell
    
    #####################################
    DGUS for Klipper (MainsailOS Install)
    #####################################
    Checking if python3-venv is installed...
    python3-venv is already installed

    Creating Python Virtual Environment
    Created Python Virtual Environment

    Activating Python Virtual Environment

    Installing python dependencies
    Looking in indexes: https://pypi.org/simple, https://www.piwheels.org/simple
    Collecting astroid==2.11.5 (from -r requirements.txt (line 1))
    Using cached https://files.pythonhosted.org/packages/94/58/6f1bbfd88b6ba5271b4a9be99cb15cb2fe369794ba410390f0d672c6ad39/astroid-2.11.5-py3-none-any.whl
    Collecting attrs==21.4.0 (from -r requirements.txt (line 2))
    Using cached https://files.pythonhosted.org/packages/be/be/7abce643bfdf8ca01c48afa2ddf8308c2308b0c3b239a44e57d020afa0ef/attrs-21.4.0-py2.py3-none-any.whl
    Collecting dill==0.3.5.1 (from -r requirements.txt (line 3))
    Using cached https://files.pythonhosted.org/packages/12/ff/3b1a8f5d59600393506c64fa14d13afdfe6fe79ed65a18d64026fe9f8356/dill-0.3.5.1-py2.py3-none-any.whl
    Collecting isort==5.10.1 (from -r requirements.txt (line 4))
    Using cached https://files.pythonhosted.org/packages/b8/5b/f18e227df38b94b4ee30d2502fd531bebac23946a2497e5595067a561274/isort-5.10.1-py3-none-any.whl
    Collecting jsonmerge==1.8.0 (from -r requirements.txt (line 5))
    Using cached https://www.piwheels.org/simple/jsonmerge/jsonmerge-1.8.0-py3-none-any.whl
    Collecting jsonschema==4.5.1 (from -r requirements.txt (line 6))
    Using cached https://files.pythonhosted.org/packages/de/ad/850070f0d9e6a9278cc44013c60c467558791cbc2e462925ba4559dec914/jsonschema-4.5.1-py3-none-any.whl
    Collecting lazy-object-proxy==1.7.1 (from -r requirements.txt (line 7))
    Using cached https://www.piwheels.org/simple/lazy-object-proxy/lazy_object_proxy-1.7.1-cp37-cp37m-linux_armv7l.whl
    Processing ./wheels/libdgus-0.0.9-py3-none-any.whl
    Collecting mccabe==0.7.0 (from -r requirements.txt (line 9))
    Using cached https://files.pythonhosted.org/packages/27/1a/1f68f9ba0c207934b35b86a8ca3aad8395a3d6dd7921c0686e23853ff5a9/mccabe-0.7.0-py2.py3-none-any.whl
    Collecting platformdirs==2.5.2 (from -r requirements.txt (line 10))
    Using cached https://files.pythonhosted.org/packages/ed/22/967181c94c3a4063fe64e15331b4cb366bdd7dfbf46fcb8ad89650026fec/platformdirs-2.5.2-py3-none-any.whl
    Collecting pylint==2.13.9 (from -r requirements.txt (line 11))
    Using cached https://files.pythonhosted.org/packages/03/09/7b710f4aab53e3ccc0d9596557bf020c5ad06312e54ec1b60402ec9d694f/pylint-2.13.9-py3-none-any.whl
    Collecting pyrsistent==0.18.1 (from -r requirements.txt (line 12))
    Using cached https://www.piwheels.org/simple/pyrsistent/pyrsistent-0.18.1-cp37-cp37m-linux_armv7l.whl
    Collecting pyserial==3.5 (from -r requirements.txt (line 13))
    Using cached https://files.pythonhosted.org/packages/07/bc/587a445451b253b285629263eb51c2d8e9bcea4fc97826266d186f96f558/pyserial-3.5-py2.py3-none-any.whl
    Collecting tomli==2.0.1 (from -r requirements.txt (line 14))
    Using cached https://files.pythonhosted.org/packages/97/75/10a9ebee3fd790d20926a90a2547f0bf78f371b2f13aa822c759680ca7b9/tomli-2.0.1-py3-none-any.whl
    Collecting websocket-client==1.3.2 (from -r requirements.txt (line 15))
    Using cached https://files.pythonhosted.org/packages/a1/9e/8ddb04ef21ea3dfe3924b884dc11fa785df662af23e049ec2d62eaba707d/websocket_client-1.3.2-py3-none-any.whl
    Collecting wrapt==1.14.1 (from -r requirements.txt (line 16))
    Using cached https://www.piwheels.org/simple/wrapt/wrapt-1.14.1-cp37-cp37m-linux_armv7l.whl
    Collecting typing-extensions>=3.10; python_version < "3.10" (from astroid==2.11.5->-r requirements.txt (line 1))
    Using cached https://files.pythonhosted.org/packages/ed/d6/2afc375a8d55b8be879d6b4986d4f69f01115e795e36827fd3a40166028b/typing_extensions-4.3.0-py3-none-any.whl
    Requirement already satisfied: setuptools>=20.0 in ./venv/lib/python3.7/site-packages (from astroid==2.11.5->-r requirements.txt (line 1)) (40.8.0)
    Collecting typed-ast<2.0,>=1.4.0; implementation_name == "cpython" and python_version < "3.8" (from astroid==2.11.5->-r requirements.txt (line 1))
    Using cached https://www.piwheels.org/simple/typed-ast/typed_ast-1.5.4-cp37-cp37m-linux_armv7l.whl
    Collecting importlib-metadata; python_version < "3.8" (from jsonschema==4.5.1->-r requirements.txt (line 6))
    Using cached https://files.pythonhosted.org/packages/d2/a2/8c239dc898138f208dd14b441b196e7b3032b94d3137d9d8453e186967fc/importlib_metadata-4.12.0-py3-none-any.whl
    Collecting importlib-resources>=1.4.0; python_version < "3.9" (from jsonschema==4.5.1->-r requirements.txt (line 6))
    Using cached https://files.pythonhosted.org/packages/3c/a7/4e4a2176fed10ab233cc39b083ba4ec222ba52de2be606e3e2b5195264e9/importlib_resources-5.8.0-py3-none-any.whl
    Collecting zipp>=0.5 (from importlib-metadata; python_version < "3.8"->jsonschema==4.5.1->-r requirements.txt (line 6))
    Using cached https://files.pythonhosted.org/packages/f0/36/639d6742bcc3ffdce8b85c31d79fcfae7bb04b95f0e5c4c6f8b206a038cc/zipp-3.8.1-py3-none-any.whl
    Installing collected packages: typing-extensions, wrapt, lazy-object-proxy, typed-ast, astroid, attrs, dill, isort, zipp, importlib-metadata, pyrsistent, importlib-resources, jsonschema, jsonmerge, libdgus, mccabe, platformdirs, tomli, pylint, pyserial, websocket-client
    Successfully installed astroid-2.11.5 attrs-21.4.0 dill-0.3.5.1 importlib-metadata-4.12.0 importlib-resources-5.8.0 isort-5.10.1 jsonmerge-1.8.0 jsonschema-4.5.1 lazy-object-proxy-1.7.1 libdgus-0.0.9 mccabe-0.7.0 platformdirs-2.5.2 pylint-2.13.9 pyrsistent-0.18.1 pyserial-3.5 tomli-2.0.1 typed-ast-1.5.4 typing-extensions-4.3.0 websocket-client-1.3.2 wrapt-1.14.1 zipp-3.8.1

    Copying config to klipper_config

    Creating systemd service (autostart)

    Installing DGUS for Klipper Service
    [sudo] password for pi:

    Reloading systemd services...

    Enabling dgus_klipper.service

    Starting initial configuration

.. _easy_install_script_configuration:

Configuration
-------------

.. code-block:: shell

    DGUS for Klipper - Config generation


    Step 1) Determine serial device for USB-TTL from Display:

    Please disconnect USB-TTL used for DGUS Display...
    Press Enter to continue

    Please connect USB-TTL of DGUS Display
    And press Enter to continue

    Found serial interface for DGUS Display: usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0


    Step 2) Setup Moonraker IP
    Is the Display connected to same machine were (MainsailOS) is running on?
    (y/n):y

    Using IP: 127.0.0.1
    Updated serial configuration...
    Updated websocket configuration...

    Display should be available in arround 15 seconds


.. note::
    During testing it happend that the display application was not automatically
    started after installation.

    If this happens on your installation please reboot the system.


Manual Installation
===================

1) Copy the *dgus-klipper* folder to your machine or directly clone it to the machine 

    .. code-block:: shell
        
        git clone https://github.com/seho85/klipper-dgus.git

2) SSH into the machine were you liked to run the display control application.
3) install python-venv package 
    .. code-block::

        sudo apt-get install python3-venv
4)  Switch into the copied (cloned) *dgus-klipper* folder
   
    1)  Create a python virtual environment 
    
        .. code-block::
            
            python3 -m venv venv

    2)  Source the virtual enviroment
        
        .. code-block::
            
            source ./venv/bin/activate

    3)  Install all needed dependencies
    
        .. code-block::
            
            pip3 install -r requirements.txt

    4) Tweak :ref:`serial_config.json <serial_config_json>`
    5) Tweak :ref:`websocket.json <websocket_json>`
    6) Tweak :ref:`dgus_display_macros.cfg <dgus_display_macros_cfg>`
