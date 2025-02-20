mod bme280;

use std::time::Duration;
use std::thread::sleep;

use bme280::{init_i2c, BmeSensor};
use mh_z19::{read_gas_concentration, parse_gas_concentration_ppm};
use rppal::uart::{Uart, Parity};
use sqlite::{open, Connection};
use waveshare_rpi::{epd::epd7in5_v2::EPD_CONFIG, Epd};
use waveshare_rpi::util::{ColorMode, image_to_epd};

const DB_FILE: &str = "data.sqlite3";
const TIME_PER_READING: u64 = 120;

fn init_db() -> Result<Connection, sqlite::Error> {
    let conn = Connection::open(DB_FILE)?;
    let init_query = "CREATE TABLE IF NOT EXISTS air_logs (
        id INTEGER PRIMARY KEY,
        co2 INTEGER NOT NULL,
        temp DOUBLE NOT NULL,
        humidity DOUBLE NOT NULL,
        pressure INTEGER NOT NULL,
        created_at DATETIME DEFAULT (datetime('now', 'localtime')));";
    conn.execute(init_query)?;
    Ok(conn)
}

fn insert_record(db_conn: &Connection, co2: u32, temp: f32, hum: f32, pres: f32) -> Result<(), sqlite::Error> {
    let insert_query = format!("INSERT INTO air_logs (co2, temp, humidity, pressure) VALUES ({}, {}, {}, {})", co2, temp, hum, pres);
    db_conn.execute(&insert_query)?;
    Ok(())
}

// TODO Make it more fail-safe by returning Result instead
fn read_mhz19(uart: &mut Uart) -> u32 {
    uart.write(&read_gas_concentration(1)).unwrap();
    let mut buffer: [u8; 9] = [0; 9];
    uart.read(&mut buffer).unwrap();
    parse_gas_concentration_ppm(&buffer).unwrap()
}
fn main() {
    if let Ok(db_conn) = init_db() {
        let i2c = init_i2c().unwrap();
        let mut uart = Uart::with_path("/dev/serial0", 9600, Parity::None, 8, 1).unwrap();
        uart.set_read_mode(9, Duration::default()).unwrap();
        loop {
            let bme_reading = i2c.read_bme().unwrap(); // TODO handle err instead of unwrapping
            let co2 = read_mhz19(&mut uart);
            insert_record(&db_conn, co2, bme_reading.0, bme_reading.1, bme_reading.2).unwrap();
            println!("Temperature: {}°C, Humidity: {}%, Pressure: {}hPa", bme_reading.0, bme_reading.1, bme_reading.2);
            println!("CO2: {}ppm", read_mhz19(&mut uart));
            sleep(Duration::from_secs(TIME_PER_READING));
        }
    } else {
        println!("Failed to initialize database! Exiting.");
    }
    
}
