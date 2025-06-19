from car_park import CarPark
from sensor import EntrySensor, ExitSensor
from display import Display

# Create a car park object with the location moondalup, capacity 100, and log_file "moondalup.txt"
log_path = "moondalup.txt"
config_path = "moondalup_config.json"
car_park = CarPark("Moondalup", 100, log_file=log_path, config_file=config_path)


# Write the car park configuration to a file called "moondalup_config.json"
car_park.write_config()

# Reinitialize the car park object from the "moondalup_config.json" file
moondalup = car_park.from_config(config_path)


# Create an entry sensor object with id 1, is_active True, and car_park car_park
moondalup_entry = EntrySensor(1, True, car_park)

# Create an exit sensor object with id 2, is_active True, and car_park car_park
moondalup_exit = ExitSensor(2, True, car_park)

# Create a display object with id 1, message "Welcome to Moondalup", is_on True, and car_park car_park
moondalup_display = Display(1,"Welcome to Moondalup", True)

# Drive 10 cars into the car park (must be triggered via the sensor - NOT by calling car_park.add_car directly)
for i in range(10):
    moondalup_entry.update_car_park(f"Real{i}")

# Drive 2 cars out of the car park (must be triggered via the sensor - NOT by calling car_park.remove_car directly)
for i in range(2):
    moondalup_exit.update_car_park(f"Real{i}")
