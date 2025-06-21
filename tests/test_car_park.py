import json
import unittest
from car_park import CarPark
from pathlib import Path

class TestCarPark(unittest.TestCase):
    def setUp(self):
        self.log_path = Path("test_log.txt")
        self.config_path = Path("test_config.json")
        self.car_park = CarPark("123 Example Street", 100, log_file=self.log_path, config_file=self.config_path)

    def test_car_park_initialized_with_all_attributes(self):
        self.assertIsInstance(self.car_park, CarPark)
        self.assertEqual(self.car_park.location, "123 Example Street")
        self.assertEqual(self.car_park.capacity, 100)
        self.assertEqual(self.car_park.plates, [])
        self.assertEqual(self.car_park.displays, [])
        self.assertEqual(self.car_park.available_bays, 100)
        self.assertEqual(self.car_park.log_file, self.log_path)

    def test_add_car(self):
        self.car_park.add_car("FAKE-001")
        self.assertEqual(self.car_park.plates, ["FAKE-001"])
        self.assertEqual(self.car_park.available_bays, 99)

    def test_remove_car(self):
        self.car_park.add_car("FAKE-001")
        self.car_park.remove_car("FAKE-001")
        self.assertEqual(self.car_park.plates, [])
        self.assertEqual(self.car_park.available_bays, 100)

    def test_overfill_the_car_park(self):
        for i in range(100):
            self.car_park.add_car(f"FAKE-{i}")
        self.assertEqual(self.car_park.available_bays, 0)
        self.car_park.add_car("FAKE-100")
        # Overfilling the car park should not change the number of available bays
        self.assertEqual(self.car_park.available_bays, 0)

     # Removing a car from an overfilled car park should not change the number of available bays
        self.car_park.remove_car("FAKE-100")
        self.assertEqual(self.car_park.available_bays, 0)

    def test_removing_a_car_that_does_not_exist(self):
     with self.assertRaises(ValueError):
        self.car_park.remove_car("NO-1")

    def test_register_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.car_park.register("Not a Sensor or Display")

    def test_log_file_created(self):
        self.assertTrue(self.log_path.exists())


    def test_car_logged_when_entering(self):
        self.car_park.add_car("NEW-001")
        with self.car_park.log_file.open() as f:
            last_line = f.readlines()[-1]
        self.assertIn("NEW-001", last_line)  # check plate entered
        self.assertIn("entered", last_line)  # check description
        self.assertIn("\n", last_line)  # check entry has a new line


    def test_car_logged_when_exiting(self):
        self.car_park.add_car("NEW-001")
        self.car_park.remove_car("NEW-001")
        with self.car_park.log_file.open() as f:
            last_line = f.readlines()[-1]
        self.assertIn("NEW-001", last_line)  # check plate entered
        self.assertIn("exited", last_line)  # check description
        self.assertIn("\n", last_line)  # check entry has a new line

    def test_write_config_creates(self):
        self.car_park.write_config()
        self.assertTrue(self.config_path.exists())

        with self.config_path.open() as f:
            config_data = json.load(f)

        self.assertEqual(config_data["location"], self.car_park.location)
        self.assertEqual(config_data["capacity"], self.car_park.capacity)
        self.assertEqual(config_data["log_file"], str(self.log_path))

    def test_from_config_creates_car_park(self):
        self.car_park.write_config()
        new_car_park = CarPark.from_config(self.config_path)
        self.assertEqual(new_car_park.location, self.car_park.location)
        self.assertEqual(new_car_park.capacity, self.car_park.capacity)
        self.assertEqual(str(new_car_park.log_file), str(self.log_path))


    def tearDown(self):
        self.log_path.unlink(missing_ok=True)
        self.config_path.unlink(missing_ok=True)


if __name__ == "__main__":
   unittest.main()
