import network
import socket
import random
from time import sleep

# Set up the ESP8266 as an Access Point
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='PlantMoisture_AP', password='12345678')

# Create a socket server to handle incoming requests
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print("Access Point created with IP:", ap.ifconfig()[0])

while True:
    try:
        # Wait for a connection from the Django server
        cl, addr = s.accept()
        print('Connection from', addr)
        
        # Simulate a random moisture value (0-100%)
        moisture_percentage = random.uniform(0, 100)
        
        # Send the simulated moisture value as a response
        response = f"{moisture_percentage:.1f}"
        
        # Read the request data (not needed here, but it's typical to read the incoming request)
        cl_file = cl.makefile('rwb', 0)
        while True:
            line = cl_file.readline()
            if not line or line == b'\r\n':
                break
        
        # Send HTTP response header
        cl.send('HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n')
        # Send the simulated moisture value as the response body
        cl.send(response)
        cl.close()
    except OSError as e:
        cl.close()
        print('Connection closed')
