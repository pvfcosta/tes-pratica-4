import os
import unittest
import tempfile
import json
from dataProcessor import read_json_file, avg_age_country, calculate_average_age

class TestDataProcessor(unittest.TestCase):
    def test_read_json_file_success(self):
        current_directory = os.path.dirname(__file__)
        file_path = os.path.join(current_directory, "../users.json")

        data = read_json_file(file_path)
       
        self.assertEqual(len(data), 1000)
        self.assertEqual(data[0]['name'], 'Kathryn Vincent')
        self.assertEqual(data[1]['age'], 57)

    def test_read_json_file_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            read_json_file("non_existent.json")

    def test_read_json_file_invalid_json(self):
        with open("invalid.json", "w") as file:
            file.write("invalid json data")
        with self.assertRaises(ValueError) as context:
            read_json_file("invalid.json")

    def test_avg_age_country_success(self):
        current_directory = os.path.dirname(__file__)
        file_path = os.path.join(current_directory, "../users.json")
        result = avg_age_country(file_path)

        self.assertAlmostEqual(result['age']["BR"], 37.596491, 2)
        self.assertAlmostEqual(result['age']["UK"], 39.549618, 2)
        self.assertAlmostEqual(result['age']["CA"], 39.459459, 2)

    def test_avg_age_country_no_country_exception(self):
        current_directory = os.path.dirname(__file__)
        file_path = os.path.join(current_directory, "../users_country.json")

        with self.assertRaises(ValueError) as context:
            avg_age_country(file_path)
        self.assertIn("Missing country from ", str(context.exception))

    def test_avg_age_country_no_age_exception(self):
        current_directory = os.path.dirname(__file__)
        file_path = os.path.join(current_directory, "../users_age.json")

        with self.assertRaises(ValueError) as context:
            avg_age_country(file_path)
        self.assertIn("Missing age from ", str(context.exception))

    def test_average_age(self):
        average_age = calculate_average_age(self.test_file.name)
        expected_average = (25 + 30 + 35) / 3
        self.assertAlmostEqual(average_age, expected_average, places=2)

    def test_empty_list(self):
        empty_data = []
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as empty_file:
            json.dump(empty_data, empty_file)
        average_age = calculate_average_age(empty_file.name)
        self.assertEqual(average_age, 0)

    def test_average_age(self):
        current_directory = os.path.dirname(__file__)
        file_path = os.path.join(current_directory, "../users.json")
        average_age = calculate_average_age(file_path)
        expected_average = 38.634
        self.assertAlmostEqual(average_age, expected_average, places=2)

    def test_missing_age_key(self):
        current_directory = os.path.dirname(__file__)
        file_path = os.path.join(current_directory, "../users_age.json")
        with self.assertRaises(ValueError) as context:
            calculate_average_age(file_path)
        self.assertIn("Cada objeto na lista deve conter a chave 'age'.", str(context.exception))

if __name__ == '__main__':
    unittest.main()