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
    print(speed)


def send_brightness(sender):
    brightness = dpg.get_value(sender)
    print(brightness)


def send_color(sender):
    color = dpg.get_value(sender)
    color = list(map(int, color))
    # dpg.set_value('color_sel', color)
    print(color[:-1])
    requests.get(f'http://192.168.0.100/cl{color[0]}.{color[1]}.{color[2]}')


def send_off(sender):
    off_command = 'off'
    print(off_command)
    requests.get(f'http://192.168.0.100/{off_command}')


def send_on(sender):
    on_command = 'on'
    print(on_command)
    requests.get(f'http://192.168.0.100/{on_command}')

def get_values_from_esp():
    brightness = 0
    speed = 0
    color = [0, 0, 0]
    state = 0
    dpg.set_value('brightness_slider', brightness)
    dpg.set_value('speed_slider', speed)
    dpg.set_value('color_sel', color)



sun_tx_tag = load_img('lamp.png', 'sun')
# lamp_off_tx_tag = load_img('lamp_off.png', 'lamp_off')
# lamp_on_tx_tag = load_img('lamp_on.png', 'lamp_on')
# speed_tx_tag = load_img('fast_forward.png', 'speed')
# low_speed_tx_tag = load_img('low_speed.png', 'low_speed')
# hi_speed_tx_tag = load_img('hi_speed.png', 'hi_speed')

with dpg.window(tag="Primary Window", no_title_bar=True, no_resize=True):
    with dpg.group(horizontal=True, horizontal_spacing=175, indent=5):
        dpg.add_image(texture_tag=sun_tx_tag,
                      width=15, height=15,
                      tint_color=(255, 255, 255, 255))
        dpg.add_image(texture_tag=sun_tx_tag,
                      width=15, height=15,
                      tint_color=(255, 255, 255, 255))

    dpg.add_slider_int(default_value=0,
                       max_value=255,
                       min_value=0,
                       width=215,
                       tag='brightness_slider',
                       callback=send_brightness
                       )

    with dpg.group(horizontal=True, horizontal_spacing=175, indent=5):
        dpg.add_image(texture_tag=sun_tx_tag,
                      width=15, height=15,
                      tint_color=(255, 255, 255, 255))
        dpg.add_image(texture_tag=sun_tx_tag,
                      width=15, height=15,
                      tint_color=(255, 255, 255, 255))

    dpg.add_slider_int(default_value=0,
                       max_value=100,
                       min_value=0,
                       width=215,
                       tag='speed_slider',
                       callback=send_speed
                       )
    dpg.add_color_picker(no_small_preview=True,
                         no_label=True,
                         no_side_preview=True,
                         width=215, no_alpha=True,
                         display_hex=False,
                         display_rgb=True,
                         callback=send_color,
                         tag='color_sel')

    with dpg.group(horizontal=True):
        dpg.add_button(tag='off_button',
                       width=105,
                       height=30,
                       label='OFF',
                       callback=send_off
                       )
        dpg.add_button(tag='on_button',
                       width=105,
                       height=30,
                       label='ON',
                       callback=send_on
                       )

    dpg.add_image(texture_tag='sun',
                  width=55,
                  height=55,
                  indent=80)

dpg.create_viewport(title='L/m ', resizable=False, max_width=250, max_height=500)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()