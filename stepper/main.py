
from machine import Pin 
import utime
import time

led = Pin(2, Pin.OUT)
led.value(True)

PUL = Pin(12, Pin.OUT)          #D6
DIR = Pin(14, Pin.OUT)          #D5
ENA = Pin(13, Pin.OUT)          #D7

ENA.value(True)

led.value(False)
utime.sleep(1)
led.value(True)
ENA.value(False)
DIR.value(True)
utime.sleep(1)

delay_us = 2500
state = False


def step(delay_us, duration):
    dt = 0
    t0 = time.time_ns()
    while dt <= duration*10**9:
        PUL.value(True)
        utime.sleep_us(delay_us)
        PUL.value(False)
        utime.sleep_us(delay_us)
        dt = time.time_ns() - t0


INTERVAL = 1

def web_page(INTERVAL, state, delay_us):
    speed = round(((1*10**6)/(delay_us*2*200)*60),2)
    if state:
        status = "Driving"
        step(delay_us, 10)
    elif not state:
        status = "Stationary"
    else:
        status = "Error"
    html = """<html>
<head>
    <meta http-equiv="refresh" content=""" + str(INTERVAL) + """>
    <title>NEMA 23 driver</title>
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
        .button { background-color: #da0a0a; border: none; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; cursor: pointer;}
        .status { color: black; text-align: center; }
    </style>
</head>
<body>
    <div class="top_nav">
        <h1>NEMA 23 driver</h1>
    </div>
    <div>
        <h3 class="status">Status""" + status + """</h3>
    </div>
    <div class="content">
        <div class="cards">
            <div class="card">
                <p><i class="fas fa-tachometer-alt fa-2x" style="color:#da0a0a;"></i><span class="symbol"> Speed</span></p><p><span class="value"><span id="speed">""" + str(speed) + """</span> RPM </span></p>
            </div>
        </div>
        <br>
        <div>
            <form>
                <label for="settings">Motor RPM:</label><br>
                <input type="text" id="settings" name="settings"><br>
                <input type="submit" value="submit"><br>
            </form>
            <p><a href="/?drive=on"><button class="button">Start</button></a></p>
            <p><a href="/?drive=off"><button class="button">Stop</button></a></p>
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
        request = conn.recv(1024)
        conn.settimeout(None)
        request = str(request)
        drive_on = request.find('/?drive=on')
        drive_off = request.find('/?drive=off')
        if drive_on == 6:
            state = True
        elif drive_off == 6:
            state = False
        else:
            state = True
        response = web_page(INTERVAL, state, delay_us)
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except OSError as e:
        conn.close()
        print('Connection closed')