class Sensor:
    def __init__(self, id, is_active, car_park):
        self.id = id
        self.is_active = is_active
        self.car_park = car_park

class EntrySensor(Sensor):
    ...
class ExitSensor(Sensor):
    ...
