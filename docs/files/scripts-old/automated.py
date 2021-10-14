import json
import uuid

from websocket import create_connection

class dohpc:
    UserAgent = "dohpc"

    def __init__(self, ip: str):
        self.ip = ip
        self.ws = create_connection(f"ws://{self.ip}/mca")
        # Check for devices

    def _requestValue(self, item: str, output_path: str, payload=None):
        reqid = uuid.uuid4().hex[0:5]
        js_request = {
            "m2m:rqp": {
                "fr": DaikinAltherma.UserAgent,
                "rqi": reqid,
                "op": 2,
                "to": f"/[0]/{item}",
            }
        }
        if payload:
            set_value_params = {
                'ty': 4,
                'op': 1,
                'pc': {                    'm2m:cin': payload,
                }
            }
            js_request['m2m:rqp'].update(set_value_params)


        self.ws.send(json.dumps(js_request))
        result = json.loads(self.ws.recv())

        assert result["m2m:rsp"]["rqi"] == reqid
        assert result["m2m:rsp"]["to"] == DaikinAltherma.UserAgent

        return dpath.util.get(result, output_path)

    def _requestValueHP(self, item: str, output_path: str, payload=None):
        return self._requestValue(f"MNAE/{item}", output_path, payload)

    @property
    def adapter_model(self) -> str:
        """ Returns the model of the LAN adapter """
        # either BRP069A61 or BRP069A62
        return self._requestValue("MNCSE-node/deviceInfo", "/m2m:rsp/pc/m2m:dvi/mod")

    @property
    def tank_temperature(self) -> float:
        """ Returns the hot water tank temperature, in °C """
        return self._requestValueHP(
            "2/Sensor/TankTemperature/la", "/m2m:rsp/pc/m2m:cin/con"
        )

    @property
    def indoor_temperature(self) -> float:
        """ Returns the indoor temperature, in °C """
        return self._requestValueHP(
            "1/Sensor/IndoorTemperature/la", "/m2m:rsp/pc/m2m:cin/con"
        )

    @property
    def outdoor_temperature(self) -> float:
        """ Returns the outdoor temperature, in °C """
        return self._requestValueHP(
            "1/Sensor/OutdoorTemperature/la", "/m2m:rsp/pc/m2m:cin/con"
        )

    @property
    def leaving_water_temperature(self) -> float:
        """ Returns the heating leaving water temperature, in °C """
        return self._requestValueHP(
            "1/Sensor/LeavingWaterTemperatureCurrent/la", "m2m:rsp/pc/m2m:cin/con"
        )

    @property
    def power_state(self) -> bool:
        """ Returns the power state """
        return self._requestValueHP("1/Operation/Power/la", "m2m:rsp/pc/m2m:cin/con") == "on"

    @property
    def tank_power_state(self) -> bool:
        """ Returns the tank power state """
        return self._requestValueHP("2/Operation/Power/la", "m2m:rsp/pc/m2m:cin/con") == "on"


    @property
    def tank_powerful_state(self) -> bool:
        """ Returns the tank powerful state """
        return self._requestValueHP("2/Operation/Powerful/la", "m2m:rsp/pc/m2m:cin/con") == 1

    @property
    def power_consumption(self) -> dict:
        """ Returns the energy consumption in kWh per [D]ay, [W]eek, [M]onth """
        return self._requestValueHP("1/Consumption/la", "m2m:rsp/pc/m2m:cin/con")

    def set_heating(self, heating_active: bool):
        """ Whether to turn the heating on(True) or off(False).
        You can confirm that it works by calling self.power_state
        """
        mode_dict = {
            True: 'on',
            False: 'standby',
        }

        payload = {
            'con': mode_dict[heating_active],
            'cnf': 'text/plain:0',
        }

        self._requestValueHP("1/Operation/Power", "/", payload)


    def set_tank_heating(self, powerful_active: bool):
        """ Whether to turn the water tank heating on(True) or off(False).
        You can confirm that it works by calling self.tank_powerful_state
        """
        mode_dict = {
            True: 1,
            False: 0,
        }

        payload = {
            'con': mode_dict[powerful_active],
            'cnf': 'text/plain:0',
        }

        self._requestValueHP("2/Operation/Powerful", "/", payload)

if __name__ == "__main__":
    ad = DaikinAltherma("192.168.10.126")
    print(ad.adapter_model)
    print(ad.tank_temperature)
    print(ad.outdoor_temperature)
    print(ad.indoor_temperature)
    print(ad.leaving_water_temperature)
    print(ad.power_state)
    print(ad.power_consumption)
    ad.set_heating(True)
    print(ad.power_state)
    print(ad.tank_power_state)
    print(ad.tank_powerful_state)
