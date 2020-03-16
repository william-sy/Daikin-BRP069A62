# Daikin Lan Adapter scripts

## Intro
Hi this repository is my fiddles into hopefully a flask app or something to put into a pi mirror project

Most of the things you see here are inspired by:

- [openenergymonitor.org](https://community.openenergymonitor.org/t/hack-my-heat-pump-and-publish-data-onto-emoncms/2551/25)
- [openhab.org](https://community.openhab.org/t/how-to-integrate-daikin-altherma-lt-heat-pump/16488/27)
- [athom.com](https://community.athom.com/t/daikin-ai/158/103)

Please give them a read it will help!
Most project out there for Daikin is for their aico units and not heatpump stuff such as:
- [git project 1](https://github.com/ael-code/daikin-control)
- [git project 2](https://github.com/apetrycki/daikinskyport)
- [git project 3](https://github.com/ael-code/daikin-aricon-pylib)

I am sure you can find more even on the urls there is this repo that does all of this on the Daikin proprietairty p1/p2 serial bus:
- [p1/ps serial bus](https://github.com/Arnold-n/P1P2Serial)

## In this repo
My attempt to combine all this into a script that fetches all the data, sofar the result is:
```
User chosen schedule ID: 3
Next schedule change: Sunday, Time: 2200, temp will be set to: 18.0
Complete schedule: $NULL|1|1700,200;2200,180;,;,;,;,;1700,200;2200,180;,;,;,;,;1700,200;2200,180;,;,;,;,;1700,200;2200,180;,;,;,;,;1700,200;2200,180;,;,;,;,;1000,200;1300,180;1700,200;2200,180;,;,;1000,200;1300,180;1700,200;2200,180;,;,
=====================================================
Connected to Daikin on: 192.168.1.247
Device function: function/SpaceHeating
The device is currently: on, and the operation is: heating
Brand: Daikin, LAN adapter Model: BRP069A62, Duty: HVAC controller, Firmware: 17003906, Software: 436CC123000, SerialNR: XXXXXXXXXXX
Given name by user: Central heating
=====================================================
Indoor unit model: EHYHBH08AAV3, software: ID9051, EEPROM: AS1706433-11A
Outdoor unit Software: ID3904, User EEPROM: AS1705847-01F, User interface software: AS1705847-01F
=====================================================
Current Errors: 0, Current Warmings: 0, Emergency state: 0,  Installer state: 0
Reported Errors:
=====================================================
Did we manually override the scheduled temp: NO
Current indoor temp: 20.0
Current outdoor temp: 13.0
Current water temp: 43.0
Current target temp: 20.0
=====================================================
Is child lock active: NO, Current pin is: 1234
=====================================================
Holiday start: 2020-03-06, Holiday End: 2020-03-06, Holiday mode active?: NO
=====================================================
ToDo: reset/reboot, Schedule and tempchange (automatic Daikin finder?)
```
Also there are the `index.html` and some javascript files from the daikin heating app, some scripts the community on the posted urls wrote and some notes that helps me to keep track.

## ToDo:
- Schedule read default name
- Schedule change ?
- Change temp.
- Reboot / reset

When all of this is found:
- Make the websocket requests in a nice loop as displayed in `daikin2.py`

Feel free to improve and create pull requests.

## Note:

All setups are different, And its is hard to program every scenario in. Support is welcome.
