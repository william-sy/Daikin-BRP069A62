def findIP(serial):
    """
    This function finds the IP adress of your heatpump controller with mDNS
    """
    from zeroconf import Zeroconf
    import socket
    type = '_daikin._tcp.local.'
    serial = serial
    zeroconf = Zeroconf()
    foundDaikinIP = ""
    try:
        info = zeroconf.get_service_info(type, serial+ '.' + type)
        if info:
            foundDaikinIP = socket.inet_ntoa(info.addresses[0])
    finally:
        zeroconf.close()
        return foundDaikinIP
