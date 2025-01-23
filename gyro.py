import smbus  # import SMBus module of I2C
from time import sleep  # import

# some MPU6050 Registers and their Address
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_ENABLE = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47


class Gyro:
    def __init__(self):
        self.bus = smbus.SMBus(1)  # or bus = smbus.SMBus(0) for older version boards
        self.device_address = 0x68  # MPU6050 device address
        self.mpu_init()
    
    def mpu_init(self):
        # write to sample rate register
        self.bus.write_byte_data(self.device_address, SMPLRT_DIV, 7)

        # Write to power management register
        self.bus.write_byte_data(self.device_address, PWR_MGMT_1, 1)

        # Write to Configuration register
        self.bus.write_byte_data(self.device_address, CONFIG, 0)

        # Write to Gyro configuration register
        self.bus.write_byte_data(self.device_address, GYRO_CONFIG, 24)

        # Write to interrupt enable register
        self.bus.write_byte_data(self.device_address, INT_ENABLE, 1)
        
    def read_raw_data(self, addr):
        # Accelero and Gyro value are 16-bit
        high = self.bus.read_byte_data(self.device_address, addr)
        low = self.bus.read_byte_data(self.device_address, addr + 1)
    
        # concatenate higher and lower value
        value = ((high << 8) | low)
    
        # to get signed value from mpu6050
        if (value > 32768):
            value = value - 65536
        return value

    @property
    def acc_x(self):
        return self.read_raw_data(ACCEL_XOUT_H) / 16384.0

    @property
    def acc_y(self):
        return self.read_raw_data(ACCEL_YOUT_H) / 16384.0

    @property
    def acc_z(self):
        return self.read_raw_data(ACCEL_ZOUT_H) / 16384.0

    @property
    def x(self):
        return self.read_raw_data(GYRO_XOUT_H) / 131.0

    @property
    def y(self):
        return self.read_raw_data(GYRO_YOUT_H) / 131.0

    @property
    def z(self):
        return self.read_raw_data(GYRO_ZOUT_H) / 131.0

    @property
    def values(self):
        return {
            'acc_x': self.acc_x,
            'acc_y': self.acc_y,
            'acc_z': self.acc_z,
            'x': self.x,
            'y': self.y,
            'z': self.z,
        }
