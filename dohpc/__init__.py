from websocket import create_connection
import yaml, uuid, ipaddress, json, sys, time
import dpath.util

class dohpc():
    """
    This is the Daikin Opensource Heatpump Controller.
    """
    UserAgent = "python-dohpc"

    def __init__(self, config_file):
        """
        In Order to get a grasp on what is available we need to do:
        1: get the ip if not given to us
        2: check the ammount of devices on the lan adapter (trough p1p2)
        3: write it to a yml file for later use.
        """
        self.config = ""
        self.config_file = config_file
        self.commonReturnPath = "m2m:rsp/pc/m2m:cin/con"
        # Get config:
        self._read_config(self.config_file)
        if self.config['basics']['search_ip'] == True:
            self._find_ip(self.config['lan_adapter']['serial_nr'])
            ip_address = self.lan_adapter_ip
        elif self.config['basics']['search_ip'] == False:
            ip_address = self.config['lan_adapter']['ip']
            try:
                ipaddress.ip_address(ip_address)
            except:
                print("No valid ip adres given.")
                sys.exit()

        self.ws = create_connection("ws://"+ip_address+"/mca")

        if self.config['basics']['scan_dev'] == True:
            # Scan lan adapter for devices`
            self._get_devices()
            self._get_options()
            self._scan_devices()
            self._update_data()
        elif self.config['basics']['scan_dev'] == False:
            self._update_data()

    def _send_value(self, req, data, return_code="m2m:rsp/rsc"):
        reqid = uuid.uuid4().hex[0:5]
        request = {
            "m2m:rqp": {
                "op": 1,
                "to": f"/[0]/{req}",
                "fr": dohpc.UserAgent,
                "rqi": reqid,
                "ty": 4,
                "pc": {
                    "m2m:cin": data,
                }
            }
        }
        self.ws.send(json.dumps(request))
        result = json.loads(self.ws.recv())
        assert result["m2m:rsp"]["rqi"] == reqid
        assert result["m2m:rsp"]["to"] == dohpc.UserAgent
        self.return_code = dpath.util.get(result, return_code)
        print(self.return_code)
        return self.return_code

    def _get_value(self, req, path, return_code="m2m:rsp/rsc"):
        """
        Get any value from the Adapter.
        """
        reqid = uuid.uuid4().hex[0:5]
        request = {
            "m2m:rqp": {
                "fr": dohpc.UserAgent,
                "rqi": reqid,
                "op": 2,
                "to": f"/[0]/{req}",
            }
        }
        self.ws.send(json.dumps(request))
        result = json.loads(self.ws.recv())

        assert result["m2m:rsp"]["rqi"] == reqid
        assert result["m2m:rsp"]["to"] == dohpc.UserAgent

        self.return_code = dpath.util.get(result, return_code)
        if self.return_code == 2000:
            self.response = dpath.util.get(result, path)
            return self.response

        if self.config['basics']['debug'] == True:
            if self.return_code == 2001:
                print("Hooray - 2001 - Succes")
            elif self.return_code == 4000:
                print(req)
                print("Sorry - 400 - URL ERR")
            elif self.return_code == 4004:
                print(req)
                print("Sorry - 404 - Not Found")
            elif self.return_code == 4102:
                print("Sorry - 4102 - Value ERR")

            print(self.return_code)

    def _read_config(self, config_file):
        """
        Read the config file.
        """
        with open(r'%s' % config_file) as file:
            self.config = yaml.full_load(file)
        return self.config

    def _find_ip(self, serial):
        """
        This function finds the IP adress of your heatpump controller with mDNS
        """
        from zeroconf import Zeroconf
        import socket
        mdns = '_daikin._tcp.local.'
        zeroconf = Zeroconf()
        foundDaikinIP = ""
        serial = str(serial)
        try:
            info = zeroconf.get_service_info(mdns, serial+ '.' + mdns)
            if info:
                foundDaikinIP = socket.inet_ntoa(info.addresses[0])
        except:
            foundDaikinIP = "0.0.0.0"
        finally:
            zeroconf.close()
            self.lan_adapter_ip = foundDaikinIP
            return self.lan_adapter_ip

    def _get_options(self):
        """
        Get all the device 0 options. From the adapter, these should be the same
        across all models.
        """
        device = self.config['p1_p2_devices']
        for key in device:
            if key == 0:
                # Get all the data from device 0
                deviceInfo      = "MNCSE-node/deviceInfo"
                deviceInfoPath  = "m2m:rsp/pc/m2m:dvi"
                self._get_value(deviceInfo, deviceInfoPath)
                self._write_device_to_yaml(key, "manufacturer", self.response["man"])
                self._write_device_to_yaml(key, "model", self.response["mod"])
                self._write_device_to_yaml(key, "duty", self.response["dty"])
                self._write_device_to_yaml(key, "c_firmware", self.response["fwv"])
                self._write_device_to_yaml(key, "c_software", self.response["swv"])
                self._write_device_to_yaml(key, "h_version", self.response["hwv"])
                self._write_device_to_yaml(key, "c_serialnr", self.response["dlb"])
                dateTime        = f"MNAE/{key}/DateTime/la"
                dateTimePath    = "m2m:rsp/pc/m2m:cin"
                self._get_value(dateTime, dateTimePath)
                self._write_device_to_yaml(key, "DeviceTime", self.response["con"])
                # These seem not to play nice.
                #firmware        = "MNCSE-node/firmware"
                #firmwarePath    = "m2m:rsp/pc/m2m:fwr"
                #self._get_value(firmware, firmwarePath)
                #print(self.response)
                #unitProfile     = f"MNAE/{key}/UnitProfile/la"
                #unitProfilePath = "m2m:rsp/pc/m2m:cin/con"
                #self._get_value(unitProfile, unitProfilePath)
                #print(self.response)
                #self._write_device_to_yaml(key, "sync", self.response["SyncStatus"])
                #self._write_device_to_yaml(key, "UnitStatus", self.response["UnitStatus"])
                # Not very usefull.
                #error           = f"MNAE/{key}/Error/la"
                #errorPath       = "m2m:rsp/pc/m2m:cin"
                #self._get_value(error, errorPath)

    def _scan_devices(self):
        """
        Scanning the device for its options.
        """
        self._read_config(self.config_file)
        device = self.config['p1_p2_devices']
        for key in device:
            if key != 0:
                if device[key]["found"] == True:
                    unitProfile      = f"MNAE/{key}/UnitProfile/la"
                    self._get_value(unitProfile, self.commonReturnPath)
                    # Load the response as JSON
                    returnProfile = json.loads(self.response)
                    #print(self.response)
                    # Unit sensors
                    self._write_device_to_yaml(key, "sensor", returnProfile["Sensor"])
                    self._write_device_to_yaml(key, "unitstatus", returnProfile["UnitStatus"])
                    self._write_device_to_yaml(key, "operation", returnProfile["Operation"])
                    self._write_device_to_yaml(key, "schedule", returnProfile["Schedule"])
                    try:
                        self._write_device_to_yaml(key, "consumption", returnProfile["Consumption"])
                    except:
                        pass

                    unitHolidayStart      = f"MNAE/{key}/Holiday/StartDate/la"
                    self._get_value(unitHolidayStart, self.commonReturnPath)
                    self._write_device_to_yaml(key, "unitholidaystart", self.response)
                    unitHolidayEnd      = f"MNAE/{key}/Holiday/EndDate/la"
                    self._get_value(unitHolidayEnd, self.commonReturnPath)
                    self._write_device_to_yaml(key, "unitholidayend", self.response)
                    unitHolidayState      = f"MNAE/{key}/Holiday/HolidayState/la"
                    self._get_value(unitHolidayState, self.commonReturnPath)
                    self._write_device_to_yaml(key, "unitholidaystate", self.response)

    def _get_devices(self):
        path = "m2m:rsp/pc/m2m:cnt/lbl"
        device = self.config['p1_p2_devices']

        for key in device:
            self._get_value(f"MNAE/{key}", path)
            if self.return_code == 2000:
                alive = True
                item  = "found"
                self._write_device_to_yaml(key, item, alive)
            elif self.return_code == 4004:
                alive = False
                item  = "found"
                self._write_device_to_yaml(key, item, alive)

    def _update_data(self):
        """
        This function is here to get all the data, assuming we already scanned the
        device for its options, so we dont have to do that anymore.
        This saves time / bandwidth (not really a concern)
        """
        self._read_config(self.config_file)
        device = self.config['p1_p2_devices']
        for key in device:
            if key != 0:
                if device[key]["found"] == True:
                    # Get unit name
                    sensorData      = f"MNAE/{key}/UnitIdentifier/Name/la"
                    self._get_value(sensorData, self.commonReturnPath)
                    self._write_device_to_yaml(key, "name", self.response)

                    o_data = {}
                    for item in device[key]['operation']:
                        operationData = f"MNAE/{key}/Operation/{item}/la"
                        self._get_value(operationData, self.commonReturnPath)
                        o_data[item] = self.response
                    self._write_device_to_yaml(key, "OperationData", o_data)

                    sc_data = {}


                    # Get data from the found sensors
                    s_data = {}
                    for item in device[key]['sensor']:
                        sensorData      = f"MNAE/{key}/Sensor/{item}/la"
                        self._get_value(sensorData, self.commonReturnPath)
                        s_data[item] = self.response
                    self._write_device_to_yaml(key, "sensorData", s_data)

                    u_data = {}
                    for item in device[key]['unitstatus']:
                        unitData = f"MNAE/{key}/UnitStatus/{item}/la"
                        self._get_value(unitData, self.commonReturnPath)
                        u_data[item] = self.response
                    self._write_device_to_yaml(key, "unitstatusData", u_data)

                    c_data = {}
                    childlockStateData = f"MNAE/{key}/ChildLock/LockedState/la"
                    self._get_value(childlockStateData, self.commonReturnPath)
                    c_data['ChildLockState'] = self.response
                    childlockPinData = f"MNAE/{key}/ChildLock/PinCode/la"
                    self._get_value(childlockPinData, self.commonReturnPath)
                    c_data['ChildLockPin'] = self.response
                    self._write_device_to_yaml(key, "childLockData", c_data)

                    if device[key]["schedule"]:
                        scheduleData = f"MNAE/{key}/Schedule/Next/la"
                        self._get_value(scheduleData, self.commonReturnPath)
                        scheduleRetunData = json.loads(self.response)
                        self._write_device_to_yaml(key, "ScheduleData", scheduleRetunData["data"])

                    try:
                        device[key]["consumption"]
                        consumptionData = f"MNAE/{key}/Consumption/la"
                        self._get_value(consumptionData, self.commonReturnPath)
                        consumptionRetunData = json.loads(self.response)
                        self._write_device_to_yaml(key, "consumptionData", consumptionRetunData["Electrical"])
                    except:
                        pass

    def _write_device_to_yaml(self, number, item, given_value):
        """
        Write the values we got from the adapter to a YML file we understand.
        """
        fname = self.config_file
        stream = open(fname, 'r')
        data = yaml.load(stream, Loader=yaml.FullLoader)
        data['p1_p2_devices'][number][item] = given_value
        with open(fname, 'w') as yaml_file:
            yaml_file.write( yaml.dump(data, default_flow_style=False))

    def _verify(self, subject, url, decode="None"):
        if decode == "None":
            decode = self.commonReturnPath

        device = self.config['p1_p2_devices']
        ret_val = {}
        for key in device:
            if key != 0:
                if device[key]["found"] == True:
                    ret_val[key] = self._get_value(f"MNAE/{key}/{url}", decode)
        return ret_val

    @property
    def IndoorTemperature(self):
        return self._verify("sensor", "Sensor/IndoorTemperature/la")
    @property
    def LeavingWaterTemperatureCurrent(self):
        return self._verify("sensor", "Sensor/LeavingWaterTemperatureCurrent/la")
    @property
    def OutdoorTemperature(self):
        return self._verify("sensor", "Sensor/OutdoorTemperature/la")
    @property
    def TankTemperature(self):
        return self._verify("sensor", "Sensor/TankTemperature/la")
    @property
    def ErrorState(self):
        return self._verify("unitstatus", "UnitStatus/ErrorState/la")
    @property
    def InstallerState(self):
        return self._verify("unitstatus", "UnitStatus/InstallerState/la")
    @property
    def WarningState(self):
        return self._verify("unitstatus", "UnitStatus/WarningState/la")
    @property
    def EmergencyState(self):
        return self._verify("unitstatus", "UnitStatus/EmergencyState/la")
    @property
    def TargetTemperatureOverruledState(self):
        return self._verify("unitstatus", "UnitStatus/TargetTemperatureOverruledState/la")
    @property
    def targetTemperature(self):
        return self._verify("operation", "Operation/TargetTemperature/la")
    @property
    def LTWTOffset(self):
        return self._verify("operation", "Operation/LeavingWaterTemperatureOffsetHeating/la")
    @property
    def powerState(self):
        return self._verify("operation", "Operation/Power/la")
    @property
    def TankPowerFullState(self):
        return self._verify("operation", "Operation/Powerful/la")
    @property
    def powerConsumption(self):
        return self._verify("consumption", "Consumption/la")
    @property
    def DomesticHotWaterTemperatureHeating(self):
        return self._verify("operation", "Operation/DomesticHotWaterTemperatureHeating/la")
    @property
    def AllSchedules(self):
        return self._verify("schedule", "Schedule/List/Heating/la")
    @property
    def CurrentSchedule(self):
        return self._verify("schedule", "Schedule/Default/la")
    @property
    def NextSchedule(self):
        return self._verify("schedule", "Schedule/Next/la")
    # This will update the values in the yml file
    @property
    def UpdateValeus(self):
        self._update_data()

    # This will get a value from the yml file
    def GetValue(self, key, subject, item):
        device = self.config['p1_p2_devices']
        return device[key][subject][item]

    # Sending values to heatpump
    def TurnOnOff(self, key, subject, state):
        # Get current Value:
        if subject == "Power":
            c_state = daikin_heat_pump.powerState
            if c_state == state:
                print("No change")
            elif c_state != state:
                data = {'con': state, 'cnf': 'text/plain:0'}
                self._send_value(f"MNAE/{key}/Operation/{subject}", data)
            else:
                print("Err")
        elif subject == "Powerful":
            c_state = daikin_heat_pump.powerState
            if c_state == state:
                print("No change")
            elif c_state != state:
                data = {'con': state, 'cnf': 'text/plain:0'}
                self._send_value(f"MNAE/{key}/Operation/{subject}", data)
            else:
                print("Err")

    def ChangeTemp(self, key, subject, temp):
        data = {'con': temp, 'cnf': 'text/plain:0'}
        self._send_value(f"MNAE/{key}/Operation/{subject}", data)


if __name__ == "__main__":
    daikin_heat_pump = dohpc("./files/start.yml")
    # Get any value from the YML file.
    #print("#- YML DATA")
    #daikin_heat_pump.UpdateValeus
    #print(daikin_heat_pump.GetValue( 1, "unitstatusData", "TargetTemperatureOverruledState"))
    # Get the value from the lan adapter itself:
    #print("#- Live DATA")
    #print("#-  sensors")
    #print(f"Indoor:    {daikin_heat_pump.IndoorTemperature}")
    #print(f"Water:     {daikin_heat_pump.LeavingWaterTemperatureCurrent}")
    #print(f"Outdoor:   {daikin_heat_pump.OutdoorTemperature}")
    #print(f"Tank:      {daikin_heat_pump.TankTemperature}")
    #print("#-  unitstatus")
    #print(f"Error:     {daikin_heat_pump.ErrorState}")
    #print(f"installer: {daikin_heat_pump.InstallerState}")
    #print(f"Warning:   {daikin_heat_pump.WarningState}")
    #print(f"Emergency: {daikin_heat_pump.EmergencyState}")
    #print(f"Toverrule: {daikin_heat_pump.TargetTemperatureOverruledState}")
    #print("#-  schedules")
    #print(f"Schedule:  {daikin_heat_pump.AllSchedules}")
    #print(f"Schedule:  {daikin_heat_pump.CurrentSchedule}")
    #print(f"Schedule:  {daikin_heat_pump.NextSchedule}")
    #print("#-  operation")
    #print(f"LTWTO:     {daikin_heat_pump.LTWTOffset}")
    #print(f"TargetT:   {daikin_heat_pump.targetTemperature}")
    #print(f"power:     {daikin_heat_pump.powerState}")
    #print(f"TankPower: {daikin_heat_pump.TankPowerFullState}")
    #print(f"PowerC:    {daikin_heat_pump.powerConsumption}")
    #print(f"TankTemp:  {daikin_heat_pump.DomesticHotWaterTemperatureHeating}")

    #print("#- Send Data")
    # Turn the system on / off
    #daikin_heat_pump.TurnOnOff("1", "Power", "on")
    #daikin_heat_pump.TurnOnOff("1", "Power", "standby")
    # Turn Tank on / off (You might want need to change the key)
    #daikin_heat_pump.TurnOnOff("2", "Powerful", "0")
    #daikin_heat_pump.TurnOnOff("2", "Powerful", "1")
    # Change the desired heat in the house:
    #daikin_heat_pump.ChangeTemp("1", "TargetTemperature", 20)
