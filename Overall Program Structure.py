import json
from statistics import mean
import RPi.GPIO as RPi
import dht11
import matplotlib.pyplot as plt
import requests
import thingspeak
import time
from time import sleep
from Adafruit_LED_Backpack import SevenSegment
from luma.core.interface.serial import spi, noop
from luma.led_matrix.device import max7219
from luma.core.render import canvas

RPi.setmode(RPi.BCM)
RPi.setwarnings(False)
RPi.cleanup()
serial = spi(port=0, device=1, gpio=noop())
device = max7219(serial, cascaded=1, block_orientation=90, rotate=0)
segment_7SD = SevenSegment.SevenSegment(address=0x70)
segment_7SD.begin()

PinButtonLeft = 25
PinButtonRight = 19

RPi.setmode(RPi.BCM)

RPi.setup(PinButtonLeft, RPi.IN, pull_up_down=RPi.PUD_OFF)
RPi.setup(PinButtonRight, RPi.IN, pull_up_down=RPi.PUD_OFF)



#----------- Accessing the thinkspeak Channel--------------
field_data = requests.get('https://thingspeak.com/channels/628559/feed.json')  # Resquest an HTTP library
# ----------- Accessing the thinkspeak Channel--------------
channel_id = 1838967
write_key = 'HO54N08LMMADQWBQ'
channel = thingspeak.Channel(id=channel_id, api_key=write_key)
#----------- Decoding the cloud reading by using JSON--------------
fields = json.loads(field_data.text)
channels= fields['channel']
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
w=0
while w<=99:
    data = feeds[w]['field1']
    field_1.append(data)

    data = feeds[w]['field2']
    field_2.append(data)

    data = feeds[w]['field3']
    field_3.append(data)

    data = feeds[w]['field4']
    field_4.append(data)

    data = feeds[w]['field5']
    field_5.append(data)

    data = feeds[w]['field6']
    field_6.append(data)

    data = feeds[w]['field7']
    field_7.append(data)

    data = feeds[w]['field8']
    field_8.append(data)
    w+=1


# Printing the field Datas
print('Field 1 data is -', field_1)
print('\nField 2 data is -', field_2)
print('\nField 3 data is -', field_3)
print('\nField 4 data is -', field_4)
print('\nField 5 data is -', field_5)
print('\nField 6 data is -', field_6)
print('\nField 7 data is -', field_7)
print('\nField 8 data is -', field_8)

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
for f in field_6a:
    tc = (f - 32) * (5 / 9)
    field_6_c.append(tc)
    f = f + 1
temp_cld_in_degreeC = list(map(float, field_6_c))
field_7a = list(map(float, field_7))
humi_cld = field_7a

print(temp_cld_in_degreeC)
print(humi_cld)
average_temp = sum(temp_cld_in_degreeC) / len(temp_cld_in_degreeC)
average_hum = int(sum(humi_cld)) / int(len(humi_cld))
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
# Part 2
t = 1

a = [0, 1, 2, 3, 4]
# Selection of measured value to be visualized
# value of K
# 0 i.e A) PM1.0
# 1 i.e B) PM2.5
# 2 i.e C) PM10.0
# 3 i.e D) Temperature
# 4 i.e E) Humidity

k = 0 # used for selection of measurement
#  Visualization with respect to button
# Press button for 2 seconds
while True:
    print("Button is not pressed! - press for 2 sec to change", k, 'time', t)
    if (k >= 0) & (k <= 4):  # this system always starts with the indication of measurement A) PM1.0
        with canvas(device) as draw:
            draw.line([a[k], 0, a[k], 0], fill="white")  # 3.4.1 Matrix LED display shows the actual indication of measurement selected
        sleep(0.5)
        # Press button for 2 seconds
        if not RPi.input(PinButtonRight):  # List of measurement in Right Direction
            k = k + 1
            if k > 4:
                print("Out of Scope")
                k = 0
                with canvas(device) as draw:
                    draw.line([a[k], 0, a[k], 0],
                              fill="white")  # Matrix LED display shows the actual indication of measurement selected
                sleep(0.5)
                print("Right Button is pressed!")
            if (k >= 0) & (k <= 4):
                with canvas(device) as draw:
                    draw.line([a[k], 0, a[k], 0],
                              fill="white")  # Matrix LED display shows the actual indication of measurement selected
                sleep(0.5)
                print("Right Button is pressed!")
        # Press button for 2 seconds
        if not RPi.input(PinButtonLeft):  # List of measurement in Left Direction
            k = k - 1
            if k < 0:
                print("Out of Scope")
                k = 4
                with canvas(device) as draw:
                    draw.line([a[k], 0, a[k], 0],
                              fill="white")  # Matrix LED display shows the actual indication of measurement selected
                sleep(0.5)
                print("Left Button is pressed!")
            if (k >= 0) & (k <= 4):
                with canvas(device) as draw:
                    draw.line([a[k], 0, a[k], 0],
                              fill="white")  # Matrix LED display shows the actual indication of measurement selected
                sleep(0.5)
                print("left Button is pressed!")  # Press button for 2 seconds
        if k == 0:  # iteration of condition code for PM1.0
            mean_PM1 = mean_field1
            StrMeasurement = str(float(round(mean_PM1, 2)))
            for y in range(0, len(StrMeasurement)):
                segment_7SD.set_digit(y, StrMeasurement[y],
                                      decimal=False)  # 3.4.2 Display mean values on the seven segment display (7SD)
                segment_7SD.set_decimal(1, 1)
            segment_7SD.write_display()
            bh = []
            for j in range(0, 8):
                adding = 0
                z = 0
                for i in range((j * 12), ((j * 12) + 12)):  # 3.4.3 Division of 100 datas into 8 different periods
                    adding = adding + field_1a[i]
                    z = z + 1
                # print(z)
                # print(adding)
                bh1 = adding / z
                percentage_pm1 = int(round(6 * (bh1 / 10)))
                bh.append(percentage_pm1)
                # print(bh)
            with canvas(device) as draw:
                for i in range(0, 8):
                    draw.line([i, 8 - bh[i], i, 8 - bh[i]],
                              fill="white")  # 3.4.3 Visualizing the measurements on the Matrix LED Display (MLD)
            sleep(0.8)

        if k == 1:  # iteration of condition code for PM2.5
            mean_PM2_5 = mean_field2
            StrMeasurement = str(float(round(mean_PM2_5, 2)))
            for y in range(0, len(StrMeasurement)):
                segment_7SD.set_digit(y, StrMeasurement[y], decimal=False)
                segment_7SD.set_decimal(1, 1)
            segment_7SD.write_display()
            bh = []
            for j in range(0, 8):
                adding = 0
                z = 0
                for i in range((j * 12), ((j * 12) + 12)):
                    adding = adding + field_2a[i]
                    z = z + 1
                # print(z)
                # print(adding)
                bh1 = adding / z
                percentage_pm1 = int(round(6 * (bh1 / 10)))
                bh.append(percentage_pm1)
                # print(bh)
            with canvas(device) as draw:
                for i in range(0, 8):
                    draw.line([i, 8 - bh[i], i, 8 - bh[i]], fill="white")
            sleep(0.8)
        if k == 2:  # iteration of condition code for PM10
            mean_PM10 = mean_field3
            StrMeasurement = str(float(round(mean_PM10, 2)))
            for y in range(0, len(StrMeasurement)):
                segment_7SD.set_digit(y, StrMeasurement[y], decimal=False)
                segment_7SD.set_decimal(1, 1)
            segment_7SD.write_display()
            bh = []
            for j in range(0, 8):
                adding = 0
                z = 0
                for i in range((j * 12), ((j * 12) + 12)):
                    adding = adding + field_3a[i]
                    z = z + 1
                # print(z)
                # print(adding)
                bh1 = adding / z
                percentage_pm1 = int(round(6 * (bh1 / 10)))
                bh.append(percentage_pm1)
                # print(bh)
            with canvas(device) as draw:
                for i in range(0, 8):
                    draw.line([i, 8 - bh[i], i, 8 - bh[i]],
                              fill="white")  # Visualizing the measurements on the Matrix LED Display (MLD)
            sleep(0.8)
        if k == 3:  # iteration of condition code for temperature
            mean_temp = average_temp * 100
            print("the temperaturee is average_temp from the cloud", average_temp)
            StrMeasurement = str(float(round(mean_temp, 2)))
            for y in range(0, len(StrMeasurement)):
                segment_7SD.set_digit(y, StrMeasurement[y], decimal=False)
                segment_7SD.set_decimal(1, 1)
            segment_7SD.write_display()
            bh = []
            for j in range(0, 8):
                adding = 0
                z = 0
                for i in range((j * 12), ((j * 12) + 12)):
                    adding = adding + temp_cld_in_degreeC[i]
                    z = z + 1
                # print(z)
                # print(adding)
                bh1 = adding / z
                percentage_pm1 = int(round(6 * (bh1 / 100)))
                bh.append(percentage_pm1)
                # print(bh)
            with canvas(device) as draw:
                for i in range(0, 8):
                    draw.line([i, 8 - bh[i], i, 8 - bh[i]], fill="white")
            sleep(0.8)
        if k == 4:  # iteration of condition code for humidity
            mean_hum = average_hum * 100
            print("the humidity is average_hum from the cloud", average_hum)
            StrMeasurement = str(float(round(mean_hum, 2)))
            for y in range(0, len(StrMeasurement)):
                segment_7SD.set_digit(y, StrMeasurement[y], decimal=False)
                segment_7SD.set_decimal(1, 1)
            segment_7SD.write_display()
            bh = []
            for j in range(0, 8):
                adding = 0
                z = 0
                for i in range((j * 12), ((j * 12) + 12)):
                    adding = adding + humi_cld[i]
                    z = z + 1
                # print(z)
                # print(adding)
                bh1 = adding / z
                percentage_pm1 = int(round(6 * (bh1 / 100)))
                bh.append(percentage_pm1)
                # print(bh)
            with canvas(device) as draw:
                for i in range(0, 8):
                    draw.line([i, 8 - bh[i], i, 8 - bh[i]], fill="white")
            sleep(0.8)

    if t % 60 == 0:
        # ----------- Accessing the thinkspeak Channel--------------
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
        w = 0
        while w <= 99:
            data = feeds[w]['field1']
            field_1.append(data)

            data = feeds[w]['field2']
            field_2.append(data)

            data = feeds[w]['field3']
            field_3.append(data)

            data = feeds[w]['field4']
            field_4.append(data)

            data = feeds[w]['field5']
            field_5.append(data)

            data = feeds[w]['field6']
            field_6.append(data)

            data = feeds[w]['field7']
            field_7.append(data)

            data = feeds[w]['field8']
            field_8.append(data)
            w += 1

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
        for f in field_6a:
            tc = (f - 32) * (5 / 9)
            field_6_c.append(tc)
            f = f + 1
        temp_cld_in_degreeC = list(map(float, field_6_c))
        field_7a = list(map(float, field_7))
        humi_cld = field_7a

        print(temp_cld_in_degreeC)
        print(humi_cld)


    # ........ Getting Temperature and Humidity Measurement every 10 seconds.......
    if t % 10 == 0 or t == 1 :
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
        
        # user interface include all local visualizaton and shall rum continuosly

        plt.subplot(5, 1, 1)
        plt.plot(range(100), field_1a, 'rd-')
        plt.axhline(y=mean_field1, color='r', linestyle='--')
        plt.xlabel('sample')
        plt.ylabel('ATM')
        plt.title('PM 1.0')

        plt.subplot(5, 1, 2)
        plt.plot(range(100), field_2a, 'ko-')
        plt.axhline(y=mean_field2, color='black', linestyle='--')
        plt.xlabel('sample')
        plt.ylabel('ATM')
        plt.title('PM 2.5')

        plt.subplot(5, 1, 3)
        plt.plot(range(100), field_3a, 'bo-')
        plt.axhline(y=mean_field3, color='b', linestyle='--')
        plt.xlabel('sample')
        plt.ylabel('ATM')
        plt.title('PM 10')
        plt.subplot(5, 1, 4)
        average_temp = sum(temp_cld_in_degreeC) / len(temp_cld_in_degreeC)
        plt.plot(range(100), temp_cld_in_degreeC, 'rd-')
        plt.axhline(y=average_temp, color='r', linestyle='--')
        plt.ylabel('Temp in deg C')
        plt.title('Temperature')
        plt.subplot(5, 1, 5)
        average_hum = int(sum(humi_cld)) / int(len(humi_cld))
        plt.plot(range(100), humi_cld, 'bo-')
        plt.axhline(y=average_hum, color='b', linestyle='--')
        plt.ylabel('Humidity %')
        plt.title('Humidity')
        plt.show()
        
        # .............Transfer AQI levels to a new cloud channel every minute
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
        Maximum_AQI = []
        z = 0
        q = z + 99
        while z < 1:
            # check the channel "https://thingspeak.com/channels/1838967" with this link
            if aqi_pm10[q] > aqi_pm25[q]:
                v = aqi_pm25[q]
                Maximum_AQI.append(v)
                print(v)
            else:
                v = aqi_pm10[q]
                Maximum_AQI.append(v)
            print('channel updated')
            channel.update({'field1': aqi_pm25[q], 'field2': aqi_pm10[q], 'field3': Maximum_AQI[z-1]})
            time.sleep(0.25)
            z= z+1
        t = t + 1
    t = t + 1

