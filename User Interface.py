


# .......... User Interface
import RPi.GPIO as RPi
from luma.core.interface.serial import spi, noop
from luma.led_matrix.device import max7219
from luma.core.render import canvas
from time import sleep
from Adafruit_LED_Backpack import SevenSegment
from main import mean_field1, humi_cld
from main import mean_field2
from main import mean_field3
from main import average_temp
from main import average_hum
from main import field_1a
from main import field_2a
from main import field_3a
from main import temp_cld_in_degreeC
from main import humi_cld
serial = spi(port=0, device=1, gpio=noop())
device = max7219(serial, cascaded=1, block_orientation=90, rotate=0)
segment_7SD = SevenSegment.SevenSegment(address=0x70)
segment_7SD.begin()

PinButtonLeft = 25
PinButtonRight = 19

RPi.setmode(RPi.BCM)

RPi.setup(PinButtonLeft, RPi.IN, pull_up_down=RPi.PUD_OFF)
RPi.setup(PinButtonRight, RPi.IN, pull_up_down=RPi.PUD_OFF)

while 1:
    print("Button is pressed! - press for 2 sec to change", k)
    if (k >= 0) & (k <= 4): # this system always starts with the indication of measurement A) PM1.0
        with canvas(device) as draw:
            draw.line([a[k], 0, a[k], 0], fill="white") # 3.4.1 Matrix LED display shows the actual indication of measurement selected
        sleep(0.5)
        # Press button for 2 seconds
        if not RPi.input(PinButtonRight): # List of measurement in Right Direction
            k = k + 1
            if k > 4:
                print("Out of Scope")
                k = 0
                with canvas(device) as draw:
                    draw.line([a[k], 0, a[k], 0], fill="white") # Matrix LED display shows the actual indication of measurement selected
                sleep(0.5)
                print("Right Button is pressed!")
            if (k >= 0) & (k <= 4):
                with canvas(device) as draw:
                    draw.line([a[k], 0, a[k], 0], fill="white") # Matrix LED display shows the actual indication of measurement selected
                sleep(0.5)
                print("Right Button is pressed!")
        # Press button for 2 seconds
        if not RPi.input(PinButtonLeft): # List of measurement in Left Direction
            k = k - 1
            if k < 0:
                print("Out of Scope")
                k = 4
                with canvas(device) as draw:
                    draw.line([a[k], 0, a[k], 0], fill="white") # Matrix LED display shows the actual indication of measurement selected
                sleep(0.5)
                print("Left Button is pressed!")
            if (k >= 0) & (k <= 4):
                with canvas(device) as draw:
                    draw.line([a[k], 0, a[k], 0], fill="white") # Matrix LED display shows the actual indication of measurement selected
                sleep(0.5)
                print("left Button is pressed!")         # Press button for 2 seconds
        if k == 0: # iteration of condition code for PM1.0
            mean_PM1 = mean_field1
            StrMeasurement = str(float(round(mean_PM1, 2)))
            for y in range(0, len(StrMeasurement)):
                segment_7SD.set_digit(y, StrMeasurement[y], decimal=False) # 3.4.2 Display mean values on the seven segment display (7SD)
                segment_7SD.set_decimal(1, 1)
            segment_7SD.write_display()
            bh = []
            for j in range(0, 8):
                adding = 0
                z = 0
                for i in range((j * 12), ((j * 12) + 12)): # 3.4.3 Division of 100 datas into 8 different periods
                    adding = adding + field_1a[i]
                    z = z + 1
                #print(z)
                #print(adding)
                bh1 = adding / z
                percentage_pm1 = int(round(6 * (bh1 / 10)))
                bh.append(percentage_pm1)
                #print(bh)
            with canvas(device) as draw:
                for i in range(0, 8):
                    draw.line([i, 8 - bh[i], i, 8 - bh[i]], fill="white") # 3.4.3 Visualizing the measurements on the Matrix LED Display (MLD)
            sleep(0.8)

        if k == 1: # iteration of condition code for PM2.5
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
                #print(z)
                #print(adding)
                bh1 = adding / z
                percentage_pm1 = int(round(6 * (bh1 / 10)))
                bh.append(percentage_pm1)
                #print(bh)
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
                #print(z)
                #print(adding)
                bh1 = adding / z
                percentage_pm1 = int(round(6 * (bh1 / 10)))
                bh.append(percentage_pm1)
                #print(bh)
            with canvas(device) as draw:
                for i in range(0, 8):
                    draw.line([i, 8 - bh[i], i, 8 - bh[i]], fill="white") # Visualizing the measurements on the Matrix LED Display (MLD)
            sleep(0.8)
        if k == 3: # iteration of condition code for temperature
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
                #print(z)
                #print(adding)
                bh1 = adding / z
                percentage_pm1 = int(round(6 * (bh1 / 100)))
                bh.append(percentage_pm1)
                #print(bh)
            with canvas(device) as draw:
                for i in range(0, 8):
                    draw.line([i, 8 - bh[i], i, 8 - bh[i]], fill="white")
            sleep(0.8)
        if k == 4: # iteration of condition code for humidity
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
                #print(z)
                #print(adding)
                bh1 = adding / z
                percentage_pm1 = int(round(6 * (bh1 / 100)))
                bh.append(percentage_pm1)
                #print(bh)
            with canvas(device) as draw:
                for i in range(0, 8):
                    draw.line([i, 8 - bh[i], i, 8 - bh[i]], fill="white")
            sleep(0.8)
