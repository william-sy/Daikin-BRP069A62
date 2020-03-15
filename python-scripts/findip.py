from zeroconf import ServiceBrowser, Zeroconf
from time import sleep
import ipaddress

devices=0

class MyListener:
    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        ip = ipaddress.IPv4Address(info.address)
        #print(f"{ip}:\nService:\n{name}\nservice info:\n{info}")
        global devices
        devices += 1

zeroconf = Zeroconf()
listener = MyListener()
browser = ServiceBrowser(zeroconf, "_daikin._tcp.local.", listener)

while devices == 0:
    sleep(0.1)

# try:
#     while devices == 0 :
#         sleep(0.1)
# finally:
#     zeroconf.close()
