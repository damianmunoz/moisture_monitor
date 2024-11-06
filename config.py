import network
import socket
from time import sleep

# Set up ESP8266 as an Access Point
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='DAMIAn', password='12345678')

# Create socket server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print("Access Point created with IP:", ap.ifconfig()[0])

while True:
    try:
        cl, addr = s.accept()
        print('Connection from', addr)

        cl_file = cl.makefile('rwb', 0)
        while True:
            line = cl_file.readline()
            if not line or line == b'\r\n':
                break

        cl.send('HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n')
        cl.send('OK')
        cl.close()
        sleep(2)
    except OSError as e:
        cl.close()
        print('Connection closed')

