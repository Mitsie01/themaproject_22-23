from machine import Pin, I2C
import utime
from bme680 import *



led = Pin(2, Pin.OUT)
led.value(True)

trigger = Pin(12, Pin.OUT)
echo = Pin(14, Pin.IN)

try:
    with open("weatherdata.csv","r") as file:
        file.close()
except:
    with open('weatherdata.csv', 'w') as file:
        file.write('Temperature, Humidity, Pressure')
        file.write('\n')
        file.close()

INTERVAL = 60
c = 343


#measure data
def pulse(c):
    trigger.value(False)
    utime.sleep_us(2)
    trigger.value(True)
    utime.sleep_us(5)
    trigger.value(False)
    while echo.value() == False:
        t_send = utime.ticks_us()
    while echo.value() == True:
        t_receive = utime.ticks_us()
    dt = t_receive - t_send
    if dt > 0 and dt < 17000:
        distance = (dt * (c/10000)) / 2
        #print(distance,"cm")
    else:
        print("Object out of range")

    return distance


def web_page(INTERVAL):
    distance = pulse(c)
    html = """<html>
<head>
    <meta http-equiv="refresh" content=""" + str(INTERVAL) + """>
    <title>Ultrasonic sensor</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    <link rel="icon" href="data:,">
    <style>
        html {font-family: Arial; display: inline-block; text-align: center;}
        p { font-size: 1.2rem;}
        body {  margin: 0;}
        .top_nav { overflow: hidden; background-color: #da0a0a; color: white; font-size: 1rem; }
        .content { padding: 30px; }
        .card { background-color: white; box-shadow: 2px 2px 12px 1px rgba(140,140,140,.5); }
        .cards { max-width: 1000px; margin: 0 auto; display: grid; grid-gap: 2rem; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); }
        .value { font-size: 3rem; }
        .symbol { font-size: 2rem; }
    </style>
</head>
<body>
    <div class="top_nav">
        <h1>Ultrasonic distance sensor</h1>
    </div>
    <div class="content">
        <div class="cards">
            <div class="card">
                <p><i class="fas fa-ruler fa-2x" style="color:#da0a0a;"></i><span class="symbol"> Distance</span></p><p><span class="value"><span id="temp">""" + str(distance) + """</span> cm</span></p>
            </div>
        </div>
    </div>
</body>
</html>"""
    return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)


while True:
    #print functions commented out to prevent webpage from freezing due to ram filling
    try:
        if gc.mem_free() < 102000:
            gc.collect()
        conn, addr = s.accept()
        conn.settimeout(3.0)
        #print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        conn.settimeout(None)
        request = str(request)
        #print('Content = %s' % request)
        response = web_page(INTERVAL)
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except OSError as e:
        conn.close()
        #print('Connection closed')