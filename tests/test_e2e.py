from unittest import TestCase
from unittest.mock import patch, MagicMock, PropertyMock, call
from input_consumers.file_input_consumer import FileInputConsumer
from command_processor import CommandProcessor
import os
from io import StringIO


class E2eTest(TestCase):
    @patch("sys.stdout")
    def test_file_reading(self, mockPrint):
        command_processor = CommandProcessor()
        input_consumer = FileInputConsumer(command_processor)
        file_name = os.path.join(os.path.dirname(__file__), "./data/test1.txt")
        input_consumer.consume(file_name)
        mockPrint.write.assert_has_calls(
            [
                call("Created parking of 6 slots"),
                call("\n"),
                call(
                    'Car with vehicle registration number "KA-01-HH-1234" has been parked at slot number 1'
                ),
                call("\n"),
                call(
                    'Car with vehicle registration number "PB-01-HH-1234" has been parked at slot number 2'
                ),
                call("\n"),
                call("1,2"),
                call("\n"),
                call(
                    'Car with vehicle registration number "PB-01-TG-2341" has been parked at slot number 3'
                ),
                call("\n"),
                call("2"),
                call("\n"),
                call(
                    'Slot number 2 vacated, the car with vehicle registration number "PB-01-HH-1234" left the space, the driver of the car was of age 21'
                ),
                call("\n"),
                call(
                    'Car with vehicle registration number "HR-29-TG-3098" has been parked at slot number 2'
                ),
                call("\n"),
                call(""),
                call("\n"),
            ]
        )
