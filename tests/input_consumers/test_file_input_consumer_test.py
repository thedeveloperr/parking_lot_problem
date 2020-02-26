from unittest import TestCase
from unittest.mock import patch, MagicMock, PropertyMock, call
from input_consumers.file_input_consumer import FileInputConsumer
import os
from io import StringIO

class UnitTestProcessMethod(TestCase):

    @patch('sys.stdout')
    def test_file_reading(self, mockPrint):
        command_processor = MagicMock()
        command_processor.process = MagicMock(return_value="mock output")
        input_consumer = FileInputConsumer(command_processor)
        file_name = os.path.join(os.path.dirname(__file__), '../data/test1.txt')

        input_consumer.consume(file_name)
        commands = [
          call("Create_parking_lot 6"),
          call("Park KA-01-HH-1234 driver_age 21"),
          call("Park PB-01-HH-1234 driver_age 21"),
          call("Slot_numbers_for_driver_of_age 21"),
          call("Park PB-01-TG-2341 driver_age 40"),
          call("Slot_number_for_car_with_number PB-01-HH-1234"),
          call("Leave 2"),
          call("Park HR-29-TG-3098 driver_age 39"),
          call("Vehicle_registration_number_for_driver_of_age 18"),
        ]
        command_processor.process.assert_has_calls(commands)
        mockPrint.write.assert_has_calls([
            call('mock output'),
            call('\n'),
            call('mock output'),
            call('\n'),
            call('mock output'),
            call('\n'),
            call('mock output'),
            call('\n'),
            call('mock output'),
            call('\n'),
            call('mock output'),
            call('\n'),
            call('mock output'),
            call('\n'),
            call('mock output'),
            call('\n'),
            call('mock output'),
            call('\n')
        ])
