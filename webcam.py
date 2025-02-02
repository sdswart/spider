import cv2
from display import LCD_2inch
from PIL import Image, ImageDraw, ImageFont


if __name__ == '__main__':
    disp = LCD_2inch.LCD_2inch()
    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()
    #Set the backlight to 100
    disp.bl_DutyCycle(50)


    vc = cv2.VideoCapture(0)

    if vc.isOpened():  # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False

    while rval:
        rval, frame = vc.read()
        im = Image.fromarray(frame)
        im = im.resize((disp.height, disp.width), resample=Image.LANCZOS)
        disp.ShowImage(im)
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break

    vc.release()
    disp.module_exit()
