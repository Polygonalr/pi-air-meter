import adafruit_ssd1306
import board
import busio
from PIL import Image, ImageDraw, ImageFont
from bme import sample
import mh_z19
from time import sleep
from oled_text import OledText, Layout32

i2c = busio.I2C(board.SCL, board.SDA)
oled = OledText(i2c, 128,32)
font = ImageFont.load_default()


def main():
    oled.auto_show = False
    oled.layout = Layout32.layout_3small()
    while True:
        oled.clear()
        bme_sample = sample()
        l1 = "CO2: {}ppm".format(mh_z19.read()['co2'])
        l2 = "ps: {}hPa".format(int(bme_sample.pressure))
        l3 = "T/H: {:.1f}°C {:.1f}%".format(bme_sample.temperature, bme_sample.humidity)
        print("\n".join([l1, l2, l3]))
        oled.text(l1, 1)
        oled.text(l2, 2)
        oled.text(l3, 3)
        oled.show()
        sleep(30)

if __name__ == "__main__":
    main()
