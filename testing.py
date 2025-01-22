# sudo pigpiod && python3 /app/testing.py

import RPi.GPIO as GPIO
import pigpio
from time import sleep

servo = 23

pwm = pigpio.pi()
pwm.set_mode(servo, pigpio.OUTPUT)

# Start servo
pwm.set_PWM_frequency(servo, 50)

# 500 = 0 deg,  1500 = 90 deg,  2500 = 180 deg
for i in range(6):
    pwm.set_servo_pulsewidth(servo, 500)
    sleep(0.5)
    pwm.set_servo_pulsewidth(servo, 1500)
    sleep(0.5)
    pwm.set_servo_pulsewidth(servo, 2500)
    sleep(0.5)
    pwm.set_servo_pulsewidth(servo, 1500)
    sleep(0.5)

# turning off servo
pwm.set_PWM_dutycycle(servo, 0)
pwm.set_PWM_frequency(servo, 0)
