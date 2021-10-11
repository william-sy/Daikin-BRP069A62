# A function to read the congiguration file.
def readConfig(file):
    import configparser
    config = configparser.ConfigParser()
    config.read(file)
    daikinSearch                    = config['DAIKIN']['search']
    daikinSerial                    = config['DAIKIN']['serial']
    daikinIP                        = config['DAIKIN']['ip']
    daikinBoiler                    = config['DAIKIN']['boiler']
    daikinDataBase                  = config['DAIKIN']['database']
    daikinMqttBroker                = config['MQTT']['broker']
    daikinMqttPublishTempTimeOut    = config['MQTT']['temp_timeout']
    daikinMqttPublishDataTimeOut    = config['MQTT']['data_timeout']
    daikinMqttExitFile              = config['MQTT']['exit']

    # These are default and can actually be removed / made standard.
    daikinUrlError                  = config['URLS']['error']
    daikinUrlBase                   = config['URLS']['base']
    daikinUrlDisc                   = config['URLS']['disc']

    # Return all the values, Done on multiline for your eyes.
    return daikinSearch, daikinSerial, daikinIP,daikinDataBase,                 \
            daikinUrlError, daikinUrlBase, daikinUrlDisc, daikinMqttBroker,     \
            daikinMqttPublishTempTimeOut, daikinMqttPublishDataTimeOut,         \
            daikinMqttExitFile, daikinBoiler
