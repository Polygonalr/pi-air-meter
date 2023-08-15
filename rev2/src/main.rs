mod bme280;

use std::time::Duration;

use bme280::{init_i2c, BmeSensor};
use mh_z19::{read_gas_concentration, parse_gas_concentration_ppm};
use rppal::uart::{Uart, Parity};
use waveshare_rpi::{epd::epd7in5_v2::EPD_CONFIG, Epd};
use waveshare_rpi::util::{ColorMode, image_to_epd};

fn read_mhz19(uart: &mut Uart) -> u32 {
    uart.write(&read_gas_concentration(1)).unwrap();
    let mut buffer: [u8; 9] = [0; 9];
    uart.read(&mut buffer).unwrap();
    parse_gas_concentration_ppm(&buffer).unwrap()
}
fn main() {
    let i2c = init_i2c().unwrap();
    let mut uart = Uart::with_path("/dev/serial0", 9600, Parity::None, 8, 1).unwrap();
    uart.set_read_mode(9, Duration::default()).unwrap();
    let bme_reading = i2c.read_bme().unwrap();
    println!("Temperature: {}°C, Humidity: {}%, Pressure: {}hPa", bme_reading.0, bme_reading.1, bme_reading.2);
    println!("CO2: {}ppm", read_mhz19(&mut uart));
}
