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
        hpTempSend = con.execute("SELECT * FROM rw_url WHERE name LIKE 'W_TargetTemperature'")
        hpOperationSend = con.execute("SELECT * FROM rw_url WHERE name LIKE 'W_Heating_OperationPower'")
        hpScheduleSend = con.execute("SELECT * FROM rw_url WHERE name LIKE 'R_Schedule_List_ID'")
        hpsheduleIDSend = con.execute("SELECT * FROM rw_url WHERE name LIKE 'W_ScheduleDefault'")
        hp_device_id = con.execute("SELECT R_Device_ID from hp_data order by DATE DESC limit 1")

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
        daikinNewSchedule = Convert(value)
        idToChange = int(daikinNewSchedule[0])
        newSchedule = daikinNewSchedule[1]
        # Get all current, schedules from the database
        daikinCurrentSchedules = con.execute("select * from hp_data order by DATE DESC limit 1")
        for row in daikinCurrentSchedules:
            S0 = row[37]
            S1 = row[38]
            S2 = row[39]
            S3 = row[40]
            S4 = row[41]
            S5 = row[42]

        if idToChange <= 2:
            print("This schedule is read only")
        elif idToChange >= 3 and idToChange <=5:
                if idToChange == 3:
                    S3 = newSchedule
                elif idToChange == 4:
                    S4 = newSchedule
                elif idToChange == 5:
                    S5 = newSchedule

                for row in hpScheduleSend:
                # Now send the New schedule of choice to the heatpump
                    ws = create_connection(f"ws://{ip}/mca")
                    ws.send('{"m2m:rqp":{"op":1,"to":"'+daikinUrlBase+''+id+''+row[11]+'","fr":"'+row[3]+'","rqi":"'+randomString()+'","ty":4,"pc":{"'+row[4]+'":{"con":"{ \\"data\\":[\\"'+S0+'\\",\\"'+S1+'\\",\\"'+S2+'\\",\\"'+S3+'\\",\\"'+S4+'\\",\\"'+S5+'\\"]}","cnf":"text/plain:0"}}}}')
                    #js_value = json.loads(ws.recv())
                    #response = js_value["m2m:rsp"]["rsc"]
                    #print(response)
        else:
            print("ID out of range")
        ws.close()
        con.close()
    elif type == "i" or type == "I":
        daikinWantedSchedule = value
        for row in hp_device_id:
            device_id = row[0]
        for row in hpsheduleIDSend:
            if int(daikinWantedSchedule) >= 5:
                print("ID out of range try between 0 to 5")
            # Set new ID to start using
            else:
                ws = create_connection(f"ws://{ip}/mca")
                ws.send('{"m2m:rqp":{"op":'+row[8]+',"to":"'+daikinUrlBase+''+id+''+row[11]+'","fr":"'+row[3]+'","rqi":"'+randomString()+'","ty":4,"pc":{"'+row[4]+'":{"con":"{\\"data\\":[{\\"path\\":\\"'+device_id+'\\",\\"id\\":'+daikinWantedSchedule+'}]}","cnf":"text/plain:0"}}}}')
                #response = js_value["m2m:rsp"]["rsc"]
                #print(response)
                ws.close()
    elif type == "o" or type == "O":
        daikinOperationState = value
        for row in hpOperationSend:
            ws = create_connection(f"ws://{ip}/mca")
            if daikinOperationState == "on":
                ws.send('{"m2m:rqp":{"op":'+row[8]+',"to":"'+daikinUrlBase+''+id+''+row[11]+'","fr":"'+row[3]+'","rqi":"'+randomString()+'","ty":4,"pc":{"m2m:cin":{"con":"on","cnf":"text/plain:0"}}}}')
                ws.close()
            elif daikinOperationState == "off":
                ws.send('{"m2m:rqp":{"op":'+row[8]+',"to":"'+daikinUrlBase+''+id+''+row[11]+'","fr":"'+row[3]+'","rqi":"'+randomString()+'","ty":4,"pc":{"m2m:cin":{"con":"standby","cnf":"text/plain:0"}}}}')
                ws.close()
            else:
                print("Please try 'on' or 'off'.")
                pass
    else:
        con.close()
        sys.exit(1)
