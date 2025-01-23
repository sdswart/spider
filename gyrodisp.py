from display import LCD_2inch
from PIL import Image, ImageDraw, ImageFont
from time import sleep
from mpu6050 import mpu6050


if __name__ == '__main__':
    gyro = mpu6050(0x68)
    data = gyro.get_accel_data()
    gyro_x_range = [data['x'], data['x']]
    gyro_y_range = [data['y'], data['y']]

    # Display
    disp = LCD_2inch.LCD_2inch()
    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()
    # Set the backlight to 100
    disp.bl_DutyCycle(50)

    ball_x_delta = int(disp.width * 0.05)
    ball_y_delta = int(disp.height * 0.05)
    # x = int(disp.width/2)
    # y = int(disp.height/2)

    while True:
        gx = data['x']
        if gx < gyro_x_range[0]:
            gyro_x_range[0] = gx
        elif gx > gyro_x_range[1]:
            gyro_x_range[1] = gx
        gy = data['y']
        if gy < gyro_y_range[0]:
            gyro_y_range[0] = gy
        elif gy > gyro_y_range[1]:
            gyro_y_range[1] = gy
        if gyro_x_range[0] == gyro_x_range[1] or gyro_y_range[0] == gyro_y_range[1]:
            sleep(0.1)
            continue
        x = int(((gx-gyro_x_range[0])/(gyro_x_range[1]-gyro_x_range[0]))*(disp.width))
        y = int(((gy - gyro_y_range[0]) / (gyro_y_range[1] - gyro_y_range[0])) * (disp.height))

        im = Image.new("RGB", (disp.width, disp.height), "WHITE")
        draw = ImageDraw.Draw(im)
        print(f'x={x}, y={y}, x_range={gyro_x_range}, y_range={gyro_y_range}\nvalues={gyro.values}', end='\r')

        draw.ellipse((x-ball_x_delta, y-ball_y_delta, x+ball_x_delta, y+ball_y_delta), fill=(0, 255, 0))
        disp.ShowImage(im)

        sleep(0.1)



