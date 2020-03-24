from zeroconf import Zeroconf
import ipaddress

TYPE = '_daikin._tcp.local.'
NAME = '175000236'
zeroconf = Zeroconf()
try:
    info = zeroconf.get_service_info(TYPE, NAME+ '.' + TYPE)
    ip = ipaddress.IPv4Address(info.address)
    print(ip)
finally:
    zeroconf.close()
