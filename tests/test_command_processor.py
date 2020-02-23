from unittest import TestCase
from unittest.mock import patch, MagicMock
from errors import MalformedCommandError
from command_processor import CommandProcessor

class UnitTestProcessMethod(TestCase):

    @patch("command_processor.ParkingLotService")
    @patch("command_processor.ParkingLotDao")
    def setUp(self, daoMock, serviceMock):
        self.command_processor = CommandProcessor()
        self.parking_lot_service_mock = serviceMock.return_value
    def test_init_command(self):
        command = "Create_parking_lot 7"
        self.parking_lot_service_mock.create_parking_lot_of_size = MagicMock(return_value=7)
        output = self.command_processor.process(command)
        self.parking_lot_service_mock.create_parking_lot_of_size.assert_called_once_with(7)
        self.assertEqual(output, "Created parking of 7 slots")

    def helper_to_test_missing_command_args_error(self, command):
        with self.assertRaises(MalformedCommandError) as e:
            output = self.command_processor.process(command)
            self.assertEqual(e.msg, "Missing command arguments.")

    def helper_to_test_missing_operation_in_command_error(self, command):
        with self.assertRaises(MalformedCommandError) as e:
            output = self.command_processor.process(command)
            self.assertEqual(e.msg, command + " missing valid operation.")

    def test_error_thrown_on_invalid_command(self):
        command = "Create_parking_lot"
        self.helper_to_test_missing_command_args_error(command)

        command = "Create_parking_lot "
        self.helper_to_test_missing_command_args_error(command)

        command = "Invalidop 6"
        self.helper_to_test_missing_operation_in_command_error(command)

        command = "Create_parking_lot invalid_size"
        with self.assertRaises(MalformedCommandError) as e:
            output = self.command_processor.process(command)
            self.assertEqual(e.msg, "invalid_size is not int. Slot size should be int.")

class IntergrationTestProcessMethod(TestCase):
    def setUp(self):
        self.command_processor = CommandProcessor()

    def test_init_command(self):
        command = "Create_parking_lot 6"
        output = self.command_processor.process(command)
        self.assertEqual(output, "Created parking of 6 slots")

    def test_init_with_non_positive_int_size(self):
        command = "Create_parking_lot -6"
        with self.assertRaises(MalformedCommandError) as e:
            output = self.command_processor.process(command)
            self.assertEqual(e.msg, "Lot size should be positive integer")

        command = "Create_parking_lot 6.3"
        with self.assertRaises(MalformedCommandError) as e:
            output = self.command_processor.process(command)
            self.assertEqual(e.msg, "Lot size should be positive integer")

        command = "Create_parking_lot 0"
        with self.assertRaises(MalformedCommandError) as e:
            output = self.command_processor.process(command)
            self.assertEqual(e.msg, "Lot size should be positive integer")
