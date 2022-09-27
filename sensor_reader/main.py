from machine import Pin, I2C
import utime


led = Pin(2, Pin.OUT)
led.value(True)

trigger = Pin(12, Pin.OUT)
echo = Pin(14, Pin.IN)

INTERVAL = 1
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
    else:
        distance = 'Out of range'

    return distance


def web_page(INTERVAL, state):
    if state:
        try:
            distance = int(pulse(c))
            unit = ' cm'
        except:
            distance = pulse(c)
            unit = ''
    elif not state:
        distance = 'Sensor off'
        unit = ''
    else:
        distance = 'Sensor failure'
        unit = ''
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
        .button { background-color: #da0a0a; border: none; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; cursor: pointer;}
    </style>
</head>
<body>
    <div class="top_nav">
        <h1>Ultrasonic distance sensor</h1>
    </div>
    <div class="content">
        <div class="cards">
            <div class="card">
                <p><i class="fas fa-ruler fa-2x" style="color:#da0a0a;"></i><span class="symbol"> Distance</span></p><p><span class="value"><span id="temp">""" + str(distance) + """</span>""" + unit + """</span></p>
            </div>
        </div>
        <br>
        <div>
            <p><a href="/?pulse=on"><button class="button">Sensor on</button></a></p>
            <p><a href="/?pulse=off"><button class="button">Sensor off</button></a></p>
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
        sensor_on = request.find('/?pulse=on')
        sensor_off = request.find('/?pulse=off')
        if sensor_on == 6:
            state = True
        elif sensor_off == 6:
            state = False
        else:
            state = True
        response = web_page(INTERVAL, state)
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except OSError as e:
        conn.close()
        print('Connection closed')