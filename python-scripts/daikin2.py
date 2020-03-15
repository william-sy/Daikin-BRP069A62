from websocket import create_connection
import json, urllib, random, string
from urllib import request, parse

def randomString(stringLength=5):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def requestValue(ws, item):
    ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/"+item+"/la\",\"fr\":\"/dddd\",\"rqi\":\""+randomString()+"\"}}")
    result1 =  json.loads(ws.recv())
    print("Response was: %s" % result1)

#You need to adjust your IP Address here
ws = create_connection("ws://192.168.1.247/mca")

items =	{
  "Heating_TankTemperature": "2/Sensor/TankTemperature",
  "Heating_IndoorTemperature": "1/Sensor/IndoorTemperature",
  "Heating_OutdoorTemperature": "1/Sensor/OutdoorTemperature",
  "Heating_OperationPower": "1/Operation/Power",
  "Heating_OperationMode": "1/Operation/OperationMode",
  "Heating_OperationTargetTemperature": "1/Operation/TargetTemperature",
  "Heating_TankOperationPower": "2/Operation/Power",
  "Heating_TankOperationMode": "2/Operation/OperationMode",
  "Heating_TankOperationTargetTemperature": "2/Operation/TargetTemperature",
  "Heating_TankOperationPowerful": "2/Operation/Powerful",
  "Heating_ErrorState": "0/UnitStatus/ErrorState"
}

for x in items:
  value = requestValue(ws, items[x])

ws.close()
