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
        hpTempSend = con.execute("SELECT * FROM rw_url where name like 'W_TargetTemperature'")
        hpOperationSend = con.execute("SELECT * FROM rw_url where name like 'W_Heating_OperationPower'")

    if type == "t" or type == "T":
        wtt = int(value)
        print(f"temp change to {wtt}")
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
        ws = create_connection(f"ws://{ip}/mca")
        #ws.send({"m2m:rqp":{"op":1,"to":"/[0]/MNAE/1/Schedule/List/Heating","fr":"/S","rqi":"sxpom","ty":4,"pc":{"m2m:cin":{"con":"{ \"data\" : [\"$NULL|0|0700,210;0900,180;1700,210;2300,180;;;0700,210;0900,180;1700,210;2300,180;;;0700,210;0900,180;1700,210;2300,180;;;0700,210;0900,180;1700,210;2300,180;;;0700,210;0900,180;1700,210;2300,180;;;0800,210;2300,180;;;;;0800,210;2300,180;;;;\",\"$NULL|0|0700,210;0900,180;1200,210;1400,180;1700,210;2300,180;0700,    210;0900,180;1200,210;1400,180;1700,210;2300,180;0700,210;0900,180;1200,210;1400,180;1700,210;2300,180;0700,210;0900,180;1200,210;1400,180;1700,210;2300,180;0700,210;0900,180;1200,210;1400,180;1700,210;2300,180;0800,210;2300,180;;;;;0800,210;2300,180;;;;\",\"$NULL|0|0800,210;2300,180;;;;;0800,210;2300,180;;;;;0800,210;2300,180;;;;;0800,210;2300,180;;;;;0800,210;2300,180;;;;;0800,210;2300,180;;;;;0800,210;2300,180;;;;\",\"$NULL|1|1700,200;22    50,120;;;;;1700,200;2200,180;;;;;1700,200;2200,180;;;;;1700,200;2200,180;;;;;1700,200;2200,180;;;;;1000,200;1300,180;1700,200;2200,180;;;1000,200;1300,180;1700,200;2200,180;;\",\"$NULL|1|;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;\",\"$NULL|1|;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;\"]}","cnf":"text/plain:0"}}}})

        js_value = json.loads(ws.recv())
        response = js_value["m2m:rsp"]["rsc"]
        ws.close()
        print(js_value)

    elif type == "i" or type == "I":
        # Set new ID to start using
        #ws.send('{"m2m:rqp":{"op":1,"to":"/[0]/MNAE/1/Schedule/Default","fr":"/S","rqi":"'+randomString()+'","ty":4,"pc":{"m2m:cin":{"con":"{\\"data\\":[{\\"path\\":\\"/'+device_id+'/MNAE/1/schedule/List/Heating/la\\",\\"id\\":3}]}","cnf":"text/plain:0"}}}}')
        pass
    elif type == "o" or type == "O":
        daikinOperationState = value
        print(daikinOperationState)
        #{"m2m:rqp":{"op":1,"to":"/[0]/MNAE/1/Operation/Power","fr":"/S","rqi":"olpcx","ty":4,"pc":{"m2m:cin":{"con":"on","cnf":"text/plain:0"}}}}
        #{"m2m:rqp":{"op":1,"to":"/[0]/MNAE/1/Operation/Power","fr":"/S","rqi":"olpcx","ty":4,"pc":{"m2m:cin":{"con":"standby","cnf":"text/plain:0"}}}}
    else:
        con.close()
        sys.exit(1)
