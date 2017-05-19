import ujson

CONFIG_FILE = "config.json"

CONFIG_DICT = ujson.load(open(CONFIG_FILE))

WLAN_SSID = CONFIG_DICT["wlan_ssid"]
WLAN_PASSWORD = CONFIG_DICT["wlan_password"]
MAKER_KEY = CONFIG_DICT["maker_key"]
WEATHER_API_KEY = CONFIG_DICT["weather_api_key"]
CITY_COORDS = CONFIG_DICT["city_coords"]
CITY = CONFIG_DICT["city"]
TIME_RANGE = CONFIG_DICT["time_range"]
