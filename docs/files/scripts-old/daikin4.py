from websocket import create_connection
import json, datetime, time, string, random
import locale, calendar, sys, os
import logging
locale.setlocale(locale.LC_ALL, '')

# Open Json for reading
with open(os.path.join(sys.path[0], "list.json"), "r") as f:
        datastore = json.load(f)

valueStore = {}
nestedValueStore = {}
jsonValueStore = {}
serviceStore = {}

mode = "read"

# Log settings
LOG_FILENAME = datastore["logfile"]
logging.basicConfig(format='%(levelname)s: %(asctime)s : %(message)s',datefmt='%d/%m/%Y %H:%M:%S',filename=LOG_FILENAME,level=logging.DEBUG)

logging.info("<- Start of program ->")
# Write json function
def writeJson():
    logging.info("JSON WRITTEN")
    with open(os.path.join(sys.path[0], "list.json"), "w") as f:
            json.dump(datastore, f)
# Define a random string to send to the device
def randomString(stringLength=5):
    # Generate a random string for the urls, This is not mandatory
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
# Find Daikin unit IP adress.
def autoDiscover():
    enabled = datastore["autodiscover"]
    if enabled == "True":
        logging.info(" Autodiscover initiated.")
        hosts = datastore["hosts"]
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
                enabled = "False"
                writeJson()
                autoDiscover.hostinfo = datastore["hosts"]
            elif item["name"] == "" or item["id"] == "":
                logging.warn(" To find a host we will need the device name and id")
                break
            elif item["ip"] != "" and item["id"] != "":
                logging.warn(" Please set autodiscover to False")
                autoDiscover.hostinfo = datastore["hosts"]
            else:
                logging.error(" You seem to have misconfigured something")
                break
    elif enabled == "False":
        logging.info(" No autodiscover initiated.")
        autoDiscover.hostinfo = datastore["hosts"]
    else:
        logging.error(" Seems like you have encounterred a error at the end of autodiscover.")
# Fetch Service items
def readServices():
    logging.info("Discovering units capabillities")
    enabled = datastore["autodiscover"]
    if enabled == "True":
        # This is not supposed to happen after the very first run.
        autoDiscover()
    elif enabled == "False":
        autoDiscover.hostinfo = datastore["hosts"]
        for item in autoDiscover.hostinfo:
            ip = item["ip"]
            id = item["id"]
            ws = create_connection("ws://"+ip+"/mca")
            ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/"+id+"/UnitProfile/la\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
            js_value = json.loads(ws.recv())
            response = js_value["m2m:rsp"]["rsc"]
            ws.close()
            if response == 2000:
                value = js_value["m2m:rsp"]["pc"]["m2m:cin"]["con"]
                serviceStore[""+id+""] = value
            else:
                logging.info("Unable to discover units capabilities")
                break
# Set temperature:
def set_tempterature(ids, temp):
    autoDiscover.hostinfo = datastore["hosts"]
    for item in autoDiscover.hostinfo:
        ip = item["ip"]
        id = item["id"]
        tmp = str(temp)
        if ids == id:
            ws = create_connection("ws://"+ip+"/mca")
            ws.send("{\"m2m:rqp\":{\"op\":1,\"to\":\"/[0]/MNAE/"+id+"/Operation/TargetTemperature\",\"fr\":\"/S\",\"rqi\":\""+randomString()+"\",\"ty\":4,\"pc\":{\"m2m:cin\":{\"con\":"+tmp+",\"cnf\":\"text/plain:0\"}}}}")
            js_value = json.loads(ws.recv())
            response = js_value["m2m:rsp"]["rsc"]
            ws.close()
            print(response)
            if response == 2001:
                logging.info("Sending new temp succes")
            else:
                if response == 4000:
                    logging.info("Sending new temp failed - URL Error")
                    break
                elif response == 4102:
                    logging.info("Sending new temp failed - value Error")
                    break
        else:
            print(f"Host with id {id} does not match")
# Fetch data items:
def readData(mode):
    enabled = datastore["autodiscover"]
    if enabled == "True":
        # This is not supposed to happen after the very first run.
        autoDiscover()
    elif enabled == "False":
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
                                #if name == "R_Schedule_Active":
                                #    valueStore[""+name+""] = filterred_schedule

                                if name == "R_Schedule_List_ID":
                                    if "R_Schedule_Active" in valueStore:
                                        # Check if we already got our set ID
                                        # Order in the JSON is important if you dont get this to work.
                                        #id_json = json.loads(valueStore["R_Schedule_Active"])
                                        #id = id_json["data"]["id"]
                                        id = int(valueStore["R_Schedule_Active"])
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
                                    valueStore[""+name+""] = str(get_nested_value)
                            else:
                                # Result can go sraight into valueStore
                                valueStore[""+name+""] = value
                        elif response == 4004:
                            logging.error("Item has not been found and is now disabled for future.")
                            ritems["type"] = "z"
                            writeJson()
                        else:
                            logging.error(" Encounterred a different error, please investigate")
                            break
                            #print(f"The item {name} gave error {response}, please investigate")
                #### end for loop
                # Create a nested dict of all the values at once.
                nestedValueStore[item["id"]] = valueStore

        ws.close()

# throw items:
def write_temp_data(id, temp):
    if jsonValueStore == "":
        logging.info("Trying to change a temperature without any data")
        readData(read)
        write_temp_data(id)
    else:
        logging.info("Temperature change requested")
        ids = str(id)
        RHTT = nestedValueStore[""+ids+""]['R_Heating_TargetTemperature']
        RHIT = nestedValueStore[""+ids+""]['R_Heating_IndoorTemperature']
        if temp == RHTT:
            logging.info("No temp change needed")
        elif temp < RHTT:
            logging.info("Setting temp to a lower setting")
            set_tempterature(ids, temp)
        elif temp > RHTT:
            logging.info("Setting temp to a higher setting")
            set_tempterature(ids, temp)

# throw schedule items:
def write_schedule_data():
    # For naming with multiple words only the following characters will be returned to you: () - + . ?
    # If you use oter charachters, you will get $NULL back but it might show up on the thermostat on the wall with this all characters should be possible
    # If you keep overwriting them, else they will return to stock.
    print("nothing yet")

def activate_schedule():
    print("Activate a certain schedule")

if __name__ == '__main__':
    # This will auto discover units over MDNS or not depending on JSON values
    #autoDiscover()
    # This will read all available services
    #readServices()
    # Reads all the data from your unit and disables it if your unit does not have a value
    readData(mode)
    # Writes data (Temp change)
    #write_temp_data(1, 21)
    # Schedule: Adapt schedule and change active schedule ID (This now also becomes the default ID in your json)
    #write_schedule_data()

print(valueStore)
logging.info("<- End of program ->")
