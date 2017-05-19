import ntptime
import sys
import utime
import urequests
from app_config import MAKER_KEY, WEATHER_API_KEY, CITY, CITY_COORDS, TIME_RANGE

WEATHER_API_URL = ("https://api.darksky.net/forecast/{key}/{coords}?units=si&exclude=minutely,hourly,daily,alerts,"
                   "flags")
PUSH_NOTIFICATION_API_URL = "http://maker.ifttt.com/trigger/weather_info/with/key/{key}"

RETRY_MIN = 30


def get_weather_info(city_coords=CITY_COORDS):
    city_coords_str = ",".join(city_coords)
    response = urequests.get(WEATHER_API_URL.format(key=WEATHER_API_KEY, coords=city_coords_str))
    weather_info = response.json()
    temperature = round(float(weather_info["currently"]["temperature"]))
    rain_probability = round(float(weather_info["currently"]["precipProbability"]) * 100)
    return temperature, rain_probability


def send_push_notification(city, temperature, rain_probability):
    post_data = {"value1": city, "value2": temperature, "value3": rain_probability}
    url = PUSH_NOTIFICATION_API_URL.format(key=MAKER_KEY)
    urequests.post(url, json=post_data, headers={"Content-Type": "application/json"})


def check_time():
    try:
        time_min, time_max = TIME_RANGE
        time_min_hour, time_min_minute = map(int, time_min.split(":"))
        time_max_hour, time_max_minute = map(int, time_max.split(":"))

        now = utime.localtime(ntptime.time())
        now_hour = now[3]
        now_minute = now[4]
        if time_max_minute == 0:
            time_max_minute = 60
        return time_min_hour <= now_hour <= time_max_hour and time_min_minute <= now_minute <= time_max_minute
    except Exception as e:
        if not isinstance(e, KeyboardInterrupt):
            print("Error while calculating if it is the correct time to trigger: {}".format(e))
        raise


def main():
    print("Initializing loop")
    while True:
        try:
            if check_time():
                temperature, rain_probability = get_weather_info()
                send_push_notification(CITY, temperature, rain_probability)
                print("Notification sent, going to sleep for longer")
                utime.sleep(20 * 60 * 60)
            else:
                print("Not time yet, retrying in {} min".format(str(RETRY_MIN)))
                utime.sleep(RETRY_MIN * 60)
        except Exception as e:
            if isinstance(e, KeyboardInterrupt):
                print("Exiting...")
                sys.exit(0)
            print("Unexpected error: {}, retrying".format(e))
            pass


if __name__ == '__main__':
    main()
