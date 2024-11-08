from machine import ADC
import network
import socket
from time import sleep

# Calibration constants
ADC_DRY = 0      # Replace with actual dry value
ADC_WET = 4095   # Replace with actual wet value (assuming 12-bit ADC)

# Set up ESP8266 as an Access Point
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='DAMIAn', password='12345678')

# Set up ADC
adc = ADC(0)

# Create socket server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print("Access Point created with IP:", ap.ifconfig()[0])

def calculate_moisture_percentage(adc_value):
    if adc_value <= ADC_DRY:
        return 0
    elif adc_value >= ADC_WET:
        return 100
    else:
        return ((adc_value - ADC_DRY) / (ADC_WET - ADC_DRY)) * 100

while True:
    try:
        cl, addr = s.accept()
        print('Connection from', addr)

        adc_value = adc.read()
        moisture_percentage = calculate_moisture_percentage(adc_value)

        cl.send('HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n')
        cl.send(str(int(moisture_percentage)))
        cl.close()
        sleep(5)
    except OSError as e:
        cl.close()
        print('Connection closed')
