import gc
import secrets

from machine import Pin, I2C, deepsleep

from lib.connect import Connect
from lib.request import Requester
from lib.stemma_soil_sensor import StemmaSoilSensor

gc.enable()

SLEEP_MS = 3600 * 1000


def c_to_f(c_temp: float) -> float:
    return (c_temp * 9 / 5) + 32


def soil(i2c) -> dict:
    try:
        soil_sensor = StemmaSoilSensor(i2c)
        return {
            "moisture": soil_sensor.get_moisture(),
            "soil_temp": c_to_f(soil_sensor.get_temp()),
        }
    except ValueError as er:
        return {"error": str(er)}


wifi = Connect(
    ssid=secrets.SSID,
    password=secrets.PASSWORD,
    hostname=secrets.HOSTNAME,
)

try:
    wifi.connect()

    soil_i2c = I2C(
        secrets.I2C_ID,
        sda=Pin(secrets.SDA_PIN),
        scl=Pin(secrets.SCL_PIN),
        freq=20000,
    )

    requester = Requester(secrets.API_URL)
    requester.post(data={"soil": soil(soil_i2c)})
finally:
    wifi.wlan.active(False)
    gc.collect()
    deepsleep(SLEEP_MS)
