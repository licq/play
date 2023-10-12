import unittest
from unittest.mock import patch
import time

# Import the `retry` function
from utils import retry

class TestRetryFunction(unittest.TestCase):
    def test_successful_function(self):
        # Define a function that always succeeds
        def my_function(param):
            return "Success"

        result = retry(my_function, max_attempts=5, param="some_param")
        self.assertEqual(result, "Success")

    def test_failed_function(self):
        # Define a function that always fails
        def my_function(param):
            raise ValueError("Error")

        result = retry(my_function, max_attempts=3, delay=1, param="some_param")
        self.assertIsNone(result)

    def test_successful_function_after_retry(self):
        # Define a function that fails the first two times and succeeds on the third attempt
        attempts = [0]  # A list to store the number of attempts

        def my_function(param):
            attempts[0] += 1
            if attempts[0] < 3:
                raise ValueError("Error")
            return "Success"

        result = retry(my_function, max_attempts=5, delay=1, param="some_param")
        self.assertEqual(result, "Success")
        self.assertEqual(attempts[0], 3)

    def test_function_with_mocked_delay(self):
        # Define a function with a mocked delay between retries
        def my_function(param):
            return "Success"

        # Mock the time.sleep function to avoid actual delays
        with patch('time.sleep') as sleep_mock:
            sleep_mock.side_effect = lambda _: None  # Mock time.sleep to do nothing

            result = retry(my_function, max_attempts=5, delay=1, param="some_param")
            self.assertEqual(result, "Success")

if __name__ == '__main__':
    unittest.main()
