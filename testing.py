#
# Installation
# Install the pigpio daemon.
# Code
#
#     sudo apt update
#     sudo apt install pigpio
#
# Start the daemon.
# Code
#
#     sudo systemctl start pigpiod
#
# To ensure it runs on boot, enable it:
# Code
#
#     sudo systemctl enable pigpiod
#
# Install the Python library.
# Code
#
#     pip3 install pigpio

import pigpio
from time import sleep

# Servo Broadcom numbers: https://pinout.xyz/
servos = {
    'fl0': 16,
    'fl1': 26,
    'fl2': 19,

    'fr0': 13,
    'fr1': 12,
    'fr2': 6,

    'rl0': 23,
    'rl1': 24,
    'rl2': 5,

    'rr0': 22,
    'rr1': 17,
    'rr2': 4,
}

pwm = pigpio.pi()

for pin in servos.values():
    pwm.set_mode(pin, pigpio.OUTPUT)
    # Start servo
    pwm.set_PWM_frequency(pin, 50)


while (name := input('Enter a name: ').strip()) not in ['exit', '']:
    if name not in servos.keys():
        continue
    pin = servos[name]

    # 500 = 0 deg,  1500 = 90 deg,  2500 = 180 deg
    pwm.set_servo_pulsewidth(pin, 500)
    sleep(1)
    pwm.set_servo_pulsewidth(pin, 1500)
    sleep(1)
    pwm.set_servo_pulsewidth(pin, 2500)
    sleep(1)
    pwm.set_servo_pulsewidth(pin, 1500)
    sleep(1)

for pin in servos.values():
    # turning off servo
    pwm.set_PWM_dutycycle(pin, 0)
    pwm.set_PWM_frequency(pin, 0)
