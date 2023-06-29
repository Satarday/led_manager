import json
import neopixel
import ure
import time

# функция загрузки настроек из файла при подаче питания
def init():
    with open('settings.json', 'r') as fp:
        settings = json.load(fp)
    fp.close()
    return settings[0], settings[1], settings[2]


# функция для отправки данных приложению по get запросу
def send_init():
    with open ('settings.json', 'r') as fp:
        settings = json.load(fp)
    json_payload = json.dumps(settings)
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.send(json_payload)
    fp.close()


# функция для сохранения данных в память, вешает прогу, надо переписать на асинхронную
def save(pr):
    time.sleep(10)
    with open('settings.json', 'w') as fp:
      json.dump(pr, fp)
    fp.close()
    flag = False
    print('saved!')


# функция для выключения ленты
def off():
    n.fill((0, 0, 0))
    n.write()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')


# функция для установки цвета
def set_color(r, g, b):
    color = [r, g, b]
    n.fill(int(r*brightness), int(g*brightness), int(b*brightness))
    n.write()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    return color


# функция для установки яркости
def set_brightness(br):
    brightness = br
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    n.write


n = neopixel.NeoPixel(data_pin, 144)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
brightness, speed, color = init()
color_holder = [0,0,0]
brightness_holder = 0
speed_holder = 0

# color = [0, 0, 0]
# old_color = [0, 0, 0]
# brightness = 0
# speed = 0
# рабочий цикл
while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)
    led_on = ure.search('/on', request)
    led_off = ure.search('/off', request)
    led_init = ure.search('/init', request)
    led_ck = ure.search('/cl([0-9]+).([0-9]+).([0-9]+)', request)
    # cl = request.find('/cl')
    # led_on = request.find('/on')
    # led_off = request.find('/off')
    # led_init = request.find('/init')
    # if led_init == 6: send_init()
    # elif led_on == 6: set_color(color[0], color[1], color[2])
    # elif led_off == 6: off()
    # if cl == 6:
    # color = request.split(' ')
    # color = color[1][3:]
    # color = color.split('.')
    # result = [int(item) for item in color]
    # color = result
    if led_init: send_init()
    elif led_on: set_color(color[0], color[1], color[2])
    elif led_off: off()
    elif led_ck: color = set_color(int(led_ck.group(1)), int(led_ck.group(2)), int(led_ck.group(3)))
    else:
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
    conn.close()

    # if color != old_color:
    #     old_color = color
    #     set_color(old_color[0], old_color[1], old_color[2])
