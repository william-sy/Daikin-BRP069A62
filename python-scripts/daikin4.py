from websocket import create_connection
import json, datetime, time, string, random
import locale, calendar
locale.setlocale(locale.LC_ALL, '')

# Define a random string to send to the device
def randomString(stringLength=5):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

with open('./python-scripts/list.json', 'r') as f:
        datastore = json.load(f)

valueStore = {}

# fetch items:
def fetchData(mode):
    for item in datastore["hosts"]:
        ip = item["ip"]
        id = item["id"]
        ws = create_connection("ws://"+ip+"/mca")
        if mode == "read":
            for ritems in datastore["rw_url"]:
                if ritems["rw"] == "r":
                    name = ritems["name"]
                    url = ritems["url"]
                    end = ritems["end"]
                    key1 = ritems["key1"]
                    key2 = ritems["key2"]
                    type = ritems["type"]
                    burl = datastore["baseurl"]
                    durl = datastore["discurl"]

                    if ritems["type"] == "b":
                        ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\""+burl+""+id+""+url+""+end+"\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
                    elif ritems["type"] == "d":
                        ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\""+durl+""+url+""+end+"\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")

                    js_value = json.loads(ws.recv())
                    value = js_value["m2m:rsp"]["pc"][""+key1+""][""+key2+""]
                    valueStore[""+name+""] = value
        elif mode == "write":
            print("Nothing Yet")

mode= "read"
fetchData(mode)
print(valueStore)
