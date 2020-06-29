# This program utilises the cwiid Python library in order to get input over bluetooth from a wiimote.
# The following lines of code demonstrate many of the features realted to wiimotes, such as capturing button presses
# and rumbling the controller.
# I have managed to map the home button to the accelerometer - simply hold it and values will appear!

# Coded by The Raspberry Pi Guy. Work based on some of Matt Hawkins's!

import cwiid, time
from gpiozero import LED
from gpiozero import RGBLED
from colorzero import Color

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

gpio18 = LED(18)
gpio18.off()

rgbLed = RGBLED(16,20,21)
rgbLed.color = Color('yellow')

print 'Ready!!!'
wii.rumble = 1
time.sleep(0.2)
wii.rumble = 0
         
while True:

  buttons = wii.state['buttons']
  
  #works!
  #print((wii.state['acc'][1]-130))
  #print((wii.state['acc']))
  #print(buttons)
  #print (wii.state) 

  driverWheel = wii.state['acc'][1]-130

  if (driverWheel >= -2 and driverWheel <= 2):
    rgbLed.color = Color('yellow')
    #print 'center'
  elif (driverWheel >= 2):
    #print 'left'
    rgbLed.color = Color('red')
  elif (driverWheel <=-2):
    #print 'right'
    rgbLed.color = Color('blue')


  # Detects whether + and - are held down and if they are it quits the program
  if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
    print '\nClosing connection ...'
    # NOTE: This is how you RUMBLE the Wiimote
    wii.rumble = 1
    time.sleep(0.3)
    wii.rumble = 0
    exit(wii)

  # The following code detects whether any of the Wiimotes buttons have been pressed and then prints a statement to the screen!
  if (buttons & cwiid.BTN_LEFT):
    print 'Left pressed'
    time.sleep(button_delay)

  if(buttons & cwiid.BTN_RIGHT):
    print 'Right pressed'
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_UP):
    print 'Up pressed'
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_DOWN):
    print 'Down pressed'
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_1):
    print 'Button 1 pressed'
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_2):
    print 'Button 2 pressed'
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_A):
    #print 'Button A pressed -- move fordward'
    gpio17.on()
    gpio18.off()
    time.sleep(button_delay)
  else:
    gpio17.off()
    gpio18.off()

  if (buttons & cwiid.BTN_B):
    #print 'Button B pressed -- move backward ' 
    gpio17.off()
    gpio18.on()
    time.sleep(button_delay)
  else:
    gpio17.off()
    gpio18.off()

 
  if (buttons & cwiid.BTN_A) & (buttons  & cwiid.BTN_B):
    print 'Stop'
    gpio17.off()
    gpio18.off()

  if (buttons & cwiid.BTN_HOME):
    wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC
    check = 0
    while check == 0:
      print(wii.state['acc'])
      time.sleep(0.01)
      check = (buttons & cwiid.BTN_HOME)
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_MINUS):
    print 'Minus Button pressed'
    time.sleep(button_delay)

  if (buttons & cwiid.BTN_PLUS):
    print 'Plus Button pressed'
    time.sleep(button_delay)
