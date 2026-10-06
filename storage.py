""" 
This module provides functions to initialize a SQLite database and save sensor readings to it. 
It uses the sqlite3 library for database operations and contextlib for resource management. 
The module also imports sensor classes from sensors.py to handle different types of sensor readings.
"""

import sqlite3 # SQLite database support
from contextlib import closing # Clean up resources
from sensors import Reading, TemperatureSensor, HumiditySensor, MotionSensor # Sensor classes
from pprint import pprint # Pretty print data
from pathlib import Path # File path handling
import random # Random values
from datetime import datetime # Date and time

DB_path = Path(__file__).parent / "sensor_readings.db"  # Define the path to the SQLite database file, which will be located in the same directory as this script.


def init_db():
    """ Create the database table if it doesn't exist. """
    with closing(sqlite3.connect(DB_path)) as conn:  # Connect to the SQLite database specified by DB_path and ensure the connection is closed after use.
        with conn: # Start a transaction block. If an exception occurs, the transaction will be rolled back.
            conn.execute (""" 
                CREATE TABLE IF NOT EXISTS readings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,  
                    sensor TEXT NOT NULL,  
                    value REAL NOT NULL,  
                    unit TEXT NOT NULL, 
                    timestamp TEXT NOT NULL  
                )
            """) 
                
def save_reading(reading: Reading):
    """ Save one sensor reading to the database. """
    with closing(sqlite3.connect(DB_path)) as conn:  # Connect to the SQLite database specified by DB_path and ensure the connection is closed after use.
        with conn:
            conn.execute(
                "INSERT INTO readings (sensor, value, unit, timestamp) VALUES (?, ?, ?, ?)",  # Prepare an SQL statement to insert a new reading into the 'readings' table.
                (reading.sensor, reading.value, reading.unit, reading.timestamp.isoformat()) # Provide the values for the SQL statement using the attributes of the Reading dataclass. Time stored in ISO 8601 format for consistency and easy parsing.
            )

if __name__ == "__main__":
    init_db()  # Initialize the database by creating the 'readings' table if it doesn't exist.

    test_reading = Reading(sensor="TestSensor", value= random.uniform(0, 100), unit="units", timestamp=datetime.now())  # Create a test Reading instance with sample data.
    save_reading(test_reading)  # Save the test reading to the database.

    print("Test reading saved to the database.")  # Print a confirmation message to the console.
    
    with closing(sqlite3.connect(DB_path)) as conn: # Connect to the SQLite database specified by DB_path and ensure the connection is closed after use.
        with conn: # Start a transaction block. If an exception occurs, the transaction will be rolled back.
            try:
                cursor= conn.execute("SELECT * FROM readings")  # Execute an SQL query to select all records from the 'readings' table.
                for row in cursor:  
                    pprint(row)  
            except sqlite3.OperationalError as e:  # Catch any operational errors that occur during the database operation.
                print(f"An error occurred: {e}")  
    print("Closing used here because we are using the context manager to ensure that the database connection is properly closed after use, preventing resource leaks and ensuring data integrity.")
