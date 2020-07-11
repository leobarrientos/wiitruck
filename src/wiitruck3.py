# This program utilises the cwiid Python library in order to get input over bluetooth from a wiimote.
# WiiTruck is a script to control a old remote truck
# Code by leobarrientos at gmail dot com. Work based on some of Matt Hawkins's! and The Raspberry Pi Guy"

import cwiid
import time
import configparser
import os
from colorzero import Color
from gpiozero import LED
from gpiozero import RGBLED
from gpiozero import Servo

from cl.rockstar.Engine import Engine
from cl.rockstar.Emotor import Emotor
from cl.rockstar.Steering import Steering

BUTTON_DELAY = 0.1


def movement_not_permitted(buttons):
    if buttons - cwiid.BTN_A - cwiid.BTN_B == 0:
        raise Exception('You cant move fordward and backward at the same time')


def go(engine):
    wii = engine.wii
    # Now if we want to read values from the Wiimote we must turn on the reporting mode.
    # First let's have it just report button presses
    wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC
    while True:
        wii_buttons = wii.state['buttons']
        steering_control(engine)
        # Detects whether BTN_A and BTN_B are held down and if they are it turn off the motors
        try:
            movement_not_permitted(wii_buttons)
            go_fordward(wii_buttons, engine.emotor)
            go_backward(wii_buttons, engine.emotor)
        except Exception as error:
            print(error)
            engine.emotor.stop()
            wii = engine.shutdown()
            time.sleep(BUTTON_DELAY)
            exit(-1)
        truck_off(wii_buttons, engine)


def go_fordward(buttons, emotor):
    if buttons & cwiid.BTN_A:
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
        wii = engine.shutdown()
        exit(0)


def steering_control(engine):
    driver_wheel = engine.wii.state['acc'][1] - 130
    if -2 <= driver_wheel <= 2:
        engine.steering.straight()
    elif driver_wheel >= 2:
        engine.steering.turn_left()
    elif driver_wheel <= -2:
        engine.steering.turn_right()


def main():
    this_folder = os.path.dirname(os.path.abspath(__file__))
    init_file = os.path.join(this_folder, 'config.cfg')
    config = configparser.ConfigParser()
    config.read(init_file)
    
    # define gpios
    ffw = LED(config.get('GPIOS', 'pin_emotor_ffd'))
    rwd = LED(config.get('GPIOS', 'pin_emotor_rwd'))

    left = LED(config.get('GPIOS', 'pin_steering_left'))
    right = LED(config.get('GPIOS', 'pin_steering_right'))

    e_motor = Emotor(ffw, rwd)
    steering = Steering(left, right)

    engine = Engine(e_motor, steering)
    engine.start()

    print('Ready to go!!!')
    go(engine)


if __name__ == "__main__":
    main()
