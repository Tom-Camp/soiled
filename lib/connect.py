import gc
import network
import time


gc.enable()


class Connect:
    def __init__(self, ssid: str, password: str, hostname: str):
        self.ssid = ssid
        self.password = password
        self.status: bool = False
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.hostname = network.hostname(hostname)

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
