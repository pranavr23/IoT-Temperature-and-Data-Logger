# .......Local temperature and Humidity Measurement........


import matplotlib.pyplot as plt
import RPi.GPIO as RPi
import dht11
from main import field_6
from main import field_7


RPi.setmode(RPi.BCM)

RPi.setwarnings(False)
RPi.cleanup()
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
    instance = dht11.DHT11( pin = 4)
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
    plt.subplot(2, 1, 1)
    average_temp = sum(temp_cld_in_degreeC) / len(temp_cld_in_degreeC)
    plt.plot(range(100), temp_cld_in_degreeC, 'rd-')
    plt.axhline(y=average_temp, color='r', linestyle='--')
    plt.ylabel('Temp in deg C')
    plt.title('Temperature')
    plt.subplot(2, 1, 2)
    average_hum = int(sum(humi_cld)) / int(len(humi_cld))
    plt.plot(range(100), humi_cld, 'bo-')
    plt.axhline(y=average_hum, color='b', linestyle='--')
    plt.ylabel('Humidity %')
    plt.title('Humidity')
    plt.show()
    plt.close()
    plt.close()
