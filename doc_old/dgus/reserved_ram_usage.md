Reserved RAM
============

| RAM Address | Usage                                                                                                       |
|-------------|-------------------------------------------------------------------------------------------------------------|
| 0x0000      | Used for different Buttons, that trigger a direct message on the Websocket Interface<br>e.g. Emergency Stop |
| 0x0001      | Temperature Target Extruder (ASCII Coded)                                                                   |
| 0x0002      | Temperature Target Bed (ASCII Coded)    |
| 0x0003      | - |
| 0x0004      | Display Mask Change |
| 0x0005      | Axes Move Distance |
| 0x0010      | Extruder Target Temperatture |
| 0x0011      | Bed Target Temperature |
| 0x0012      | Move Buttons |
| 0x0013      | Z-Offset Buttons |
| 0x0014      | Z-Offset Distance |
| 0x0015      | Speed Factor (ASCII) |
| 0x0016      | Extrusion Factor (ASCII) |

Button Codes (0x0000)
---------------------

| Code   | Usage          |
|--------|----------------|
| 0xFFFF | Emergency Stop |
| **Positioning**                |
| 0x0010 | Move X+         |
| 0x0011 | Move X-         |
| 0x0012 | Move Y+        |
| 0x0013 | Move Y-        |
| 0x0014 | Move Z+        |
| 0x0015 | Move Z-        |
| 0x0016 | Home X/Y       |
| 0x0017 | Home Z         |
| 0x0018 | Home ALL       |



Display changed Mask (0x0004)
-----------------------------
Used for notify the Application when the Display Mask was changed.
The KeyCode Matches Display Mask Index to which the Display has changed.


Axes Move Distance (0x0005)
---------------------------
The Value which is delivered from this address is used to driver the position of the toolhead.

Value is tenth (1/10) of a mm


Z-Offset Buttons (0x0013)
-------------------------
| Code   | Usage           |
|--------|-----------------|
| 0x0000 | Z-Offset Raise  |
| 0x0001 | Z-Offset Lower  |

Z-Offset Distance (0x0014)
--------------------------
Value is a thousand (1/1000) of a mm