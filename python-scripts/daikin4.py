from websocket import create_connection
import json, datetime, time, string, random
import locale, calendar, sys, os
locale.setlocale(locale.LC_ALL, '')

valueStore = {}
mode = "read"

with open(os.path.join(sys.path[0], "list.json"), "r") as f:
        datastore = json.load(f)

# Define a random string to send to the device
def randomString(stringLength=5):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

# Discover Daikin units.
def autoDiscover():
    enabled = datastore["autodiscover"]
    if enabled == "True":
        print("Autodiscover initiated. (TBD)")
        # create a autodiscovered list here (mdns)
    elif enabled == "False":
        print("No autodiscover initiated.")
        autoDiscover.hostinfo = datastore["hosts"]
    else:
        print("Oops!")

# fetch or write items:
def workData(mode, value=""):
    for item in autoDiscover.hostinfo:
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
                    key3 = ritems["key3"]
                    type = ritems["type"]
                    burl = datastore["baseurl"]
                    durl = datastore["discurl"]
                    eurl = datastore["errorurl"]
                    # Specific URL for type of data
                    if ritems["type"] == "b" or ritems["type"] == "n":
                        ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\""+burl+""+id+""+url+""+end+"\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
                    elif ritems["type"] == "d":
                        ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\""+durl+""+url+""+end+"\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
                    elif ritems["type"] == "e":
                        ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\""+eurl+""+url+""+end+"\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
                    # Get the result and parse json
                    js_value = json.loads(ws.recv())
                    response = js_value["m2m:rsp"]["rsc"]
                    # If response was healty (http error codes sort of)
                    if response == 2000:
                        # Reprocess initial result
                        value = js_value["m2m:rsp"]["pc"][""+key1+""][""+key2+""]
                        # If we need to process a nested result
                        if ritems["type"] == "n":
                            # Load value as json
                            nested_value = json.loads(value)
                            if name == "R_Schedule_List_ID":
                                # This one needs a different process, as we get a dict in a nested json.
                                get_nested_value = nested_value["data"]
                                print(get_nested_value)
                                print(get_nested_value[key3])
                                #filterred_schedule = get_nested_value[""+key3+""]
                                # Store this in valueStore
                                #valueStore[""+name+""] = filterred_schedule
                            else:
                                # Get the value we want from key3
                                get_nested_value = nested_value["data"][""+key3+""]
                                # Store this in valueStore
                                valueStore[""+name+""] = get_nested_value
                        else:
                            # Result can go sraight into valueStore
                            valueStore[""+name+""] = value
                    elif response == 4004:
                        print(f"The item {name} has not been found")
                    else:
                        print(f"The item {name} gave error {response}, please investigate")
        elif mode == "write":
            print(f"Nothing Yet {value}")

        ws.close()

# This will auto discover units over MDNS or not depending on JSON
autoDiscover()
# Reads or writes
workData(mode)

print(valueStore)
