# Define a random string to send to the device
def randomString(stringLength=5):
    import string, random
    """
    Generate a random string of fixed length
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

# A function to read the heatpump data, not in use just yet.
def readHPOptions(daikinIP, daikinDevices):
    from websocket import create_connection
    import json, datetime, time
    import locale, calendar
    locale.setlocale(locale.LC_ALL, '')

    # Setup the connection
    ip = daikinIP
    ws = create_connection("ws://"+ip+"/mca")
    numerOfDevices = int(daikinDevices)
    daikinDeviceOptions = {}

    # Scan our options and put then in variables
    while numerOfDevices >= 0:
        daikinDeviceID = str(numerOfDevices)
        ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/"+daikinDeviceID+"/UnitProfile/la\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
        raw_data = json.loads(ws.recv())
        filter_data = raw_data["m2m:rsp"]["pc"]["m2m:cin"]["con"]
        # DDID = Daikin Device ID
        daikinDeviceOptions["DDID{0}".format(daikinDeviceID)] = filter_data
        numerOfDevices -= 1

    ws.close()
    # Returns a dict with JSON as value
    return daikinDeviceOptions

# A function to read the heatpump data
def readHPDetails(daikinIP, dbFileName, daikinUrlError, daikinUrlBase, daikingUrlDisc, daikinDevices):
    from websocket import create_connection
    import sqlite3 as sl
    import datetime, json

    # Setup the connection
    ip = daikinIP
    ws = create_connection(f"ws://{ip}/mca")
    numberofDaikinDevices = int(daikinDevices)
    daikinFilteredData = {}

    if numberofDaikinDevices > 1:
        # Print disclaimer.
        print("""
            Currently more than 1 Daikin device has not been tested / implemented
            Feel free to test on your setup and help the project along if you find bugs!
            Thanks
        """)
    # Create a row to put all the date in:
    now = datetime.datetime.now()
    # Allows you one row per minute.
    today = now.strftime("%Y%m%d%H%M")
    # Get all the specific urls we want.
    con = sl.connect(dbFileName)
    with con:
        con.execute(f"INSERT OR REPLACE INTO hp_data (DATE) VALUES  ('{today}'); ")
        # Get base and nested URLS
        hpBase = con.execute("SELECT * FROM rw_url WHERE type LIKE 'b' AND rw NOT LIKE 'w%' OR type LIKE 'n%'")
        # Get discovery URLS
        hpDisc = con.execute("SELECT * FROM rw_url where type like '%d%' and rw like '%r%'")
        # Get error URLS
        hpError = con.execute("SELECT * FROM rw_url where type like '%e%' and rw like '%r%'")
        # Get Device ID and default schedule ID:
        hpSDID = con.execute("SELECT * FROM rw_url where type like '%s%' and rw like '%w%'")
    # Time to get the results we want from the heatpump.
    while numberofDaikinDevices >= 1:
        id = str(numberofDaikinDevices)
        for row in hpBase:
            # m2m:rqp = ReQuestParameter, this is default.
            # rqi ReQuestIndex? needs to be random in anycase
            ws.send("{\"m2m:rqp\":{\"op\":"+row[8]+",\"to\":\""+daikinUrlBase+""+id+""+row[11]+""+row[2]+"\",\"fr\":\""+row[3]+"\",\"rqi\":\""+randomString()+"\"}}")
            daikinSocketResponse = ws.recv()
            daikinSocketResponseName = row[7]
            daikinDataFilter(daikinSocketResponse, daikinSocketResponseName, dbFileName, row[4], row[5], row[6], row[10], today, con)

        numberofDaikinDevices -= 1

    for row in hpDisc:
        ws.send("{\"m2m:rqp\":{\"op\":"+row[8]+",\"to\":\""+daikingUrlDisc+""+row[11]+""+row[2]+"\",\"fr\":\""+row[3]+"\",\"rqi\":\""+randomString()+"\"}}")
        daikinSocketResponse = ws.recv()
        daikinSocketResponseName = row[7]
        daikinDataFilter(daikinSocketResponse, daikinSocketResponseName, dbFileName, row[4], row[5], row[6], row[10], today, con)

    for row in hpError:
        ws.send("{\"m2m:rqp\":{\"op\":"+row[8]+",\"to\":\""+daikinUrlError+""+row[11]+""+row[2]+"\",\"fr\":\""+row[3]+"\",\"rqi\":\""+randomString()+"\"}}")
        daikinSocketResponse = ws.recv()
        daikinSocketResponseName = row[7]
        daikinDataFilter(daikinSocketResponse, daikinSocketResponseName, dbFileName, row[4], row[5], row[6], row[10], today, con)

    for row in hpSDID:
        ws.send("{\"m2m:rqp\":{\"op\":"+row[8]+",\"to\":\""+daikinUrlBase+""+id+""+row[11]+""+row[2]+"\",\"fr\":\"+row[3]+\",\"rqi\":\""+randomString()+"\"}}")
        daikinSocketResponse = ws.recv()
        daikinSocketResponseName = row[7]
        daikinDataFilter(daikinSocketResponse, daikinSocketResponseName, dbFileName, row[4], row[5], row[6], row[10], today, con)

    con.commit()
    ws.close()
    con.close()

def daikinDataFilter(returnData, rowName, dbFileName, daikinKey1, daikinKey2, daikinKey3, daikinRwType, today, con):
    import sqlite3 as sl
    import json
    # Now that we have the data, we need to clean it and make it usable.
    # Check if we get a healthy response:
    data = json.loads(returnData)
    response = data["m2m:rsp"]["rsc"]
    if response == 2000:
        # Healthy return code
        #print(f"{rowName}: {returnData}")
        if daikinRwType == "n":
            # This will get messy, but bear with it pesky values hidden away:
            if rowName == "R_Schedule_List_ID":
                extractData = data["m2m:rsp"]["pc"][daikinKey1][daikinKey2]
                nestedData = json.loads(extractData)
                extractNestedData = nestedData["data"]
                #return extractNestedData
                con.execute(f"""
                    UPDATE hp_data SET
                        R_Schedule_List_ID_0 = '{extractNestedData[0]}',
                        R_Schedule_List_ID_1 = '{extractNestedData[1]}',
                        R_Schedule_List_ID_2 = '{extractNestedData[2]}',
                        R_Schedule_List_ID_3 = '{extractNestedData[3]}',
                        R_Schedule_List_ID_4 = '{extractNestedData[4]}',
                        R_Schedule_List_ID_5 = '{extractNestedData[5]}'
                    WHERE DATE LIKE '{today}';
                """)
            else:
                try:
                    extractData = data["m2m:rsp"]["pc"][daikinKey1][daikinKey2]
                    nestedData = json.loads(extractData)
                    extractNestedData = nestedData["data"][daikinKey3]
                    #return extractNestedData
                    con.execute(f"""
                        UPDATE hp_data SET
                            {rowName} = '{extractNestedData}'
                        WHERE DATE LIKE '{today}';
                    """)
                except:
                    pass
                    # power must be off
        elif daikinRwType == "s":
            # Normally we dont want this but we have to make 1 execption:
            if rowName == "R_ScheduleDefault":
                extractData = data["m2m:rsp"]["pc"][daikinKey1][daikinKey2]
                nestedData = json.loads(extractData)
                deviceID = nestedData["data"][0]["path"]
                defaultSchedule = nestedData["data"][0]["id"]
                con.execute(f"""
                    UPDATE hp_data SET
                        R_Device_ID = '{deviceID}',
                        R_Schedule_List_ID = '{defaultSchedule}'
                    WHERE DATE LIKE '{today}';
                """)
            else:
                pass
        else:
            # These should be less nested:
            if rowName == "R_D_Error":
                extractData = data["m2m:rsp"]["pc"][daikinKey1][daikinKey2]
                if extractData == "":
                    extractData = "None"
                    #return extractData
                con.execute(f"""
                    UPDATE hp_data SET
                        {rowName} = '{extractData}'
                    WHERE DATE LIKE '{today}';
                """)
            else:
                extractData = data["m2m:rsp"]["pc"][daikinKey1][daikinKey2]
                #return extractData
                con.execute(f"""
                    UPDATE hp_data SET
                        {rowName} = '{extractData}'
                    WHERE DATE LIKE '{today}';
                """)
        pass
    elif response == 4004:
        # Unhealthy return code, we dont want this again
        con = sl.connect(dbFileName)
        con.execute(f"UPDATE rw_url SET type = 'Z' WHERE name {rowName}")
        con.commit()
        con.close()
    pass
