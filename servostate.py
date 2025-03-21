import pigpio
from time import sleep
import numpy as np

# Servo Broadcom numbers: https://pinout.xyz/
servos = {
    'fl0': 19,
    'fl1': 26,
    'fl2': 20,

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


class SpiderServo:
    def __init__(self, name):
        self.name = name
        self.pin = servos[name]
        self.front = name.startswith('f')
        self.right = name[1] == 'r'
        self.segment = int(name[2])
        self.angle = None
        pwm.set_mode(self.pin, pigpio.OUTPUT)
        # Start servo
        pwm.set_PWM_frequency(self.pin, 50)

    @property
    def pulsewidth(self):
        if self.angle is not None:
            return np.clip(2500-((180-self.angle)/180)*(2000))

    def set_angle(self, angle):
        if self.right:  # reverse angle
            angle = 180 - angle
        self.angle = angle
        # angle_to_pulse_width
        pw = 2500-((180-angle)/180)*(2000)
        pwm.set_servo_pulsewidth(self.pin, pw)

    def __del__(self):
        pwm.set_PWM_dutycycle(self.pin, 0)
        pwm.set_PWM_frequency(self.pin, 0)


spider_servos = {name: SpiderServo(name) for name in servos}

def stand():
    for servo in spider_servos.values():
        servo.set_angle(90)
    sleep(1)
    for servo in spider_servos.values():
        if servo.segment == 2:
            servo.set_angle(10)

states = {
    'stand': stand
}

while (state := input('Enter a name: ').strip()) not in ['exit', '']:
    if state not in states.keys():
        continue
    fcn = states[state]
    fcn()

for servo in spider_servos.values():
    servo.__del__()

