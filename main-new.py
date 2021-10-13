from websocket import create_connection
import yaml, uuid, ipaddress
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



    def _get_options():
        pass


dohpc("./files/dohpc.yml")
# Lets init by scanning the ammount of connected devices.
