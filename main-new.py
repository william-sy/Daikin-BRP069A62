from websocket import create_connection
import yaml, uuid, ipaddress, json
import dpath.util
#import json, datetime, time, string, random, yaml
#import locale, calendar
#locale.setlocale(locale.LC_ALL, '')

# Define a random string to send to the device
#def randomString(stringLength=5):
#    """Generate a random string of fixed length """
#    letters = string.ascii_lowercase
#    return ''.join(random.choice(letters) for i in range(stringLength))

ip = "192.168.2.130"
ws = create_connection("ws://"+ip+"/mca")


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
        # Get config:
        self._read_config(config_file)
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
        elif self.config['basics']['search_ip'] == False:
            pass
            # If this is what the user wants we need to check
            # if there is a device in p1_p2_devices

    def _get_value(self, req, path, return_code="m2m:rsp/rsc"):
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
        elif self.return_code == 4004:
            pass
        return self.return_code

    def _read_config(self, config_file):
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
        device = self.config['p1_p2_devices']
        for key in device:
            if key != 0:
                if device[key]["found"] == True:
                    unitProfile      = f"MNAE/{key}/UnitProfile/la"
                    unitProfilePath  = "m2m:rsp/pc/m2m:cin/con"
                    self._get_value(unitProfile, unitProfilePath)
                    print(self.response)


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

    def _write_device_to_yaml(self, number, item, given_value):
        fname = self.config_file
        stream = open(fname, 'r')
        data = yaml.load(stream, Loader=yaml.FullLoader)
        data['p1_p2_devices'][number][item] = given_value
        with open(fname, 'w') as yaml_file:
            yaml_file.write( yaml.dump(data, default_flow_style=False))



dohpc("./files/dohpc.yml")
# Lets init by scanning the ammount of connected devices.
