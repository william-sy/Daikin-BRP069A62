from websocket import create_connection
import json, datetime, time, string, random
import locale, calendar
locale.setlocale(locale.LC_ALL, '')

# Define a random string to send to the device
def randomString(stringLength=5):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

ip = "192.168.2.130"
ws = create_connection("ws://"+ip+"/mca")

# Just get the deviceID
#ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]\",\"fr\":\"/S\",\"rqi\":\""+randomString()+"\"}}")
#{"m2m:rqp":{"op":2,"to":"/[0]","fr":"/S","rqi":"txdkl"}
#js_function = json.loads(ws.recv())
#device_id = js_function["m2m:rsp"]["pc"]["m2m:cb"]["csi"]
#print(device_id)
# Device ID:
#{'m2m:rsp': {'rsc': 2000, 'rqi': 'fgwur', 'to': '/S', 'fr': '/[0]', 'pc': {'m2m:cb':{'rn': 'mn-cse-5e639e61465efa001c09edc0', 'ri': '0000', 'pi': '', 'ty': 5, 'ct': '20000000T000000Z', 'lt': '20000000T000000Z', 'st': 4, 'csi': 'mn-cse-5e639e61465efa001c09edc0'}}}}

# Get default schedule id
ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/1/Schedule/Default/la\",\"fr\":\"/S\",\"rqi\":\""+randomString()+"\"}}")
#ws.send("{\"m2m:rqp\":{\"op\":1,\"to\":\"/[0]/MNAE/"+id+"/Operation/TargetTemperature\",\"fr\":\"/S\",\"rqi\":\""+randomString()+"\",\"ty\":4,\"pc\":{\"m2m:cin\":{\"con\":"+tmp+",\"cnf\":\"text/plain:0\"}}}}")
# Response:
#{'m2m:rsp': {'rsc': 2000, 'rqi': 'jwmwi', 'to': '/S', 'fr': '/[0]/MNAE/1/Schedule/Default/la', 'pc': {'m2m:cin': {'rn': '0000000e', 'ri': '003d_0000000e', 'pi': '003d', 'ty': 4, 'ct': '20201225T214938Z', 'lt': '20201225T214938Z', 'st': 14, 'con': '{"data":[{"path":"/mn-cse-5e639e61465efa001c09edc0/MNAE/1/schedule/List/Heating/la","id":3}]}'}}}}
js_function = json.loads(ws.recv())
response = js_function["m2m:rsp"]["pc"]["m2m:cin"]["con"]
test = json.loads(response)
print(test["data"][0]["path"])
print(test["data"][0]["id"])

#ws.send('{"m2m:rqp":{"op":1,"to":"/[0]/MNAE/1/Schedule/Default","fr":"/S","rqi":"'+randomString()+'","ty":4,"pc":{"m2m:cin":{"con":"{\\"data\\":[{\\"path\\":\\"/'+device_id+'/MNAE/1/schedule/List/Heating/la\\",\\"id\\":3}]}","cnf":"text/plain:0"}}}}')
#js_function = json.loads(ws.recv())
#print(js_function)
#print(js_function)
#ws.send('{"m2m:rqp":{"op":1,"to":"/[0]/MNAE/1/Schedule/Default","fr":"/S","rqi":"awdde","ty":4,"pc":{"m2m:cin":{"con":"{\"data\":[{\"path\":\"/mn-cse-5e639e61465efa001c09edc0/MNAE/1/schedule/List/Heating/la\",\"id\":3}]}","cnf":"text/plain:0"}}}}')
#js_function = json.loads(ws.recv())
#print(js_function)

#{"m2m:rqp":{"op":1,"to":"/[0]/MNAE/1/Schedule/Default","fr":"/S","rqi":"yqlxr","ty":4,"pc":{"m2m:cin":{"con":"{\"data\":[{\"path\":\"/mn-cse-5e639e61465efa001c09edc0/MNAE/1/schedule/List/Heating/la\",\"id\":2}]}","cnf":"text/plain:0"}}}}
#{"m2m:rqp":{"op":1,"to":"/[0]/MNAE/1/Schedule/Default","fr":"/S","rqi":"zukbi","ty":4,"pc":{"m2m:cin":{"con":"{\"data\":[{\"path\":\"/mn-cse-5e639e61465efa001c09edc0/MNAE/1/schedule/List/Heating/la\",\"id\":3}]}","cnf":"text/plain:0"}}}}
#{"m2m:rqp":{"op":1,"to":"/[0]/MNAE/1/Schedule/Default","fr":"/S","rqi":"izlzc","ty":4,"pc":{"m2m:cin":{"con":"{\"data\":[{\"path\":\"/mn-cse-5e639e61465efa001c09edc0/MNAE/1/schedule/List/Heating/la\",\"id\":2}]}","cnf":"text/plain:0"}}}}
#{"m2m:rqp":{"op":1,"to":"/[0]/MNAE/1/Schedule/Default","fr":"/S","rqi":"jhxcz","ty":4,"pc":{"m2m:cin":{"con":"{\"data\":[{\"path\":\"/mn-cse-5e639e61465efa001c09edc0/MNAE/1/schedule/List/Heating/la\",\"id\":2}]}","cnf":"text/plain:0"}}}}


# Change Schedule:
#ws.send({"m2m:rqp":{"op":1,"to":"/[0]/MNAE/1/Schedule/List/Heating","fr":"/S","rqi":"sxpom","ty":4,"pc":{"m2m:cin":{"con":"{ \"data\" : [\"$NULL|0|0700,210;0900,180;1700,210;2300,180;;;0700,210;0900,180;1700,210;2300,180;;;0700,210;0900,180;1700,210;2300,180;;;0700,210;0900,180;1700,210;2300,180;;;0700,210;0900,180;1700,210;2300,180;;;0800,210;2300,180;;;;;0800,210;2300,180;;;;\",\"$NULL|0|0700,210;0900,180;1200,210;1400,180;1700,210;2300,180;0700,    210;0900,180;1200,210;1400,180;1700,210;2300,180;0700,210;0900,180;1200,210;1400,180;1700,210;2300,180;0700,210;0900,180;1200,210;1400,180;1700,210;2300,180;0700,210;0900,180;1200,210;1400,180;1700,210;2300,180;0800,210;2300,180;;;;;0800,210;2300,180;;;;\",\"$NULL|0|0800,210;2300,180;;;;;0800,210;2300,180;;;;;0800,210;2300,180;;;;;0800,210;2300,180;;;;;0800,210;2300,180;;;;;0800,210;2300,180;;;;;0800,210;2300,180;;;;\",\"$NULL|1|1700,200;22    50,120;;;;;1700,200;2200,180;;;;;1700,200;2200,180;;;;;1700,200;2200,180;;;;;1700,200;2200,180;;;;;1000,200;1300,180;1700,200;2200,180;;;1000,200;1300,180;1700,200;2200,180;;\",\"$NULL|1|;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;\",\"$NULL|1|;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;\"]}","cnf":"text/plain:0"}}}})

ws.close()
