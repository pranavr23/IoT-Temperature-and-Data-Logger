import json
from statistics import mean
import RPi.GPIO as RPi
import dht11
import matplotlib.pyplot as plt
import requests
import thingspeak
import time

RPi.setmode(RPi.BCM)
RPi.setwarnings(False)
RPi.cleanup()

# ----------- Accessing the thinkspeak Channel--------------
channel_id = 1838967
write_key = 'HO54N08LMMADQWBQ'
channel = thingspeak.Channel(id=channel_id, api_key=write_key)
field_data = requests.get('https://thingspeak.com/channels/628559/feed.json')

# ----------- Decoding the cloud reading by using JSON--------------
fields = json.loads(field_data.text)
channels = fields['channel']
feeds = fields['feeds']
field_1 = []
field_2 = []
field_3 = []
field_4 = []
field_5 = []
field_6 = []
field_7 = []
field_8 = []

# Accessing the Entries and appending it.
a = 0
while a <= 99:
    data = feeds[a]['field1']
    field_1.append(data)

    data = feeds[a]['field2']
    field_2.append(data)

    data = feeds[a]['field3']
    field_3.append(data)

    data = feeds[a]['field4']
    field_4.append(data)

    data = feeds[a]['field5']
    field_5.append(data)

    data = feeds[a]['field6']
    field_6.append(data)

    data = feeds[a]['field7']
    field_7.append(data)

    data = feeds[a]['field8']
    field_8.append(data)
    a += 1

# Printing the field Datas
print('Field 1 data is -', field_1)
print('\nField 2 data is -', field_2)
print('\nField 3 data is -', field_3)
print('\nField 4 data is -', field_4)
print('\nField 5 data is -', field_5)
print('\nField 6 data is -', field_6)
print('\nField 7 data is -', field_7)
print('\nField 8 data is -', field_8)

# Mean Values of the field Datas
field_1a = list(map(float, field_1))
mean_field1 = mean(field_1a)
print('Mean value of field1 is', mean_field1)
field_2a = list(map(float, field_2))
mean_field2 = mean(field_2a)
print('Mean value of field2 is', mean_field2)
field_3a = list(map(float, field_3))
mean_field3 = mean(field_3a)
print('Mean value of field3 is', mean_field3)

field_6a = list(map(float, field_6))
# ......convert temperature in degree celsius
field_6_c = []
for a in field_6a:
    t = (a - 32) * (5 / 9)
    field_6_c.append(t)
    a = a + 1
temp_cld_in_degreeC = list(map(float, field_6_c))
field_7a = list(map(float, field_7))
humi_cld = field_7a

print(temp_cld_in_degreeC)
print(humi_cld)
# ........Getting Temperature and Humidity Measurement.......
while True:
    instance = dht11.DHT11(pin=4)
    result = instance.read()
    while not result.is_valid():
        result = instance.read()

    temp = result.temperature
    hum = result.humidity
    print("Temperature: %-3.1f C" % temp)
    print("Humidity: %-3.1f %%" % hum)
    temp_cld_in_degreeC.append(temp)
    humi_cld.append(hum)
    # ........Implementation of FIFO data buffer.....
    if len(temp_cld_in_degreeC) > 100:
        temp_cld_in_degreeC.pop(0)  # use of pop function
    if len(humi_cld) > 100:
        humi_cld.pop(0)
    # .....................Visualizing temperature and humidity measurements and mean values........

    average_temp = sum(temp_cld_in_degreeC) / len(temp_cld_in_degreeC)

    average_hum = int(sum(humi_cld)) / int(len(humi_cld))
    break
