# A function to read the congiguration file.
def readConfig(file):
    import configparser
    config = configparser.ConfigParser()
    config.read(file)
    daikinSearch = config['DAIKIN']['search']
    daikinSerial = config['DAIKIN']['serial']
    daikinIP = config['DAIKIN']['ip']
    daikinDevices = config['DAIKIN']['devices']

    return daikinSearch, daikinSerial, daikinIP, daikinDevices
