# This program utilises the cwiid Python library in order to get input over bluetooth from a wiimote.
# WiiTruck is a script to control a old remote truck
# Code by leobarrientos at gmail dot com. Work based on some of Matt Hawkins's! and The Raspberry Pi Guy"

import cwiid
import time
from colorzero import Color
from gpiozero import LED
from gpiozero import RGBLED


def wii_remote_conn():
    print 'Please press buttons 1 + 2 on your Wiimote now ...'
    time.sleep(1)

    # This code attempts to connect to your Wiimote and if it fails the program quits
    try:
        wii = cwiid.Wiimote()
        print 'Wiimote connection established!\n'
        print 'Go ahead and press some buttons\n'
        print 'Press PLUS and MINUS together to disconnect and quit.\n'

        # turn on led to show connected
        wii.led = 1
        return wii
    except RuntimeError:
        print "Cannot connect to your Wiimote. Run again and make sure you are holding buttons 1 + 2!"
        quit()


def go(wii):
    button_delay = 0.1

    # define gpios
    gpio17 = LED(17)
    gpio18 = LED(18)

    # set off to all gpios
    gpio17.off()
    gpio18.off()

    # Now if we want to read values from the Wiimote we must turn on the reporting mode.
    # First let's have it just report button presses
    wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC

    while True:
        buttons = wii.state['buttons']
        # works!
        # print((wii.state['acc'][1]-130))
        # print((wii.state['acc']))
        # print(buttons)
        # print (wii.state)

        direction_control(wii)

        # Detects whether BTN_A and BTN_B are held down and if they are it turn off the motors
        if buttons - cwiid.BTN_A - cwiid.BTN_B == 0:
            print '\nNot permited ... and Stop!'
            gpio17.off()
            gpio18.off()
            time.sleep(button_delay)
        else:
            if (buttons & cwiid.BTN_A):
                # print 'Button A pressed -- move fordward'
                gpio17.on()
                gpio18.off()
                time.sleep(button_delay)
            else:
                gpio17.off()
                gpio18.off()

            if (buttons & cwiid.BTN_B):
                # print 'Button B pressed -- move backward '
                gpio17.off()
                gpio18.on()
                time.sleep(button_delay)
            else:
                gpio17.off()
                gpio18.off()

        # Detects whether + and - are held down and if they are it quits the program
        if buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0:
            print '\nClosing connection ...'
            # NOTE: This is how you RUMBLE the Wiimote
            wii.rumble = 1
            time.sleep(0.3)
            wii.rumble = 0
            exit(wii)


def direction_control(wii):
    # direction led indicator definitions
    directionled = RGBLED(16, 20, 21)
    directionled.color = Color('yellow')

    driver_wheel = wii.state['acc'][1] - 130
    if -2 <= driver_wheel <= 2:
        directionled.color = Color('yellow')
        # print 'center'
    elif driver_wheel >= 2:
        # print 'left'
        directionled.color = Color('red')
    elif driver_wheel <= -2:
        # print 'right'
        directionled.color = Color('blue')


def main():
    wii = wii_remote_conn()
    time.sleep(3)

    wii.rumble = 1
    time.sleep(0.2)
    wii.rumble = 0

    print 'Ready to go!!!'
    go(wii)


if __name__ == "__main__":
    main()
