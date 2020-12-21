# A fucntion to find the IP with mDNS id wanted
def findIP(name):
    from zeroconf import Zeroconf
    import socket
    type = '_daikin._tcp.local.'
    name = name
    zeroconf = Zeroconf()
    try:
        info = zeroconf.get_service_info(type, name+ '.' + type)
        if info:
            foundDaikinIP = socket.inet_ntoa(info.addresses[0])
            # degug satement.
            #print("Service %s added, IP address: %s" % (name, socket.inet_ntoa(info.addresses[0])))
    finally:
        zeroconf.close()
        return foundDaikinIP
