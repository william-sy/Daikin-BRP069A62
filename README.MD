# Daikin BPR069A62 Lan Adapter

## Intro
Welcome to the repository for the DAIKIN BRP-BRP069A62. This project aims to get all
available data from the `BPR069A62 lan adapter` and display it or modify it accordingly to your needs where possible.

The following actions are possible:
- Display all data in a single output
- Edit current desired temperature
- Read out all data from the heatpump and lan adapter
- Change current active schedule (schedules 0 to 5)
- Change all editable schedules (schedules 3 to 5)
- Change name of at least schedules 3 to 5 0 to 3 is not tested.
- Turn the heatpump on or off

# Current to-do of project:
- Create a GUI
- Documentation (Ongoing in the code itself, not formalized in the docs folder just yet)
- Edit holiday (on/off/dates) / change pincode
- Reboot / Reset.

# Simple how-to get started:

# Credits / Other usefull links:
Most of the things you see here are inspired by:
- [openenergymonitor.org](https://community.openenergymonitor.org/t/hack-my-heat-pump-and-publish-data-onto-emoncms/2551/25)
- [openhab.org](https://community.openhab.org/t/how-to-integrate-daikin-altherma-lt-heat-pump/16488/27)
- [athom.com](https://community.athom.com/t/daikin-ai/158/103)
- [home-assistant.io](https://community.home-assistant.io/t/daikin-heat-pump-altherma-integration/202760/13)
- [community.getvera.com](https://community.getvera.com/t/lua-code-to-read-data-via-websocket/213810/17)

Please give them a read it will help!
Most project out there for Daikin is for their aico units and not heatpump stuff such as:
- [git project 1](https://github.com/ael-code/daikin-control)
- [git project 2](https://github.com/apetrycki/daikinskyport)
- [git project 3](https://github.com/ael-code/daikin-aricon-pylib)

I am sure you can find more even on the urls there is this repo that does all of this on the Daikin proprietairty p1/p2 serial bus:
- [p1/ps serial bus](https://github.com/Arnold-n/P1P2Serial)

# Acknowledgments
* [Frankkkkk](https://github.com/Frankkkkk/python-daikin-altherma) As much as my code helped yours, it helped right back :)
