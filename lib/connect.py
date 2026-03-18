import gc
import network
import time

from secrets import SSID, PASSWORD, HOSTNAME


gc.enable()


class Connect:
    ssid: str = SSID
    password: str = PASSWORD
    status: bool = False
    wlan: network.WLAN = network.WLAN(network.STA_IF)

    def __init__(self):
        network.hostname(HOSTNAME)
        self.wlan.active(True)

    def connect(self):
        self.wlan.connect(self.ssid, self.password)
        max_wait = 10
        while max_wait > 0:
            status: int = self.wlan.status()  # type: ignore[assignment]
            if status < 0 or status >= 3:
                break
            max_wait -= 1
            print("waiting for connection...")
            time.sleep(1)

        if self.wlan.status() != 3:  # type: ignore[operator]
            raise OSError(
                "WiFi connection failed, status: {}".format(self.wlan.status())
            )
        else:
            print("connected")
