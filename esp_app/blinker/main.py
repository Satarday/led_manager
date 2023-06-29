import json
import neopixel
import ure


# функция загрузки настроек из файла при подаче питания
def init():
    with open('settings.json', 'r') as fp:
        settings = json.load(fp)
    fp.close()
    return settings[0], settings[1], settings[2]


n = neopixel.NeoPixel(data_pin, 144)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
brightness, speed, color = init()
color_holder = [0,0,0]
brightness_holder = 0
speed_holder = 0

# функция для отправки данных приложению по get запросу
def send_init():
    with open ('settings.json', 'r') as fp:
        settings = json.load(fp)
    json_payload = json.dumps(settings)
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.send(json_payload)
    conn.close()
    fp.close()


# функция для сохранения данных в память, вешает прогу, надо переписать на асинхронную
def save(pr):
    with open('settings.json', 'w') as fp:
      json.dump(pr, fp)
    #   print(s)
    fp.close()
    # print('saved!')
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.close()


# функция для выключения ленты
def off():
    n.fill((0, 0, 0))
    n.write()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.close()


# функция для установки цвета
def set_color(r, g, b, br):
    color = [r, g, b]
    r = int(r*br/100)
    g = int(g*br/100)
    b = int(b*br/100)
    real_color = (r, g, b)
    n.fill((r, g, b))
    n.write()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.close()
    # print(real_color, color)
    return color


# функция для установки яркости
def set_brightness(br):
    set_color(color[0],color[1],color[2], br)
    n.write()
    new_br = br
    return new_br


while True:
    conn, addr = s.accept()
    # print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)
    led_on = ure.search('/on', request)
    led_off = ure.search('/off', request)
    led_init = ure.search('/init', request)
    led_ck = ure.search('/cl([0-9]+).([0-9]+).([0-9]+)', request)
    led_br = ure.search('/br([0-9]+)', request)
    led_sv = ure.search('/sv', request)
    if led_init: send_init()
    elif led_on: set_color(color[0], color[1], color[2], brightness)
    elif led_off: off()
    elif led_ck: color = set_color(int(led_ck.group(1)), int(led_ck.group(2)), int(led_ck.group(3)), brightness)
    elif led_br: brightness = set_brightness(int(led_br.group(1)))
    elif led_sv: save((brightness,speed,color))
    else:
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.close()
