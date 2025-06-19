from sensor import Sensor
from display import Display
from pathlib import Path
from datetime import datetime
import json

class CarPark:
    def __init__(self, location, capacity, plates=None, displays=None, sensors=None, log_file=Path("log.txt"), config_file=Path("config.json")):
        self.location = location
        self.capacity = capacity
        self.plates = plates or []
        self.displays = displays or []
        self.sensors = sensors or []
        self.log_file = log_file if isinstance(log_file, Path) else Path(log_file)
        self.log_file.touch(exist_ok=True)
        self.config_file = config_file if isinstance(config_file, Path) else Path(config_file)

    def __str__(self):
        return f"Car park at {self.location} has {self.capacity}"

    @property
    def available_bays(self):
        return max(0, self.capacity - len(self.plates))

    def update_displays(self):
        data = {"available_bays": self.available_bays, "temperature": 25}
        for display in self.displays: display.update(data)

    def register(self, component):
        if not isinstance(component, (Sensor, Display)):
            raise TypeError("Object must be a Sensor or Display")

        if isinstance(component, Display):
            self.displays.append(component)

        if isinstance(component, Sensor):
            self.sensors.append(component)

    def _log_car_activity(self, plate, action):
        with self.log_file.open('a') as f:
            f.write(f"{plate} {action} at {datetime.now():%Y-%m-%d %H:%M:%S}\n")

    def add_car(self, plate):
        self.plates.append(plate)
        self.update_displays()
        self._log_car_activity(plate, "entered")

    def remove_car(self, plate):
        self.plates.remove(plate)
        self.update_displays()
        self._log_car_activity(plate, "exited")

    def write_config(self):
        with open(self.config_file, 'w') as f:
            json.dump({"location": self.location,
                       "capacity": self.capacity,
                       "log_file": str(self.log_file)}, f)

    @classmethod
    def from_config(cls, config_file=Path("config.json")):
        config_file = config_file if isinstance(config_file, Path) else Path(config_file)
        with config_file.open() as f:
            config = json.load(f)
        return cls(config["location"], config["capacity"], log_file=config["log_file"])

