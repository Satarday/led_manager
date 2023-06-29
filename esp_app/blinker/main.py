import json
import neopixel
import ure

n = neopixel.NeoPixel(data_pin, 144)


def clear():
    n.fill((0, 0, 0))
    n.write()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')


def set_color(r, g, b):
    n.fill((int(r*brightness), int(g*brightness), int(b*brightness))
    n.write()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')

def set_brightness(br):
    brightness = br
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    n.write
def send_init(br, spd, clr):
    data = [br, spd, clr]
    json_data = {'settings': data}
    json_payload = json.dumps(json_data)
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.send(json_payload)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

color = [0, 0, 0]
old_color = [0, 0, 0]
brightness = 0
speed = 0

while True:
    old_color = color
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)
    led_on = request.find('/on')
    led_off = request.find('/off')
    led_init = request.find('/init')
    # cl = request.find('/cl')
    cl_match = ure.search('/cl/([0-9]+).([0-9]+).([0-9]+)', request)
    if led_init == 6:
        send_init()
    elif led_on == 6:
        set_color(old_color[0], old_color[1], old_color[2])
    elif led_off == 6:
        clear()
    # if cl == 6:
    # color = request.split(' ')
    # color = color[1][3:]
    # color = color.split('.')
    # result = [int(item) for item in color]
    # color = result
    elif cl_match:
        color = [int(cl_match.group(1)), int(cl_match.group(2)), int(cl_match.group(3))]
    # conn.send('HTTP/1.1 200 OK\n')
    # conn.send('Content-Type: text/html\n')
    # conn.send('Connection: close\n\n')
    else:
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
    conn.close()

    if color != old_color:
        old_color = color
        set_color(old_color[0], old_color[1], old_color[2])
