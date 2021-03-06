# Daikin BRP069A62


## Welcome to the documentation of the main.py application.

There will be multiple pages to help you get started.
- How to use main.py and its command line arguments.
- Daikin websocket implementation.

Hopefully eventually this will also include:
- flask / nypscreen documentation
once those are built and implemented in the script.

## Stuff in the files directory

Here is all the old code that I made in the past for this.
Keeping it for further reference. Neatly organised numbered randomly.

## Using the program

## How it is made

This project is made with the help of the pages mentioned in the `Credits` section. These
pages helped the project along and finally made it all happen.

## Using the `main.py`
If you followed all the basic steps on the main page you are already on your way!
Now lets see what we can do in terms of other command line options and what to give them:

### Changing schedules times and temperatures
```bash
 python3 ./main.py -f ./files/config.ini -s s -v "5 \$NULL|1|,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,"
```
Changes schedule number 5 to empty, Only schedules 3,4 and 5 are editable
Each day has 6 time slots, starting with Monday
Setting every day to 0900 to 18 degrees would be:
```json
\$NULL|1|0900,180;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,
```
Doing this for every day:
```json
\$NULL|1|0900,180;,;,;,;,;,;0900,180;,;,;,;,;,;0900,180;,;,;,;,;,;0900,180;,;,;,;,;,;0900,180;,;,;,;,;,;0900,180;,;,;,;,;,;,;,;,;,;,;,
```
> You need to escape special characters
> Renaming a schedule on the thermostat will tell you this.

### Changing schedule name
```bash
 python3 ./main.py -f ./files/config.ini -s s -v "5 EMPTY|1|,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,;,"
```
Changes the name of schedule 5 from `$NULL` to `EMPTY`
> Note not all special characters are allowed if you happen to wish one with it..

ToDo: Add list of allowed characters :)

### Changing Active Schedule
```bash
python3 ./main.py -f ./files/config.ini -s i -v 3
```
Sets active schedule to number 3
Value must be 0 to 5
### Changing Temperature
```bash
python3 ./main.py -f ./files/config.ini -s t -v 13
```
Set current wanted temperature to 13 degrees (Cold!)
There is a max and a min value. But the script does not check for them.

### Reading data
```bash
python3 ./main.py -f ./files/config.ini -r
```
Reads the database and uses the stored URLS in there as what to read.
### Showing Data
```bash
python3 ./main.py -f ./files/config.ini -r
```
Reads the database and shows you the data.
### Turning on or off
```bash
python3 ./main.py -f ./files/config.ini -s o -v on
python3 ./main.py -f ./files/config.ini -s o -v off
```
> off in this case is actually `standby` in the lan adapter

### Create a new database:
``` bash
python3 ./main.py -f ./files/config.ini -cdb ./files/daikin.db
```

#### To come:
- A fancy diplay in flask / NPYSCREEN
- Changing / setting a holiday start and end date
- The app does not allow you to change the pincode of child lock,
Perhaps this is possible somehow.

### Open ports of the lan adapter
- port 23: Telnet this has a timeout and is thus only open for a certain amount of time.
The user name and password are unknown at this point.
- port 80: Webpage can be viewed upon booting the adapter again on a timeout. Here you can set various things
such as firmware and a static IP
- port 80: Websocket this port is open all the time and basically how this script does its thing.

Bonus:
- SD Card, There is a SD card reader on the board, but yet unknown what for.

> If any one finds out about the telnet part do let me know :)

### Websocket
With the help again of the links in the `Credits` you can do a simple man in the middle attack with
the daikin controller app from the app store out of google play (There is a have a backup of this incase it goes missing)

As the websocket protocol is send over http the requests and responses are easy to capture using a proxy like `Charles` (30 day trail)

#### What to send and what do you get in return?
This is going to be a long section!

First you need to get the IP adress of your lan adapter you can get this from the app on your phone, trough MDNS or in you router.
Once you get a hold of this you can start sending websockets, trough python (`python3 -m pip install websocket`) or any other application.

First lets see the most basic request you can make:
```JSON
{"m2m:rqp":{"op":2,"to":"/[0]","fr":"/","rqi":"dfred"}}
```

To understand this you can go down a long rabbit hole of online stuff :)
like this:
- [WebSocketProtocol](https://onem2m.org/images/files/deliverables/Release2/TS-0020_WebSocket_Protocol_Binding_V2_0_0.pdf)
> Or see the files folder there is a saved copy

For the Lan adapter we will work with:
- OP (values 1 or 2)
- TO (The request URL)
- FR (Valeus / or /S)
- RQI (A random string to keep track of the response you get)
There are more but that is for later.

Now that we know the protocol and have our first request lets look at the output

```JSON
{"m2m:rsp":{"rsc":2000,"rqi":"dfred","to":"/","fr":"/[0]","pc":{"m2m:cb":{"rn":"mn-cse-LONGSTRINGSPECIFICTOYOU","ri":"0000","pi":"","ty":5,"ct":"20000000T000000Z","lt":"20000000T000000Z","st":4,"csi":"mn-cse-LONGSTRINGSPECIFICTOYOU"}}}}
```
Lets format this:

```JSON
{
	"m2m:rsp": {
		"rsc": 2000,
		"rqi": "dfred",
		"to": "/",
		"fr": "/[0]",
		"pc": {
			"m2m:cb": {
				"rn": "mn-cse-LONGSTRINGSPECIFICTOYOU",
				"ri": "0000",
				"pi": "",
				"ty": 5,
				"ct": "20000000T000000Z",
				"lt": "20000000T000000Z",
				"st": 4,
				"csi": "mn-cse-LONGSTRINGSPECIFICTOYOU"
			}
		}
	}
}
```
Lets see what we got:
- rsc: A return code (2000 okm, 2001 ok/valid, 4000, 5000 and other)
This is a sort of HTTP return code we moslty only care about `200*` return codes
- rn/csi: This string is specific to your lan adapter and you need to to activate a new schedule out of 6 possible schedules. (Only at that request) There is a better request you can make to get the full path you need.

Now this was not a very helpfull request to make to the lan adapter. But lets look at the python code to get this:

```python
from websocket import create_connection
import json, string, random
def randomString(stringLength=5):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

ip = "192.168.x.x"
ws = create_connection("ws://"+ip+"/mca")
ws.send('{"m2m:rqp":{"op":2,"to":"/[0]","fr":"/S","rqi":"'+randomString()+'"}}')

response = json.loads(ws.recv())
print(response)
ws.close()
```
Now the urls get a bit more complex along the way. But this is the most minimal request you can make.

Now in order to get something we actually want we can make this request:
```json
{"m2m:rqp":{"op":2,"to":"/[0]/MNAE/1/UnitProfile/la","fr":"/","rqi":"dfred"}}
```
> You can send the same random string twice if you want.

> You can also send `/[0]/MNAE/1/UnitProfile, /[0]/MNAE/1/, /[0]/MNAE/1, ETC` but those are not very helpfull.

This will get you all the "Info" Mainly what we are interested in is

```python
response = json.loads(ws.recv())
data = response["m2m:rsp"]["pc"]["m2m:cin"]["con"]
print(data)
```
This will give you this raw output:
```JSON
{\"SyncStatus\":\"reboot\",\"Sensor\":[\"IndoorTemperature\",\"OutdoorTemperature\",\"LeavingWaterTemperatureCurrent\"],\"UnitStatus\":[\"ErrorState\",\"InstallerState\",\"WarningState\",\"EmergencyState\",\"TargetTemperatureOverruledState\"],\"Operation\":{\"Power\":[\"on\",\"standby\"],\"OperationMode\":[\"heating\"],\"TargetTemperature\":{\"heating\":{\"maxValue\":30.0000000000000000,\"minValue\":12.0000000000000000,\"stepValue\":1.0000000000000000}},\"RoomTemperatureHeating\":{\"maxValue\":30.0000000000000000,\"minValue\":12.0000000000000000,\"stepValue\":1.0000000000000000,\"settable\":true},\"LeavingWaterTemperatureHeating\":{\"maxValue\":80,\"minValue\":25,\"stepValue\":1,\"settable\":false}},\"Schedule\":{\"Base\":\"action\",\"defaultScheduleAvailable\":\"true\",\"NameAdjustable\":\"false\",\"List\":{\"heating\":[{\"StartTime\":{\"stepValue\":10.0000000000000000,\"unit\":\"minutes\"},\"TargetTemperature\":{\"heating\":{\"maxValue\":30.0000000000000000,\"minValue\":12.0000000000000000,\"stepValue\":1}},\"Actions\":[\"StartTime\",\"TargetTemperature\"],\"maxActionsAllowed\":6},[\"monday\",\"tuesday\",\"wednesday\",\"thursday\",\"friday\",\"saturday\",\"sunday\"],[\"monday\",\"tuesday\",\"wednesday\",\"thursday\",\"friday\",\"saturday\",\"sunday\"],[\"monday\",\"tuesday\",\"wednesday\",\"thursday\",\"friday\",\"saturday\",\"sunday\"],[\"monday\",\"tuesday\",\"wednesday\",\"thursday\",\"friday\",\"saturday\",\"sunday\"],[\"monday\",\"tuesday\",\"wednesday\",\"thursday\",\"friday\",\"saturday\",\"sunday\"],[\"monday\",\"tuesday\",\"wednesday\",\"thursday\",\"friday\",\"saturday\",\"sunday\"],[]]}}}"
```
You can reload this into json in python to get a propper overview like(snippet of data):
```JSON
"SyncStatus":"update",
"Sensor":[
  "IndoorTemperature",
  "OutdoorTemperature",
  "LeavingWaterTemperatureCurrent"
],
```
Telling you all the things you can adjust with min / max / possible values

Worthy of note:
The url `/[0]/MNAE/` is your BASE URL, after which a number comes this number is `[1,2,3,4]` Depending on how many Daikin devices you have at home. As I have only 1 device I have no idea if this ever changes after a reboot.

So you can also send this request:
```JSON
{"m2m:rqp":{"op":2,"to":"/[0]/MNAE/0/UnitProfile/la","fr":"/","rqi":"dfred"}}
```
Giving you the things you can adjust with the controller itself. (which is not much)

So far the following URLS have been discovered (some do double duty as send and request, some not even useful for most DIY applications):

```text
/[0]
/[0]/MNAE/0
/[0]/MNAE/0/DateTime/la
/[0]/MNAE/0/Error/la
/[0]/MNAE/0/UnitProfile/la
/[0]/MNAE/1
/[0]/MNAE/1/ChildLock/LockedState/la
/[0]/MNAE/1/ChildLock/PinCode/la
/[0]/MNAE/1/Consumption/la
/[0]/MNAE/1/Holiday/EndDate/la
/[0]/MNAE/1/Holiday/HolidayState/la
/[0]/MNAE/1/Holiday/StartDate/la
/[0]/MNAE/1/Operation/OperationMode/la
/[0]/MNAE/1/Operation/Power/la
/[0]/MNAE/1/Operation/TargetTemperature/la
/[0]/MNAE/1/Schedule/Next/la
/[0]/MNAE/1/Sensor/IndoorTemperature/la
/[0]/MNAE/1/Sensor/OutdoorTemperature/la
/[0]/MNAE/1/UnitIdentifier/Icon/la
/[0]/MNAE/1/UnitIdentifier/Name/la
/[0]/MNAE/1/UnitProfile/la
/[0]/MNAE/1/UnitStatus/EmergencyState/la
/[0]/MNAE/1/UnitStatus/ErrorState/la
/[0]/MNAE/1/UnitStatus/InstallerState/la
/[0]/MNAE/1/UnitStatus/TargetTemperatureOverruledState/la
/[0]/MNAE/1/UnitStatus/WarningState/la
/[0]/MNCSE-node/deviceInfo
/[0]/MNCSE-node/firmware
```
Again you can increment the number in the URL and repeat the discovery / resend all the URLS above to get all the info for a second device if any.

#### Writing packages
Writing data to the lan adapter is a bit complicated / frustrating as in some cases you send data in plain text in order for the device to understand you (even tough you send JSON so its get back translated) Also if you want to update one schedule you have to send all six of them instead of one with just the ID.

#### New temperature:

```JSON
{"m2m:rqp":{"op":1,"to":"/[0]/MNAE/1/Operation/TargetTemperature","fr":"/S","rqi":"","ty":4,"pc":{"m2m:cin":{"con":14,"cnf":"text/plain:0"}}}}
```
where `14` can be any value from 12 to 30

#### changing schedule:
```JSON
{"m2m:rqp":{"op":1,"to":"/[0]/MNAE/1/Schedule/List/Heating","fr":"/S","rqi":"sxpom","ty":4,"pc":{"m2m:cin":{"con":"{ \"data\" : [\"$NULL|0|0700,210;0900,180;1700,210;2300,180;;;0700,210;0900,180;1700,210;2300,180;;;0700,210;0900,180;1700,210;2300,180;;;0700,210;0900,180;1700,210;2300,180;;;0700,210;0900,180;1700,210;2300,180;;;0800,210;2300,180;;;;;0800,210;2300,180;;;;\",\"$NULL|0|0700,210;0900,180;1200,210;1400,180;1700,210;2300,180;0700,    210;0900,180;1200,210;1400,180;1700,210;2300,180;0700,210;0900,180;1200,210;1400,180;1700,210;2300,180;0700,210;0900,180;1200,210;1400,180;1700,210;2300,180;0700,210;0900,180;1200,210;1400,180;1700,210;2300,180;0800,210;2300,180;;;;;0800,210;2300,180;;;;\",\"$NULL|0|0800,210;2300,180;;;;;0800,210;2300,180;;;;;0800,210;2300,180;;;;;0800,210;2300,180;;;;;0800,210;2300,180;;;;;0800,210;2300,180;;;;;0800,210;2300,180;;;;\",\"$NULL|1|;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;\",\"$NULL|1|;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;\",\"$NULL|1|;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;\"]}","cnf":"text/plain:0"}}}}
```
The fist 3 scheduels are default, you can change the following on the last 3
- Name, change `$NULL` into the name you like. Advised is plain text some special characters are allowed but not all.
- schedule, a csv in a csv as plain text in json format in a json.
see changing schedules for format details.

#### Setting holiday
```JSON
{"m2m:rqp":{"op":1,"to":"/[0]/MNAE/1/Holiday/StartDate","fr":"/S","rqi":"npoqn","ty":4,"pc":{"m2m:cin":{"con":"2020-12-31","cnf":"text/plain:0"}}}}
{"m2m:rqp":{"op":1,"to":"/[0]/MNAE/1/Holiday/EndDate","fr":"/S","rqi":"doesf","ty":4,"pc":{"m2m:cin":{"con":"2020-12-31","cnf":"text/plain:0"}}}}
{"m2m:rqp":{"op":1,"to":"/[0]/MNAE/1/Holiday/HolidayState","fr":"/S","rqi":"rhbh","ty":4,"pc":{"m2m:cin":{"con":1,"cnf":"text/plain:0"}}}}
```

In order:
1: Holliday start date
2: Holliday stop date
3: Tuning on holiday (1) change to (0) to turn off.

#### Change to a different schedule:

```JSON
{"m2m:rqp":{"op":1,"to":"/[0]/MNAE/1/Schedule/Default","fr":"/S","rqi":"'+randomString()+'","ty":4,"pc":{"m2m:cin":{"con":"{\"data\":[{\"path\":\"/'device_id'/MNAE/1/schedule/List/Heating/la\",\"id\":3}]}","cnf":"text/plain:0"}}}}
```
- device_id: is a personal ID with a URL you need to send to the adapter. This is the only way to change it. Its read and found for you and put in the database.
- id: numer 3 to 5 to change the schedule you want.

### MQTT:
There is now MQTT support in this script.

Basic usage: `python3 ./main.py -f ./files/config.ini -m`
This will start the MQTT server/client. To stop press `control + c` As you might send this to the background, there is option to place a empty file on a location of your choosing. This will also stop the MQTT process.

What is being PUBBED/SUBBED:

#### SUBS:
1: DHPW/RecvOperationPower - on / off
2: DHPW/RecvTargetTemperature - Integer 12 to 30
3: DHPW/RecvUpdateSchedule - See "changing schedule"
4: DHPW/RecvChangeSchedule - Integer 0 to 5

#### PUBS:
The pubs are divided into 2 sets, a small one and a big one. the smaller one only sends some temp data and the bigger one also sends the schedules errors and other info. The program starts with the big one, and then only sends the big one every `X` seconds configured in the config.ini.

The smaller set is default to every 5 min:
Smaller set:
```
DHPW/IndoorTemperature
DHPW/LeavingWaterTemperatureCurrent
DHPW/WantedTemperature
DHPW/OutdoorTemperature
DHPW/SystemState
DHPW/OperatingMode
DHPW/OperatingMode
DHPW/CurrentActiveSchedule
DHPW/NextSchedule
DHPW/NextTemperatureGoal
```
Bigger set:
```
DHPW/ChildLockState
DHPW/ChildLockCode
DHPW/HolidayStart
DHPW/HolidayEnd
DHPW/HolidayState
DHPW/UserGivenName
DHPW/SystemHeatingState
DHPW/HpUnitIndoorEprom
DHPW/HpUnitUserEprom
DHPW/HpIndoorSoftware
DHPW/HpOutdoorSoftware
DHPW/HpModelNumber
DHPW/ControllerFirmware
DHPW/ControllerSoftware
DHPW/ControllerSerial
DHPW/Brand
DHPW/Model
DHPW/Type
DHPW/DeviceFunction
DHPW/Errors
DHPW/ErrorState
DHPW/InstallerState
DHPW/WarningState
DHPW/EmergencyState
```

All data is `raw` and  un processed as of now! This means that some things might be `0 to 6` instead of `monday to sunday` for example.

Upon request/demand this might be implemented


Any questions? please shoot a message :)
