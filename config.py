import ujson

CONFIG_FILE = "config.json"

CONFIG_DICT = ujson.loads(CONFIG_FILE)

WLAN_SSID = CONFIG_DICT["wlan_ssid"]
WLAN_PASSWORD = CONFIG_DICT["wlan_password"]
