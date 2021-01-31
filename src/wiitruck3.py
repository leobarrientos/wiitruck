# This program utilises the cwiid Python library in order to get input over bluetooth from a wiimote.
# WiiTruck is a script to control a old remote truck
# Code by leobarrientos at gmail dot com. Work based on some of Matt Hawkins's! and The Raspberry Pi Guy"

import cwiid
import time
import configparser
import os
from gpiozero import LED, Servo, Device

from cl.rockstar.Engine import Engine
from cl.rockstar.Emotor import Emotor
from cl.rockstar.Steering import Steering
from flask import Flask
from gpiozero.pins.native import NativeFactory

BUTTON_DELAY = 0.1


def movement_not_permitted(buttons):
    if buttons - cwiid.BTN_2 - cwiid.BTN_B == 0:
        raise Exception('You cant move fordward and backward at the same time')


def go(engine):
    wii = engine.wii
    # Now if we want to read values from the Wiimote we must turn on the reporting mode.
    # First let's have it just report button presses
    wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC

    engine.steering.servo.value = 0
    value=0

    while True:
        wii_buttons = wii.state['buttons']
        # steering_control(engine)
        # Detects whether BTN_A and BTN_B are held down and if they are it turn off the motors
        try:
            movement_not_permitted(wii_buttons)
            go_fordward(wii_buttons, engine.emotor)
            go_backward(wii_buttons, engine.emotor)
            value = servo(wii_buttons, engine.steering.servo, value)
        except Exception as error:
            print(error)
            engine.emotor.stop()
            # wii = engine.shutdown()
            time.sleep(BUTTON_DELAY)
        # exit(-1)
        truck_off(wii_buttons, engine)


def go_fordward(buttons, emotor):
    if buttons & cwiid.BTN_2:
        emotor.move_fordward()
        time.sleep(BUTTON_DELAY)
    else:
        emotor.stop()


def go_backward(buttons, emotor):
    if buttons & cwiid.BTN_B:
        emotor.move_backward()
        time.sleep(BUTTON_DELAY)
    else:
        emotor.stop()


def truck_off(buttons, engine):
    # Detects whether + and - are held down and if they are it quits the program
    if buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0:
        engine.shutdown()
        exit(0)


def servo(buttons, my_servo, value):
    """
    Controlling servo with right&left command
    """

    # wii control
    if buttons & cwiid.BTN_UP:
        value = value + 1
        value2 = (float(value) - 10) / 10
        value2 = -0.25
        if -0.3 <= value2 < 0: 
            my_servo.value = value2
            print('Left pressed' + str(value2))
            time.sleep(BUTTON_DELAY)

    if buttons & cwiid.BTN_DOWN:
        value = value - 1
        value2 = (float(value) - 10) / 10
        value2 = 0.25
        if 0 < value2 <= 0.3:
            my_servo.value = value2
            print('Right pressed' + str(value2))
            time.sleep(BUTTON_DELAY)

    if buttons & cwiid.BTN_RIGHT:
        my_servo.mid()

    # if buttons & cwiid.BTN_DOWN:
    #    print 'Down pressed'
    #    time.sleep(BUTTON_DELAY)
    return value


def steering_control(engine):
    driver_wheel = engine.wii.state['acc'][1] - 130
    if -2 <= driver_wheel <= 2:
        engine.steering.straight()
    elif driver_wheel >= 2:
        engine.steering.turn_left(driver_wheel)
    elif driver_wheel <= -2:
        engine.steering.turn_right(driver_wheel)


app = Flask(__name__)


@app.route('/on')
def on():

    this_folder = os.path.dirname(os.path.abspath(__file__))
    init_file = os.path.join(this_folder, 'config.cfg')
    config = configparser.ConfigParser()
    config.read(init_file)

    # define gpios
    ffw = LED(config.get('GPIOS', 'pin_emotor_ffd'))
    rwd = LED(config.get('GPIOS', 'pin_emotor_rwd'))

    servo = Servo(config.get('GPIOS', 'pin_steering_servo'), min_pulse_width=5/10000, max_pulse_width=25/10000)

    # blink front lights
    lights = LED(config.get('GPIOS', 'pin_lights'))

    e_motor = Emotor(ffw, rwd)
    steering = Steering(servo)

    engine = Engine(e_motor, steering, lights)
    engine.start()

    print('Ready to go!!!')
    go(engine)
    return "OK"


@app.route('/')
def hello_world():
    return 'Hello World! - WiiTruck!!! --> go to http://192.168.100.36//on !!'


if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=80)
    on()
