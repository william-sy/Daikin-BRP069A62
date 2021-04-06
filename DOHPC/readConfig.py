# A function to read the congiguration file.
def readConfig(file):
    import configparser
    config = configparser.ConfigParser()
    config.read(file)
    daikinSearch = config['DAIKIN']['search']
    daikinSerial = config['DAIKIN']['serial']
    daikinIP = config['DAIKIN']['ip']
    daikinDevices = config['DAIKIN']['devices']
    daikinDataBase = config['DAIKIN']['database']
    daikinUrlError = config['URLS']['error']
    daikinUrlBase = config['URLS']['base']
    daikingUrlDisc = config['URLS']['disc']
    daikinMqttBroker = config['MQT']['broker']
    daikinMqttName = config['MQT']['name']
    return daikinSearch, daikinSerial, daikinIP, daikinDevices, daikinDataBase, daikinUrlError, daikinUrlBase, daikingUrlDisc, daikinMqttBroker, daikinMqttName
