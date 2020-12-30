{
    "autodiscover": "False",  (Whether to autodiscover (not implemented yet)) -> If true then define the serial number of the device ask your installed!
    "baseurl": "/[0]/MNAE/",  (Default Url for 90% of the time)
    "discurl": "/[0]/MNCSE-node/", (The other 10 %)
    "dnstype": "_daikin._tcp.local.", (The mdns string_)
    "errorurl": "/[0]/MNAE/0", (THe url where the unit collects errors)
    "logfile": "./daikin.log", (Where you want your logs)
    "hosts": [
        {
            "ip": "192.168.1.247",  (Hosts here if autodiscover == false)
            "id": "1"
        }
    ],
    "rw_url": [
        {
            "name": "R_Info",  (general name)
            "key1": "m2m:cnt", (read key 1)
            "key2": "lbl",     (read key 2)
            "op": "2",         (Read or write setting)
            "url": "",         (The url to get data from)
            "fr": "/",         (set to /S for sending / for receiving)
            "end": "",         (/la or empty depending on sending / reading etc.)
            "cnf": "",         (The data to send here)
            "rw" : "r",        ( If this config is for reading or writing)
            "type": "",        (b,e,n, or d (base, nested, discovery or error url)) (Z is disabled.)
        },

Names:
R: Read
D: Device
U: Unit
I: Info
S: Status
