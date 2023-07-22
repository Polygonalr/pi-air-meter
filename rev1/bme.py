import bme280
import smbus2
from time import sleep

port = 1
address = 0x76
bus = smbus2.SMBus(port)
bme280.load_calibration_params(bus, address)

def sample():
    return bme280.sample(bus, address)

if __name__ == "__main__":
    while True:
        bme280_data = sample()
        print(bme280_data.humidity, bme280_data.pressure, bme280_data.temperature)
        sleep(1)
