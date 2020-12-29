from zeroconf import Zeroconf
import socket, time

type = '_daikin._tcp.local.'
name = '175000236'
zeroconf = Zeroconf()
try:
    info = zeroconf.get_service_info(type, name+ '.' + type)
    if info:
        print("Service %s added, IP address: %s" % (name, socket.inet_ntoa(info.addresses[0])))
finally:
    zeroconf.close()
