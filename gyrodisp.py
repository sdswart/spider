from display import LCD_2inch
from PIL import Image, ImageDraw, ImageFont
from time import sleep
from gyro import Gyro


if __name__ == '__main__':
    gyro = Gyro()
    gyro_x_range = (gyro.x, gyro.x)
    gyro_y_range = (gyro.y, gyro.y)

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
        gx = gyro.x
        if gx < gyro_x_range[0]:
            gyro_x_range[0] = gx
        elif gx > gyro_x_range[1]:
            gyro_x_range[1] = gx
        gy = gyro.y
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
        draw.ellipse((x-ball_x_delta, y-ball_y_delta, x+ball_x_delta, y+ball_y_delta), fill=(0, 255, 0))
        disp.ShowImage(im)

        sleep(0.1)



