from websocket import create_connection
import json, datetime, time, string, random
import locale, calendar, sys, os
import logging
locale.setlocale(locale.LC_ALL, '')

# Open Json for reading
with open(os.path.join(sys.path[0], "list.json"), "r") as f:
        datastore = json.load(f)

valueStore = {}
mode = "read"
LOG_FILENAME = datastore["logfile"]
logging.basicConfig(format='%(levelname)s: %(asctime)s : %(message)s',datefmt='%d/%m/%Y %H:%M:%S',filename=LOG_FILENAME,level=logging.DEBUG)

logging.info("<- Start of program ->")
# Write json function
def writeJson():
    with open(os.path.join(sys.path[0], "list.json"), "w") as f:
            json.dump(datastore, f)
# Define a random string to send to the device
def randomString(stringLength=5):
    # Generate a random string for the urls, This is not mandatory
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
# Discover Daikin units.
def autoDiscover():
    enabled = datastore["autodiscover"]
    if enabled == "True":
        logging.info(" Autodiscover initiated.")
        hosts = datastore["hosts"]
        print(hosts)
        for item in hosts:
            name = item["name"]
            if item["ip"] == "" and item["id"] != "" and item["name"] != "" :
                logging.debug(" We need to look for a IP.")
                from zeroconf import Zeroconf
                import ipaddress
                dns = datastore["dnstype"]
                zeroconf = Zeroconf()
                try:
                    info = zeroconf.get_service_info(dns, item["name"]+ '.' + dns)
                    ip = ipaddress.IPv4Address(info.address)
                finally:
                    zeroconf.close()
                temp = str(ip)
                item["ip"] = ""+temp+""
                writeJson()
                autoDiscover.hostinfo = datastore["hosts"]
            elif item["name"] == "" or item["id"] == "":
                logging.warn(" To find a host we will need the device name and id")
                break
            elif item["ip"] != "" and item["id"] != "":
                logging.warn(" Please set autodiscover to false")
                autoDiscover.hostinfo = datastore["hosts"]
            else:
                logging.error(" You seem to have misconfigured something")
                break
    elif enabled == "False":
        logging.info(" No autodiscover initiated.")
        autoDiscover.hostinfo = datastore["hosts"]
    else:
        logging.error(" Seems like you have encounterred a error at the end of autodiscover.")
        break
# fetch items:
def readData(mode):
    enabled = datastore["autodiscover"]
    if enabled == "True":
        hosts = datastore["hosts"]
        for item in hosts:
            if item["ip"] == "" and item["id"] != "" and item["name"] != "" :
                logging.error(" You need to run autodiscover first")
                break
            elif item["ip"] != "" and item["id"] == ""
                logging.error(" You need to run autodiscover first")
                break
    elif enabled == "False":
        logging.info(" No autodiscover initiated.")
        autoDiscover.hostinfo = datastore["hosts"]

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
                        elif ritems["type"] == "z":
                            print(f"The value {name} has been disabled.")
                            continue
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
                                    if "R_Schedule_Active" in valueStore:
                                        # Check if we already got our manually set ID
                                        # Order in the JSON is important if you dont get this to work.
                                        id = valueStore["R_Schedule_Active"]
                                    else:
                                        # Transform our default json string into a int
                                        id = int(key3)
                                    # Filter the nested json
                                    get_nested_value = nested_value["data"]
                                    # Filter the list that came out of this.
                                    filterred_schedule = get_nested_value[id]
                                    # Store this in valueStore
                                    valueStore[""+name+""] = filterred_schedule
                                else:
                                    # Get the value we want from key3
                                    get_nested_value = nested_value["data"][""+key3+""]
                                    # Store this in valueStore
                                    valueStore[""+name+""] = get_nested_value
                            else:
                                # Result can go sraight into valueStore
                                valueStore[""+name+""] = value
                        elif response == 4004:
                            logging.error("Item has not been found and is now disabled for future.")
                            #print(f"The item {name} has not been found")
                            ritems["type"] = "z"
                            writeJson()
                        else:
                            logging.error(" Encounterred a different error, please investigate")
                            break
                            #print(f"The item {name} gave error {response}, please investigate")

        ws.close()



# throw items:
def writeTempData(mode):
    print("nothing yet")

# throw schedule items:
def writeScheduleData():
    print("nothing yet")


if __name__ == '__main__':
    # This will auto discover units over MDNS or not depending on JSON values
    autoDiscover()
    # Reads all the data from your unit and disables it if your unit does not have a value
    readData(mode)

    # Writes data (Temp change)
    writeTempData(mode)

    # Schedule: Adapt schedule and change active schedule ID (This now also becomes the default ID in your json)
    #writeScheduleData()

# Debug our valueStore
print(valueStore)
logging.info("<- End of program ->")
