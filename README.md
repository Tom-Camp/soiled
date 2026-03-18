# 🐛 ESP32-S2 Soil Sensor 🥕

MicroPython firmware for an ESP32-S2 that reads soil moisture and temperature from an Adafruit STEMMA Soil 
ensor and POSTs readings to a remote API every hour using deep sleep between readings.

## ⚙️ Hardware

| Component       | Details                                                        |
|-----------------|----------------------------------------------------------------|
| Microcontroller | ESP32-S2 (e.g. Adafruit QT PY with uFL Antenna Port)           |
| Sensor          | Adafruit STEMMA Soil Sensor (I2C, address `0x36`)              |
| Power           | Adafruit LiIon/LiPoly Charger BFF Add-On + 3.7V LiPo battery   |
| Connections     | Sensor SDA/SCL via STEMMA QT connector (GPIO 21/22 by default) |

## 👷 How It Works

On each wake cycle:
1. Connects to Wi-Fi
2. Reads moisture (capacitive) and temperature from the soil sensor
3. Converts temperature from Celsius to Fahrenheit
4. POSTs `{"soil": {"moisture": <int>, "soil_temp": <float>}}` to the configured API endpoint
5. Disables WiFi and enters deep sleep for 1 hour

## 🗂️ File Structure

```
main.py                    # Entry point: WiFi, sensor read, HTTP POST, deep sleep
lib/
  connect.py               # WiFi connection via network.WLAN
  request.py               # HTTP POST via MicroPython requests module
  seesaw.py                # Low-level I2C driver for Adafruit SeeSaw chip
  stemma_soil_sensor.py    # STEMMA soil sensor driver (get_temp, get_moisture)
secrets.py                 # WiFi/API credentials — not in git, must be created manually
```

## 🎨 Setup

### 1. Flash MicroPython

Flash a MicroPython image for ESP32-S2 onto the device before proceeding.

### 2. Create `secrets.py`

Create `secrets.py` in the project root (it is gitignored). This file must be deployed to the device 
separately.

```python
SSID = "your-wifi-ssid"
PASSWORD = "your-wifi-password"
HOSTNAME = "soilsensor"
API_URL = "https://your-api.example.com/readings"
API_KEY = "your-api-key"
DEVICE_ID = "your-device-id"
I2C_ID = 0       # I2C bus ID
SDA_PIN = 21     # GPIO pin number
SCL_PIN = 22     # GPIO pin number
```

### 3. Deploy to Device

Install `mpremote` and copy files to the device:

```bash
# Install mpremote
uv run mpremote

# Copy source files
mpremote cp main.py :main.py
mpremote cp lib/connect.py :lib/connect.py
mpremote cp lib/request.py :lib/request.py
mpremote cp lib/seesaw.py :lib/seesaw.py
mpremote cp lib/stemma_soil_sensor.py :lib/stemma_soil_sensor.py

# Copy secrets (not in git)
mpremote cp secrets.py :secrets.py
```

### 4. Verify

Open the REPL to observe output on first boot:

```bash
mpremote repl
```

## API Payload

```json
{
  "soil": {
    "moisture": 850,
    "soil_temp": 68.4
  }
}
```

Headers sent with each request:
- `Content-Type: application/json`
- `X-API-KEY: <API_KEY>`
- `X-Device-Id: <DEVICE_ID>`

## 🏗️ Development

The local Python environment (managed by `uv`) is for type-checking stubs only — no code runs 
locally. MicroPython runs on the device.

```bash
# Install dev dependencies (type stubs, pre-commit)
uv sync

# Install pre-commit hooks
uv run pre-commit install
```

## 📝 License

This project is licensed under the AGPL-3.0 License - see the [LICENSE](LICENSE) file for details.

