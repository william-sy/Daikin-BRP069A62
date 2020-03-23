{
    "autodiscover": "False",  (Whether to autodiscover (not implemented yet))
    "baseurl": "/[0]/MNAE/",  (Default Url for 90% of the time)
    "discurl": "/[0]/MNCSE-node/", (The other 10 %)
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
            "type": "",          (b,e,n, or d (base, nested, discovery or error url))
        },

Names:
R: Read
D: Device
U: Unit
I: Info
S: Status
