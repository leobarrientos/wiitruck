# This program utilises the cwiid Python library in order to get input over bluetooth from a wiimote.
# WiiTruck is a script to control a old remote truck
# Code by leobarrientos at gmail dot com. Work based on some of Matt Hawkins's! and The Raspberry Pi Guy"

import cwiid
import time
from colorzero import Color
from gpiozero import LED
from gpiozero import RGBLED
from gpiozero import Servo

BUTTON_DELAY = 0.1


def servo(buttons, my_servo, value):
    """
    Controling servo with right&left command
    """
    # wii control
    if buttons & cwiid.BTN_LEFT:
        print('Left pressed')
        value2 = (float(value) - 10) / 10
        my_servo.value = value2
        time.sleep(BUTTON_DELAY)

    if buttons & cwiid.BTN_RIGHT:
        print('Left pressed')
        time.sleep(BUTTON_DELAY)

    if buttons & cwiid.BTN_UP:
        print('Up pressed')
        my_servo.value = 0

    # if buttons & cwiid.BTN_DOWN:
    #    print 'Down pressed'
    #    time.sleep(BUTTON_DELAY)
    return value


def wii_remote_conn():
    print('Please press buttons 1 + 2 on your Wiimote now ...')
    time.sleep(1)

    # This code attempts to connect to your Wiimote and if it fails the program quits
    try:
        wii = cwiid.Wiimote()
        print('Wiimote connection established!\n')
        print('Go ahead and press some buttons\n')
        print('Press PLUS and MINUS together to disconnect and quit.\n')

        # turn on led to show connected
        wii.led = 1
        return wii
    except RuntimeError:
        print("Cannot connect to your Wiimote. Run again and make sure you are holding buttons 1 + 2!")
        quit()


def permitted_bottons(buttons):
    if buttons - cwiid.BTN_A - cwiid.BTN_B != 0:
        raise Exception('You cant move fordward and backward at the same time')


def go(wii):
    # define gpios
    gpio17 = LED(17)
    gpio18 = LED(18)

    # set off to all gpios
    gpio17.off()
    gpio18.off()

    # direction led indicator definitions
    directionled = RGBLED(16, 20, 21)
    directionled.color = Color('yellow')

    # Now if we want to read values from the Wiimote we must turn on the reporting mode.
    # First let's have it just report button presses
    wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC

    # Servo Control
    my_gpio = 27

    # Min and Max pulse widths converted into milliseconds
    # To increase range of movement:
    #   increase maxPW from default of 2.0
    #   decrease minPW from default of 1.0
    # Change myCorrection using increments of 0.05 and
    # check the value works with your servo.
    my_correction = 0.45
    max_pw = (2.0 + my_correction) / 1000
    min_pw = (1.0 - my_correction) / 1000

    value = 0
    my_servo: Servo = Servo(my_gpio, min_pulse_width=min_pw, max_pulse_width=max_pw)
    my_servo.value = value

    while True:
        buttons = wii.state['buttons']
        # works!
        # print((wii.state['acc'][1]-130))
        # print((wii.state['acc']))
        # print(buttons)
        # print (wii.state)

        direction_control(wii, directionled)

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
        print('\nClosing connection ...')
        # NOTE: This is how you RUMBLE the Wiimote
        wii.rumble = 1
        time.sleep(0.3)
        wii.rumble = 0
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
    wii = wii_remote_conn()
    time.sleep(3)

    wii.rumble = 1
    time.sleep(0.2)
    wii.rumble = 0

    print('Ready to go!!!')
    go(wii)


if __name__ == "__main__":
    main()
