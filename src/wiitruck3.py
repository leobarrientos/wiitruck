# This program utilises the cwiid Python library in order to get input over bluetooth from a wiimote.
# The following lines of code demonstrate many of the features realted to wiimotes, such as capturing button presses
# and rumbling the controller.
# I have managed to map the home button to the accelerometer - simply hold it and values will appear!

# Coded by The Raspberry Pi Guy. Work based on some of Matt Hawkins's!

import cwiid, time
from gpiozero import LED


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


def go(wii, gpio17, button_delay):
    # Now if we want to read values from the Wiimote we must turn on the reporting mode. First let's have it just report button presses
    wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC

    while True:
        buttons = wii.state['buttons']

        # works!
        # print((wii.state['acc'][1]-130))
        # print((wii.state['acc']))
        # print(buttons)

        driver_wheel = wii.state['acc'][1] - 130

        if -2 <= driver_wheel <= 2:
            print 'center'
        elif driver_wheel >= 2:
            print 'left'
        elif driver_wheel <= -2:
            print 'right'

        if buttons & cwiid.BTN_A:
            print 'Button A pressed -- move fordward'
            gpio17.on()
            time.sleep(button_delay)
        else:
            gpio17.off()

        if buttons & cwiid.BTN_B:
            gpio17.off()
            print 'Button B pressed -- Stop '
            time.sleep(button_delay)

        # Detects whether + and - are held down and if they are it quits the program
        if buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0:
            print '\nClosing connection ...'
            # NOTE: This is how you RUMBLE the Wiimote
            wii.rumble = 1
            time.sleep(0.3)
            wii.rumble = 0
            exit(wii)


def main():
    wii = wii_remote_conn()
    time.sleep(3)

    gpio17 = LED(17)
    button_delay = 0.1
    gpio17.off()

    wii.rumble = 1
    time.sleep(0.2)
    wii.rumble = 0

    print 'Ready to go!!!'
    go(wii, gpio17, button_delay)


if __name__ == "__main__":
    main()
