import gc
import secrets
import sys
import time

from machine import Pin, I2C

from lib.connect import Connect
from lib.request import Requester
from lib.stemma_soil_sensor import StemmaSoilSensor

wifi = Connect(
    ssid=secrets.SSID,
    password=secrets.PASSWORD,
    hostname=secrets.HOSTNAME,
)
wifi.connect()

requester = Requester(secrets.API_URL)

soil_i2c = I2C(
    secrets.I2C_ID,
    sda=Pin(secrets.SDA_PIN),
    scl=Pin(secrets.SCL_PIN),
    freq=20000,
)
tzo = 4

gc.enable()


def c_to_f(c_temp: float) -> float:
    return (c_temp * 9 / 5) + 32


def soil() -> dict:
    try:
        soil_sensor = StemmaSoilSensor(soil_i2c)
        soil_sensor_data = {
            "moisture": soil_sensor.get_moisture(),
            "soil_temp": c_to_f(soil_sensor.get_temp()),
        }
    except ValueError as er:
        soil_sensor_data = {"error": str(er)}
    finally:
        pass

    return soil_sensor_data


while True:
    try:
        soil_data = soil()
        data: dict = {
            "soil": soil_data,
        }
        _ = requester.post(data=data)

    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except Exception as exc:
            raise f"System exit exception: {exc}"
    gc.collect()
    time.sleep(3600)
