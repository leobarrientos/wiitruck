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

BUTTON_DELAY = 0.1


def servo(buttons, my_servo, value):
    """
    Controlling servo with right&left command
    """

    # wii control
    if buttons & cwiid.BTN_LEFT:
        print('Left pressed')
        value = value + 1
        value2 = (float(value) - 10) / 10
        my_servo.value = value2
        time.sleep(BUTTON_DELAY)

    if buttons & cwiid.BTN_RIGHT:
        print('Right pressed')
        value = value - 1
        value2 = (float(value) - 10) / 10
        my_servo.value = value2
        time.sleep(BUTTON_DELAY)

    if buttons & cwiid.BTN_UP:
        print('Up pressed... servo centered')
        my_servo.mid()

    # if buttons & cwiid.BTN_DOWN:
    #    print 'Down pressed'
    #    time.sleep(BUTTON_DELAY)
    return value


def permitted_bottons(buttons):
    if buttons - cwiid.BTN_A - cwiid.BTN_B == 0:
        raise Exception('You cant move fordward and backward at the same time')


def go(engine):
    # define gpios
    gpio17 = LED(17)
    gpio18 = LED(18)

    # set off to all gpios
    gpio17.off()
    gpio18.off()

    # direction led indicator definitions
    direction_led = RGBLED(16, 20, 21)
    direction_led.color = Color('yellow')

    wii = engine.wii
    # Now if we want to read values from the Wiimote we must turn on the reporting mode.
    # First let's have it just report button presses
    wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC

    # Servo Control
    servo_gpio = 27

    # Min and Max pulse widths converted into milliseconds
    # To increase range of movement:
    #   increase maxPW from default of 2.0
    #   decrease minPW from default of 1.0
    # Change myCorrection using increments of 0.05 and
    # check the value works with your servo.
    servo_correction = 0.45
    servo_max_pw = (2.0 + servo_correction) / 1000
    servo_min_pw = (1.0 - servo_correction) / 1000

    value = 0
    my_servo = Servo(servo_gpio, min_pulse_width=servo_min_pw, max_pulse_width=servo_max_pw)
    my_servo.value = value

    while True:
        buttons = wii.state['buttons']
        # works!
        # print((wii.state['acc'][1]-130))
        # print((wii.state['acc']))
        # print(buttons)
        # print (wii.state)

        direction_control(wii, direction_led)

        # Detects whether BTN_A and BTN_B are held down and if they are it turn off the motors
        try:
            permitted_bottons(buttons)
            detect_fordward_movement(buttons, gpio17, gpio18)
            detect_backward_movement(buttons, gpio17, gpio18)
            value = servo(buttons, my_servo, value)
        except Exception as error:
            print(error)
            gpio17.off()
            gpio18.off()
            time.sleep(BUTTON_DELAY)

        truck_off(buttons, wii)


def detect_fordward_movement(buttons, gpio17, gpio18):
    if buttons & cwiid.BTN_A:
        # print 'Button A pressed -- move fordward'
        gpio17.on()
        gpio18.off()
        time.sleep(BUTTON_DELAY)
    else:
        gpio17.off()
        gpio18.off()


def detect_backward_movement(buttons, gpio17, gpio18):
    if buttons & cwiid.BTN_B:
        # print 'Button B pressed -- move backward '
        gpio17.off()
        gpio18.on()
        time.sleep(BUTTON_DELAY)
    else:
        gpio17.off()
        gpio18.off()


def truck_off(buttons, wii):
    # Detects whether + and - are held down and if they are it quits the program
    if buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0:


        exit(wii)


def direction_control(wii, direction_led):
    driver_wheel = wii.state['acc'][1] - 130
    if -2 <= driver_wheel <= 2:
        direction_led.color = Color('yellow')
        # print 'center'
    elif driver_wheel >= 2:
        # print 'left'
        direction_led.color = Color('red')
    elif driver_wheel <= -2:
        # print 'right'
        direction_led.color = Color('blue')


def main():

    this_folder = os.path.dirname(os.path.abspath(__file__))
    init_file = os.path.join(this_folder, 'config.cfg')
    # print this_folder

    config = configparser.ConfigParser()
    config.read(init_file)
    print(config.get('GPIOS', 'pin_1_motor'))

    engine = Engine(None, None)
    wii = engine.start()

    print('Ready to go!!!')
    go(engine)


if __name__ == "__main__":
    main()
