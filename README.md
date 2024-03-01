Device Used: Raspberry-Pi


Language: Python


Cloud: Thingspeak

1. The program reads the current cloud data and initialize all arrays at the start-up of the program.
2. The user interface (Information on 7 segment display and Trend Graph on LED's) including all local visualizations runs continuously.
3. The two cloud channels for reading data and writing data is be updated every minute.
4. The local measurements from the temperature and humidity sensor will be taken every 10 seconds.
5. The AQI calculations and transfer to the thingspeak server will be executed every minute.
