import adafruit_ssd1306
import board
import busio
from PIL import Image, ImageDraw, ImageFont
from bme import sample
import mh_z19
from time import sleep
from oled_text import OledText, Layout32
import sqlite3
from sys import argv

TIME_PER_READING = 30 # seconds
READINGS_BEFORE_LOGGING = 4

i2c = busio.I2C(board.SCL, board.SDA)
oled = OledText(i2c, 128,32)
font = ImageFont.load_default()

def init_database():
    db_file = 'data.sqlite3'
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    sql = """CREATE TABLE IF NOT EXISTS air_logs (
        id INTEGER PRIMARY KEY,
        co2 INTEGER NOT NULL,
        temp DOUBLE NOT NULL,
        humidity DOUBLE NOT NULL,
        pressure INTEGER NOT NULL,
        created_at DATETIME DEFAULT (datetime('now', 'localtime')));"""
    c.execute(sql)
    conn.commit()
    return (conn, c)

(conn, c) = init_database()

def insert_record(conn, c, co2, temp, hum, pres):
    sql = """INSERT INTO air_logs (co2, temp, humidity, pressure) VALUES ({}, {}, {}, {});""" \
        .format(co2, temp, hum, pres)
    c.execute(sql)
    conn.commit()

def main(led_on):
    cycle = 0
    oled.auto_show = False
    oled.layout = Layout32.layout_3small()
    try:
        while True:
            oled.clear()
            try:
                bme_sample = sample()
                z19_sample = mh_z19.read()
                co2 = 0 if 'co2' not in z19_sample else z19_sample['co2']
                l1 = "CO2: {}ppm".format(co2)
                l2 = "ps: {}hPa".format(int(bme_sample.pressure))
                l3 = "T/H: {:.1f}°C {:.1f}%".format(bme_sample.temperature, bme_sample.humidity)
                print("\n".join([l1, l2, l3]))
                if led_on:
                    oled.text(l1, 1)
                    oled.text(l2, 2)
                    oled.text(l3, 3)
                    oled.show()
                if cycle == 0:
                    insert_record(conn, c, co2, bme_sample.temperature, bme_sample.humidity, int(bme_sample.pressure))
                cycle = (cycle + 1) % READINGS_BEFORE_LOGGING
                sleep(30)
            except OSError as e:
                print("Error reading from BME280!")
                sleep(30)
    finally:
        c.close()
        conn.close()

if __name__ == "__main__":
    if len(argv) > 2:
        print(f"Usage: python3 {argv[0]} [off]\nDefault is LED ON.")
        exit(0)
    if len(argv) == 2 and argv[1].lower() == "off":
        main(False)
    main(True)
