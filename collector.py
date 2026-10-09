""" This module simulates a data collector that reads from various sensors and stores the readings in a SQLite database. """
import time
from sensors import TemperatureSensor, HumiditySensor, MotionSensor
from storage import init_db, save_reading
import sqlite3
from contextlib import closing
from pprint import pprint
from storage import DB_path

INTERVAL_SECONDS = 5  # Interval between readings in seconds

def main():
    init_db()  # Initialize the database by creating the 'readings' table if it doesn't exist.
    # List of sensor instances to simulate readings from different types of sensors.
    sensors = [  
        TemperatureSensor(name="living_room_temp"),  # Temperature sensor for the living room
        HumiditySensor(name="living_room_humidity"),  # Humidity sensor for the living room
        MotionSensor(name="living_room_motion")  # Motion sensor for the living room
    ]

    print(f"Collector initialized and started. Reading every {INTERVAL_SECONDS} seconds...")  # Print a message indicating that the collector has started and the interval at which readings will be taken.

    next_time = time.monotonic() + INTERVAL_SECONDS
    try:
        while True:  # Infinite loop to continuously collect sensor readings.
            for sensor in sensors: 
                reading = sensor.read() # Call the read method of the sensor to get a new reading.
                save_reading(reading)  # Save the reading to the database.
                print(f"Saved reading: Sensor: {reading.sensor}, Value: {reading.value}{reading.unit}, Timestamp: {reading.timestamp.isoformat()}")  # Print the saved reading to the console for confirmation.
            wait_time= next_time - time.monotonic()  
            if wait_time>0: 
                time.sleep(wait_time)  
            next_time = next_time + INTERVAL_SECONDS


    except KeyboardInterrupt:  # Catch a keyboard interrupt (Ctrl+C) to allow graceful shutdown of the collector.
        print("Collector stopped by user.")  

if __name__ == "__main__":
    # main()  # Call the main function to start the collector.

    with closing(sqlite3.connect(DB_path)) as conn: # Connect to the SQLite database specified by DB_path and ensure the connection is closed after use.    
        with conn: 
            try:
                cursor= conn.execute("SELECT * FROM readings")  # Execute an SQL query to select all records from the 'readings' table.
                for row in cursor:  
                    pprint(row)
            except sqlite3.Error as e:
                print(f"Error occurred while fetching readings: {e}")
