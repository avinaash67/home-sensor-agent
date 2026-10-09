import random
from datetime import datetime, timezone # datetime module imports the datetime class for timestamping readings and timezone for handling time zones
from dataclasses import dataclass # dataclasses module is used to create data classes for structured data
from abc import ABC, abstractmethod # abc module is used to create abstract base classes for sensors

# Dataclasses
@dataclass
class Reading: 
    sensor: str # e.g. living_room_temperature
    value: float # e.g. 22.5
    unit: str # e.g. "°C"
    timestamp: datetime # e.g. "2023-10-01T12:00:00Z"


class Sensor(ABC):  # ABC refers to Abstract Base Class, which is a class that cannot be instantiated on its own and is meant to be subclassed by other classes.
    def __init__(self, name: str):   
        self.name = name 
    
    @abstractmethod
    def read(self) -> Reading:
        """ Return one new reading from the sensor. """

class TemperatureSensor(Sensor):
    def __init__(self, name: str, initial_temp: float = 22.0):
        super().__init__(name)
        self.temperature = initial_temp  # Initialize the temperature with a default value of 22.0°C

    def next_temperature(self, previous: float) -> float:
        """Simulate a temperature sensor reading."""
        # Simulate a temperature change by adding a random value between -0.5 and 0.5 to the previous temperature
        delta = random.uniform(-0.5, 0.5)
        new_temp = previous + delta
        new_temp = max(-5, min(35, new_temp))  # Clamp the temperature between -5 and 35
        return round(new_temp, 2)  # Round the new temperature to two decimal places
    
    def read(self)-> Reading:
        """Returns a new temperature reading from the sensor."""
        self.temperature = self.next_temperature(previous=self.temperature)  # Update the temperature with a new simulated reading
        return Reading(
            sensor=self.name,
            value=self.temperature,
            unit="°C",
            timestamp = datetime.now(timezone.utc) 
        )
class HumiditySensor(Sensor):
    
    def __init__(self, name:str, initial_humidity: float = 50.0):
        super().__init__(name)
        self.humidity = initial_humidity  # Initialize the humidity with a default value of 50.0%
    
    def next_humidity(self, previous: float) -> float:
        """ Simulate the humidity sensor reading. """
        delta = random.uniform(-1.0, 1.0)  # Simulate a humidity change by adding a random value between -1.0 and 1.0 to the previous humidity
        new_humidity = previous + delta
        new_humidity = max(0, min(100, new_humidity))  # Clamp the humidity between 0 and 100
        return round(new_humidity, 2)  # Round the new humidity to two decimal places

    def read(self) -> Reading:
        """Returns a new humidity reading from the sensor."""
        self.humidity = self.next_humidity(previous=self.humidity) # Update the humidity with a new simulated reading
        return Reading(
            sensor= self.name, 
            value = self.humidity,
            unit = "%",
            timestamp = datetime.now(timezone.utc)  # timezone.utc ensures that the timestamp is in Coordinated Universal Time (UTC) format, which is a standard time format used for consistency across different time zones.
        )

class MotionSensor(Sensor):
    """ Simulate a motion sensor reading. """
    def __init__(self, name: str, previous_motion: bool = False):
        super().__init__(name)
        self.motion_detected = previous_motion  # Initialize the motion detected state

    def read(self) -> Reading:
        """Returns a new motion reading from the sensor."""
        # Simulate motion detection with a 10% chance of detecting motion
        self.motion_detected = min(1.0, max(0.0, random.random())) < 0.1  # 10% chance of motion detection
        value = 1.0 if self.motion_detected else 0.0  # Set value to 1.0 if motion is detected, otherwise 0.0
        return Reading(
            sensor=self.name,
            value=value,
            unit="motion",
            timestamp=datetime.now(timezone.utc)
        )


if __name__ == "__main__":
    # Create an instance of the TemperatureSensor class
    # Initially we do a test using single sensor instances and print their readings to the console.
    temperature_living_room_sensor = TemperatureSensor(name = "Temperature_living_room", initial_temp=22.0)
    reading = temperature_living_room_sensor.read() # the reading variable is of type Reading, which is a dataclass that holds the sensor name, value, unit, and timestamp of the reading.
    print(type(reading))  # Print the type of the reading variable to confirm it is a Reading object
    print(f"Sensor: {reading.sensor}, Value: {reading.value}{reading.unit}, Timestamp: {format(reading.timestamp, '%Y-%m-%d %H:%M:%S')}")  # timestamp = datetime.now().isoformat()  # Get the current timestamp in ISO 8601 format

    humidity_living_room_sensor = HumiditySensor(name= "Humidity_living_room", initial_humidity=50.0)
    reading = humidity_living_room_sensor.read()
    print(f"Sensor: {reading.sensor}, Value: {reading.value}{reading.unit}, Timestamp: {format(reading.timestamp, '%Y-%m-%d %H:%M:%S')}")

    motion_living_room_sensor = MotionSensor(name= "Motion_living_room", previous_motion=False)
    reading = motion_living_room_sensor.read()
    print(f"Sensor: {reading.sensor}, Value: {reading.value}{reading.unit}, Timestamp: {format(reading.timestamp, '%Y-%m-%d %H:%M:%S')}")

    # Now we will create a list of sensor instances and iterate over them to read their values and print the readings to the console.
    sensors = [temperature_living_room_sensor, humidity_living_room_sensor, motion_living_room_sensor]  # Create a list of sensor instances
    for sensor in sensors:  # Iterate over each sensor in the list
        reading = sensor.read()
        print(f"Sensor: {reading.sensor}, Value: {reading.value}{reading.unit}, Timestamp: {format(reading.timestamp, '%Y-%m-%d %H:%M:%S')}")  # Print the reading details for each sensor