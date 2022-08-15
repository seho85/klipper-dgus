*************
Display Masks
*************

.. uml::

    (*) --> Startup
    note right
    When Display is powered on,
    or klipper is in any other state
    then ready. This mask will be 
    automatically shown.

    Features:
    -Restart
    -FW Restart
    end note

    Startup --> MainMenu
    note right
    Central Menu to reach
    all functions
    end note

    MainMenu --> Overview
    note bottom
    This mask will be automatically shown
    when klippy enters ready state.

    Features:
    - Control Bed, Extruder Temperatur
    - Show Printtime and progress
    - Show actual postion of printhead
    - Pause / Resume / Cancel Print
    end note

    MainMenu --> Homing
    note bottom
    Features:
    - Homing
    - Drive Axes
    - Perform Z-Tilt
    - 2 user def. postions
    end note

    MainMenu --> Extruder
    note bottom
    Features:
    - Extrude
      Retract
      Filament
    end note

    MainMenu --> Tuning
    note bottom
    Features:
    -Set Z-Offset
    -Set SpeedFactor
    -Set ExtrusionFactor
    end note


    MainMenu --> Fan-LED
    note bottom
    Features:
    -Control Extruder FAN
    -Switch LED
    end note