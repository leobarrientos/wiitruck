#!/usr/bin/python
#--------------------------------------
#    ___  ___  _ ____
#   / _ \/ _ \(_) __/__  __ __
#  / , _/ ___/ /\ \/ _ \/ // /
# /_/|_/_/  /_/___/ .__/\_, /
#                /_/   /___/
#
#           servo3.py
# Example script to control a servo
# connected to GPIO17 using the Gpiozero library.
# Allows tweaking of pulse widths to get the full
# range of movement.
# Uses "value" to move between min and max rotation.
#
# Use CTRL-C to break out of While loop.
#
# Author : Matt Hawkins
# Date   : 20/01/2018
#
# https://www.raspberrypi-spy.co.uk/tag/servo/
#
#--------------------------------------
from gpiozero import Servo
from time import sleep

myGPIO=19

# Min and Max pulse widths converted into milliseconds
# To increase range of movement:
#   increase maxPW from default of 2.0
#   decrease minPW from default of 1.0
# Change myCorrection using increments of 0.05 and
# check the value works with your servo.
myCorrection=0.45
maxPW=(2.0+myCorrection)/1000
minPW=(1.0-myCorrection)/1000

myServo = Servo(myGPIO,min_pulse_width=minPW,max_pulse_width=maxPW)

print("Using GPIO27")
print("Max pulse width is set to 2.45 ms")
print("Min pulse width is set to 0.55 ms")

while True:

  print("Set value range -1.0 to +1.0")
  for value in range(0,21):
    value2=(float(value)-10)/10
    myServo.value=value2
    print("Servo value set to "+str(value2))
    sleep(1)

  print("Set value range +1.0 to -1.0")
  for value in range(20,-1,-1):
    value2=(float(value)-10)/10
    myServo.value=value2
    print("Servo value set to "+str(value2))
    sleep(1)
