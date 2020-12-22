# Define a random string to send to the device
def randomString(stringLength=5):
    import string, random
    """
    Generate a random string of fixed length
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

# A function to read the heatpump data
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

    # Setup the connection
    ip = daikinIP
    ws = create_connection("ws://"+ip+"/mca")
    con = sl.connect(dbFileName)
    numberofDaikinDevices = int(daikinDevices)
    if numberofDaikinDevices > 1:
        # Print disclaimer.
        print("""
            Currently more than 1 Daikin device has not been tested / implemented
            Feel free to test on your setup and help the project along if you find bugs!
            Thanks
        """)
    # Get all the specific urls we want.
    with con:
        # Get base and nested URLS
        #hpBase = con.execute("SELECT * FROM rw_url WHERE type LIKE REGEXP '[bn]'; AND rw NOT LIKE '%w%'")
        hpBase = con.execute("SELECT * FROM rw_url WHERE type LIKE 'b' AND rw NOT LIKE 'w%' OR type LIKE 'n%'")
        # Get discovery URLS
        hpDisc = con.execute("SELECT * FROM rw_url where type like '%d%' and rw like '%r%'")
        # Get error URLS
        hpError = con.execute("SELECT * FROM rw_url where type like '%e%' and rw like '%r%'")

    # Time to get the results we want from the heatpump.
    while numberofDaikinDevices >= 1:
        id = str(numberofDaikinDevices)
        for row in hpBase:
            # m2m:rqp = ReQuestParameter, this is default.
            # rqi ReQuestIndex? needs to be random in anycase
            ws.send("{\"m2m:rqp\":{\"op\":"+row[8]+",\"to\":\""+daikinUrlBase+""+id+""+row[11]+""+row[2]+"\",\"fr\":\""+row[3]+"\",\"rqi\":\""+randomString()+"\"}}")
            daikinSocketResponse = ws.recv()
            daikinSocketResponseName = row[7]
            daikinDataFilter(daikinSocketResponse, daikinSocketResponseName, dbFileName)
            #print(ws.recv())
        numberofDaikinDevices -= 1

    for row in hpDisc:
        ws.send("{\"m2m:rqp\":{\"op\":"+row[8]+",\"to\":\""+daikingUrlDisc+""+row[11]+""+row[2]+"\",\"fr\":\""+row[3]+"\",\"rqi\":\""+randomString()+"\"}}")
        daikinSocketResponse = ws.recv()
        daikinSocketResponseName = row[7]
        daikinDataFilter(daikinSocketResponse, daikinSocketResponseName, dbFileName)

    for row in hpError:
        ws.send("{\"m2m:rqp\":{\"op\":"+row[8]+",\"to\":\""+daikinUrlError+""+row[11]+""+row[2]+"\",\"fr\":\""+row[3]+"\",\"rqi\":\""+randomString()+"\"}}")
        daikinSocketResponse = ws.recv()
        daikinSocketResponseName = row[7]
        daikinDataFilter(daikinSocketResponse, daikinSocketResponseName, dbFileName)

    ws.close()

def daikinDataFilter(ReturnData, rowName, dbFileName):
    #import json, datetime, time
    #import locale, calendar
    #locale.setlocale(locale.LC_ALL, '')
    import sqlite3 as sl
    import json
    # Now that we have the data, we need to clean it and make it usable.
    daikinFilteredData = {}
    # Check if we get a healthy response:
    data = json.loads(ReturnData)
    response = data["m2m:rsp"]["rsc"]
    if response == 2000:
        # Healthy return code
        print(f"{rowName}: {ReturnData}")
    elif response == 4004:
        # Unhealthy return code, we dont want this again
        con = sl.connect(dbFileName)
        con.execute(f"UPDATE rw_url SET type = 'Z' WHERE name {rowName}")

    pass
