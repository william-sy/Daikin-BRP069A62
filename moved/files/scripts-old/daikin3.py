from websocket import create_connection
import json, datetime, time, urllib
from urllib import request, parse
import random
import string

def randomString(stringLength=5):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def postUdpate(item, value):
    if value is None:
        print("Not posting None value for "+item)
        return
    req =  request.Request("http://openhab:8080/rest/items/"+item+"/state", data=str(value).encode('utf-8')) # this will make the method "POST"
    req.add_header('Content-Type', 'text/plain')
    req.get_method = lambda: 'PUT'
    resp = request.urlopen(req)
    if resp.status!=202 :
        print("Response was %s %s" % (resp.status, resp.reason))

def requestValue(ws, item):
    ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/"+item+"/la\",\"fr\":\"/OpenHab\",\"rqi\":\""+randomString()+"\"}}")
    result1 =  json.loads(ws.recv())
    #print("Response was: %s" % result1)
    value = result1["m2m:rsp"]["pc"]["m2m:cin"]["con"]
    return value

def requestYesterdaysConsumption(unitNumber):
    consumption=requestValue(ws, str(unitNumber)+"/Consumption")
    cj = json.loads(consumption)
    now = datetime.datetime.now()
    weeklyIndex=(now.weekday()-1)+7
    dailyUsage=cj["Electrical"]["Heating"]["W"][weeklyIndex]
    print("Received electrical weekly usage value '%s' for unit %s" % (dailyUsage, unitNumber))
    if dailyUsage is not None: #This may occur if your local time is more advanced
        return dailyUsage*1000 # than the heating unit.
    return None

def requestLast2HoursConsumption(unitNumber):
    consumption=requestValue(ws, str(unitNumber)+"/Consumption")
    cj = json.loads(consumption)
    now = datetime.datetime.now()
    hourlyIndex=((now.hour-2)//2)+12
    biHourly=cj["Electrical"]["Heating"]["D"][hourlyIndex]
    print("Received electrical daily usage value '%s' for unit %s" % (biHourly, unitNumber))
    if biHourly is not None:
        return biHourly*1000
    return None

ts = time.time()
timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

ws = create_connection("ws://192.168.188.20/mca")

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
  print("Received value '%s' for %s" % (value, x))
  #postUdpate(x, value)

#postUdpate("Heating_BiHourlyEnergyHeat", requestLast2HoursConsumption(1))
#postUdpate("Heating_BiHourlyEnergyWater", requestLast2HoursConsumption(2))
#postUdpate("Heating_DailyEnergyHeat", requestYesterdaysConsumption(1))
#postUdpate("Heating_DailyEnergyWater", requestYesterdaysConsumption(2))
ws.close()
