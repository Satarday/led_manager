
import neopixel
n = neopixel.NeoPixel(data_pin, 144)
def clear():
  n.fill( (0, 0, 0) )
  n.write()
def set_color (r,g,b):
  n.fill( (r, g, b) )
  n.write()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

color = [0,0,0] 
old_color = [0,0,0]


while True:
  old_color = color
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  request = str(request)
  led_on = request.find('/on')
  led_off = request.find('/off')
  cl = request.find('/cl')
  if led_on == 6:
    set_color(old_color[0],old_color[1],old_color[2])
  if led_off == 6:
    clear()
  if cl == 6:
    color = request.split(' ')
    color = color[1][3:]
    color = color.split('.')
    result = [int(item) for item in color]
    color = result
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.close()

  if color != old_color :
    old_color = color
    set_color(old_color[0],old_color[1],old_color[2])