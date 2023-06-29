import dearpygui.dearpygui as dpg
import requests


dpg.create_context()
counter = 0

def load_img(im_name, texture_name=None):
    texture_name = str(counter) if str(texture_name) == 'None' else texture_name
    width, height, channels, data = dpg.load_image(im_name)
    with dpg.texture_registry(show=False):
        dpg.add_static_texture(width=width,
                               height=height,
                               default_value=data,
                               tag=texture_name)
    return texture_name


def send_speed(sender):
    speed = dpg.get_value(sender)
    # print(speed)
    requests.get(f'http://192.168.0.103/spd{speed}')


def send_brightness(sender):
    brightness = dpg.get_value(sender)
    # print(brightness)
    requests.get(f'http://192.168.0.103/br{brightness}')

def send_color(sender):
    color = dpg.get_value(sender)
    color = list(map(int, color))
    # dpg.set_value('color_sel', color)
    # print(color[:-1])
    requests.get(f'http://192.168.0.103/cl{color[0]}.{color[1]}.{color[2]}')
    # print()

def send_off(sender):
    off_command = 'off'
    # print(off_command)
    requests.get(f'http://192.168.0.103/{off_command}')


def send_on(sender):
    on_command = 'on'
    # print(on_command)
    requests.get(f'http://192.168.0.103/{on_command}')

def get_values_from_esp():
    response = requests.get('http://192.168.0.103/init')
    if response.status_code == 200: data = response.json()
    dpg.set_value('brightness_slider', data[0])
    dpg.set_value('speed_slider', data[1])
    dpg.set_value('color_sel', data[2])

def save():
    save_command = 'sv'
    requests.get(f'http://192.168.0.103/{save_command}')



sun_tx_tag = load_img('C:/Users/vovap/Git_projects/led_manager/base_app\icons/lamp.png', 'sun')
lamp_off_tx_tag = load_img('C:/Users/vovap/Git_projects/led_manager/base_app/icons/lamp_off.png', 'lamp_off')
lamp_on_tx_tag = load_img('C:/Users/vovap/Git_projects/led_manager/base_app/icons/lamp_on.png', 'lamp_on')
low_speed_tx_tag = load_img('C:/Users/vovap/Git_projects/led_manager/base_app/icons/low_speed.png', 'low_speed')
hi_speed_tx_tag = load_img('C:/Users/vovap/Git_projects/led_manager/base_app/icons/hi_speed.png', 'hi_speed')

with dpg.window(tag="Primary Window", no_title_bar=True, no_resize=True):
    with dpg.group(horizontal=True, horizontal_spacing=175, indent=5):
        dpg.add_image(texture_tag=lamp_off_tx_tag,
                      width=15, height=15,
                      tint_color=(255, 255, 255, 255))
        dpg.add_image(texture_tag=lamp_on_tx_tag,
                      width=15, height=15,
                      tint_color=(255, 255, 255, 255))

    dpg.add_slider_int(default_value=1,
                       max_value=100,
                       min_value=1,
                       width=220,
                       tag='brightness_slider',
                       callback=send_brightness
                       )

    with dpg.group(horizontal=True, horizontal_spacing=175, indent=5):
        dpg.add_image(texture_tag=low_speed_tx_tag,
                      width=15, height=15,
                      tint_color=(255, 255, 255, 255))
        dpg.add_image(texture_tag=hi_speed_tx_tag,
                      width=15, height=15,
                      tint_color=(255, 255, 255, 255))

    dpg.add_slider_int(default_value=0,
                       max_value=100,
                       min_value=0,
                       width=220,
                       tag='speed_slider',
                       callback=send_speed
                       )
    dpg.add_color_picker(no_small_preview=True,
                         no_label=True,
                         no_side_preview=True,
                         width=220, no_alpha=True,
                         display_hex=False,
                         display_rgb=True,
                         callback=send_color,
                         tag='color_sel')

    with dpg.group(horizontal=True):
        dpg.add_button(tag='off_button',
                       width=106,
                       height=30,
                       label='OFF',
                       callback=send_off
                       )
        dpg.add_button(tag='on_button',
                       width=106,
                       height=30,
                       label='ON',
                       callback=send_on
                       )
    dpg.add_button(tag='sv_button',
                   width=220,
                   height=30,
                   label='SAVE',
                   callback=save)
    # dpg.add_image(texture_tag=sun_tx_tag,
    #               width=55,
    #               height=55,
    #               indent=80)

get_values_from_esp()
dpg.create_viewport(title='L/m ', resizable=False, max_width=220, max_height=430)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
