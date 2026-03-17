# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MicroPython firmware for an ESP32-S2 that reads from an Adafruit STEMMA Soil Sensor (I2C capacitive 
moisture/temperature sensor) and POSTs readings to a remote API every hour.

**Runtime**: MicroPython on ESP32-S2 — not CPython. Standard library availability is limited. The local 
Python 3.14 environment (managed by `uv`) is only for type-checking stubs; no code runs locally.

## Hardware

- **Microcontroller**: ESP32-S2 (e.g. Adafruit QT PY with uFL Antenna Port)
- **Sensor**: Adafruit STEMMA Soil Sensor (I2C address `0x36`)
- **Power connection**: Adafruit LiIon or LiPoly Charger BFF Add-On for QT Py
- **Power**: 3.7V LiPo battery (e.g. 2000mAh) connected to charger add-on
- **Connections**: Sensor SDA to ESP32 GPIO (e.g. 21), SCL to GPIO (e.g. 22) via STEMA QT Py I2C port

## Deploying to Device

Files are uploaded directly to the ESP32 using `mpremote` or `ampy`. There is no build step.

```bash
# Install mpremote
uv run mpremote

# Copy all source files to device
mpremote cp main.py :main.py
mpremote cp lib/connect.py :lib/connect.py
mpremote cp lib/request.py :lib/request.py
mpremote cp lib/seesaw.py :lib/seesaw.py
mpremote cp lib/stemma_soil_sensor.py :lib/stemma_soil_sensor.py

# Also deploy secrets.py (not in git)
mpremote cp secrets.py :secrets.py

# Open REPL
mpremote repl
```

## Configuration (secrets.py)

`secrets.py` is gitignored and must be created manually on the device or copied separately. Required 
variables:

```python
SSID = "..."
PASSWORD = "..."
HOSTNAME = "..."
API_URL = "https://..."
API_KEY = "..."
DEVICE_ID = "..."
I2C_ID = 0          # I2C bus ID
SDA_PIN = ...       # GPIO pin number
SCL_PIN = ...       # GPIO pin number
```

## Architecture

```
main.py                      # Entry point: init WiFi + I2C, polling loop (1hr interval)
lib/
  connect.py                 # Connect class — WiFi via network.WLAN; resets device on failure
  request.py                 # Requester class — HTTP POST via MicroPython requests module
  seesaw.py                  # Low-level I2C driver for Adafruit SeeSaw chip (ported from CircuitPython)
  stemma_soil_sensor.py      # StemmaSoilSensor(Seesaw) — get_temp() and get_moisture()
```

The sensor driver layer: `seesaw.py` handles raw I2C register reads/writes; `stemma_soil_sensor.py` extends 
it with the specific register addresses and decoding for the STEMMA soil sensor (I2C address `0x36`).

`main.py` converts temperature from Celsius to Fahrenheit before posting. The posted payload is:`{"soil": 
{"moisture": <int>, "soil_temp": <float>}}`.

## MicroPython Constraints

- No `f-strings` with complex expressions in older MicroPython versions
- `ustruct` instead of `struct`, `utime` may be needed instead of `time` on some builds
- `const()` is a MicroPython optimization for integer constants — keep it for register definitions
- Memory is tight; `gc.collect()` is called each loop iteration
- `requests` module is MicroPython's built-in HTTP client — always call `response.close()` to free sockets
