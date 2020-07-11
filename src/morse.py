import cwiid, time
import RPi.GPIO as GPIO

button_delay = 0.1

print 'Please press buttons 1 + 2 on your Wiimote now ...'
time.sleep(1)

# This code attempts to connect to your Wiimote and if it fails the program quits
try:
    wii=cwiid.Wiimote()

    #turn on led to show connected
    wii.led = 1
except RuntimeError:
    print "Cannot connect to your Wiimote. Run again and make sure you are holding buttons 1 + 2!"
    quit()

print 'Wiimote connection established!\n'
print 'Go ahead and press some buttons\n'
print 'Press PLUS and MINUS together to disconnect and quit.\n'

time.sleep(3)

#Now if we want to read values from the Wiimote we must turn on the reporting mode. First let's have it just report button presses
wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC

gpio17 = LED(17)
gpio17.off()

print 'Ready!!!'

CODE = {' ': ' ',
        "'": '.----.',
        '(': '-.--.-',
        ')': '-.--.-',
        ',': '--..--',
        '-': '-....-',
        '.': '.-.-.-',
        '/': '-..-.',
        '0': '-----',
        '1': '.----',
        '2': '..---',
        '3': '...--',
        '4': '....-',
        '5': '.....',
        '6': '-....',
        '7': '--...',
        '8': '---..',
        '9': '----.',
        ':': '---...',
        ';': '-.-.-.',
        '?': '..--..',
        'A': '.-',
        'B': '-...',
        'C': '-.-.',
        'D': '-..',
        'E': '.',
        'F': '..-.',
        'G': '--.',
        'H': '....',
        'I': '..',
        'J': '.---',
        'K': '-.-',
        'L': '.-..',
        'M': '--',
        'N': '-.',
        'O': '---',
        'P': '.--.',
        'Q': '--.-',
        'R': '.-.',
        'S': '...',
        'T': '-',
        'U': '..-',
        'V': '...-',
        'W': '.--',
        'X': '-..-',
        'Y': '-.--',
        'Z': '--..',
        '_': '..--.-'}
ledPin=17
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin,GPIO.ALT0)
GPIO.setclock(4,64000)


def dot():
    GPIO.output(ledPin,1)
    time.sleep(0.2)
    GPIO.output(ledPin,0)
    time.sleep(0.2)

def dash():
    GPIO.output(ledPin,1)
    time.sleep(0.5)
    GPIO.output(ledPin,0)
    time.sleep(0.2)

while True:
    input = raw_input('What would you like to send? ')
    for letter in input:
        for symbol in CODE[letter.upper()]:
            if symbol == '-':
                dash()
            elif symbol == '.':
                dot()
            else:
                time.sleep(0.5)
        time.sleep(0.5)