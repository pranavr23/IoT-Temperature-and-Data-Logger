

import json
from statistics import mean
import matplotlib.pyplot as plt
import requests


#----------- Accessing the thinkspeak Channel--------------

field_data = requests.get('https://thingspeak.com/channels/628559/feed.json')  # Resquest an HTTP library

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
a=0
while a<=99:
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
    a+=1


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
field_1a = list(map(float,field_1))
mean_field1 = mean(field_1a)
print('Mean value of field1 is', mean_field1)
field_2a = list(map(float,field_2))
mean_field2 = mean(field_2a)
print('Mean value of field2 is', mean_field2)
field_3a = list(map(float,field_3))
mean_field3 = mean(field_3a)
print('Mean value of field3 is', mean_field3)

#............Visualizing PM measurements and mean values...............
plt.subplot(3, 1, 1)
plt.plot(range(100), field_1a, 'rd-')
plt.axhline(y=mean_field1, color='r', linestyle='--')
plt.xlabel('sample')
plt.ylabel('ATM')
plt.title('PM 1.0')

plt.subplot(3, 1, 2)
plt.plot(range(100), field_2a, 'ko-')
plt.axhline(y=mean_field2, color='black', linestyle='--')
plt.xlabel('sample')
plt.ylabel('ATM')
plt.title('PM 2.5')

plt.subplot(3, 1, 3)
plt.plot(range(100), field_3a, 'bo-')
plt.axhline(y=mean_field3, color='b', linestyle='--')
plt.xlabel('sample')
plt.ylabel('ATM')
plt.title('PM 10')
plt.show()
plt.close()
