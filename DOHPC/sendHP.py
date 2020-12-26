# Converting the argument given to something we can work with
def Convert(string):
    li = list(string.split(" "))
    return li

# Define a random string to send to the device
# I know defined twice, considder it a //To-DO
def randomString(stringLength=5):
    import string, random
    """
    Generate a random string of fixed length
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def sendHPvalues(type, value, daikinIP, dbFileName, daikinUrlError, daikinUrlBase, daikingUrlDisc, daikinDevices):
    import sqlite3 as sl
    from websocket import create_connection
    import json, sys
    """
    Get latest target temperature from the HEATPUMP,
    This works best if you have fresh data.
    """
    con = sl.connect(dbFileName)
    id = "1"
    ip = daikinIP
    with con:
        hpCurrentTemp = con.execute("SELECT R_Heating_TargetTemperature FROM hp_data ORDER BY DATE DESC LIMIT 1;")
        hpTempSend = con.execute("SELECT * FROM rw_url where name like 'W_TargetTemperature'")
        hpOperationSend = con.execute("SELECT * FROM rw_url where name like 'W_Heating_OperationPower'")

    for row in hpCurrentTemp:
        current_target_temp = row[0]
    # Check if the wanted temp is lower or higher else do nothing.
    if type == "t" or type == "T":
        ctt = int(current_target_temp)
        wtt = int(value)
        print(f"temp change to {wtt}")
        if ctt == wtt:
            pass
        else:
            for row in hpTempSend:
                ws = create_connection(f"ws://{ip}/mca")
                ws.send("{\"m2m:rqp\":{\"op\":"+row[8]+",\"to\":\""+daikinUrlBase+""+id+""+row[11]+"\",\"fr\":\""+row[3]+"\",\"rqi\":\""+randomString()+"\",\"ty\":4,\"pc\":{\""+row[4]+"\":{\"con\":"+value+",\"cnf\":\""+row[1]+"\"}}}}")
                js_value = json.loads(ws.recv())
                response = js_value["m2m:rsp"]["rsc"]
                ws.close()
                if response == 2001:
                    print("Sending new temp succes")
                else:
                    if response == 4000:
                        print("Sending new temp failed - URL Error")
                        sys.exit(1)
                    elif response == 4102:
                        print("Sending new temp failed - value Error")
                        sys.exit(1)
            con.close()

    elif type == "s" or type == "S":
        #daikinNewSchedule = Convert(value)
        #print(f"id: {daikinNewSchedule[0]}")
        #print(f"sched: {daikinNewSchedule[1]}")
        # Change:
        ws = create_connection(f"ws://{ip}/mca")
        ws.send('{"m2m:rqp":{"op":1,"to":"/[0]/MNAE/1/Schedule/Active","fr":"/S","rqi":"rtgfd","ty":4,"pc":{"m2m:cin":{"con":1,"cnf":"text/plain:0"}')
        js_value = json.loads(ws.recv())
        response = js_value["m2m:rsp"]["rsc"]
        ws.close()
        print(js_value)
        #{"m2m:rqp":{"op":1,"to":"/[0]/MNAE/1/Schedule/Active","fr":"/S","rqi":"","ty":4,"pc":{"m2m:cin":{"con": "{"data":{"path":"/mn-cse-5e639e61465efa001c09edc0/MNAE/1/schedule/List/Heating","id":2}}","cnf":"application/json:0"}}}}
        #Data:?: "{"data":{"path":"/mn-cse-5e639e61465efa001c09edc0/MNAE/1/schedule/List/Heating/la","id":2}}"
        #{"m2m:rqp":{"op":1,"to":"/[0]/MNAE/1/Schedule/Active","fr":"/S","rqi":"","ty":4,"pc":{"m2m:cin":{"con":20,"cnf":"text/plain:0"}}}}
    elif type == "o" or type == "O":
        daikinOperationState = value
        print(daikinOperationState)
        #{"m2m:rqp":{"op":1,"to":"/[0]/MNAE/1/Operation/Power","fr":"/S","rqi":"olpcx","ty":4,"pc":{"m2m:cin":{"con":"on","cnf":"text/plain:0"}}}}
        #{"m2m:rqp":{"op":1,"to":"/[0]/MNAE/1/Operation/Power","fr":"/S","rqi":"olpcx","ty":4,"pc":{"m2m:cin":{"con":"standby","cnf":"text/plain:0"}}}}
    else:
        con.close()
        sys.exit(1)
