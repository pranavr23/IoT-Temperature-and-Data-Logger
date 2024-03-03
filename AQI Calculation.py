
from main import field_2a
from main import field_3a

import RPi.GPIO as RPi
import thingspeak
import time

RPi.setmode(RPi.BCM)
RPi.setwarnings(False)

#----------- Accessing the thinkspeak Channel--------------
channel_id = 1838967
write_key = 'HO54N08LMMADQWBQ'
channel = thingspeak.Channel(id=channel_id, api_key=write_key)
# Function for calculation of AQI
def pm25_aqi(x):  # for pm2.5
    if 0 <= x <= 12.0:
        aqi_value = (((50 - 0) * (x - 0)) / (12 - 0)) + 0
    elif 12.1 <= x <= 35.4:
        aqi_value = (((100 - 51) * (x - 12.1)) / (35.4 - 12.1)) + 51
    elif 35.5 <= x <= 55.4:
        aqi_value = (((150 - 101) * (x - 35.5)) / (55.5 - 35.5)) + 101
    elif 55.5 <= x <= 150.4:
        aqi_value = (((200 - 151) * (x - 55.5)) / (150.4 - 55.5)) + 151
    elif 150.5 <= x <= 250.4:
        aqi_value = (((300 - 201) * (x - 150.5)) / (250.4 - 150.5)) + 201
    elif 250.5 <= x <= 350.4:
        aqi_value = (((400 - 301) * (x - 250.5)) / (350.4 - 250.5)) + 301
    elif 350.5 <= x <= 500.4:
        aqi_value = (((500 - 401) * (x - 350.5)) / (500.4 - 350.5)) + 401
    aqi_value = "{:.2f}".format(aqi_value)
    return aqi_value


def pm10_aqi(x):  # for pm10
    if 0 <= x <= 54.0:
        aqi_value = (((50 - 0) * (x - 0)) / (54 - 0)) + 0
    elif 55 <= x <= 154:
        aqi_value = (((100 - 51) * (x - 55)) / (154 - 55)) + 51
    elif 155 <= x <= 254:
        aqi_value = (((150 - 101) * (x - 155)) / (254 - 155)) + 101
    elif 255 <= x <= 354:
        aqi_value = (((200 - 151) * (x - 255)) / (354 - 255)) + 151
    elif 355 <= x <= 424:
        aqi_value = (((300 - 201) * (x - 355)) / (424 - 355)) + 201
    elif 425 <= x <= 504:
        aqi_value = (((400 - 301) * (x - 425)) / (504 - 425)) + 301
    elif 505 <= x <= 604:
        aqi_value = (((500 - 401) * (x - 505)) / (604 - 505)) + 401
    aqi_value = "{:.2f}".format(aqi_value)
    return aqi_value


aqi_pm25 = []
for i in field_2a:  # for pm2.5
    v = pm25_aqi(i)
    aqi_pm25.append(v)
aqi_pm10 = []
for i in field_3a:  # for pm10
    v = pm10_aqi(i)
    aqi_pm10.append(v)
print(aqi_pm25)
print(aqi_pm10)

# .............3.3.2 Transfer AQI levels to a new cloud channel
Maximum_AQI = []
z = 0
while z < 100:
    # check the channel "https://thingspeak.com/channels/1838967" with this link
    if aqi_pm25[z] < aqi_pm10[z]:
        v = aqi_pm10[z]
        Maximum_AQI.append(v)
    if aqi_pm10[z] < aqi_pm25[z]:
        v = aqi_pm25[z]
        Maximum_AQI.append(v)
    channel.update({'field1': aqi_pm25[z], 'field2': aqi_pm10[z], 'field3': Maximum_AQI[z]})
    time.sleep(0.25)
    z += 1
