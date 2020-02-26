from unittest import TestCase
from unittest.mock import patch, MagicMock, PropertyMock
from errors import MalformedCommandError, DuplicateVehicleError, ParkingFullError
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

    @patch("command_processor.Vehicle")
    @patch("command_processor.Driver")
    def test_park_command(self, driverMock, vehicleMock):
        command = 'Park KA-01-HH-1234 driver_age 21'
        parked_slot_mock = MagicMock()
        parked_slot_mock.return_value.parked_vehicle.number = "KA-01-HH-1234"
        type(parked_slot_mock.return_value).number = PropertyMock(return_value=1)
        self.parking_lot_service_mock.park_vehicle = parked_slot_mock
        output = self.command_processor.process(command)
        driverMock.assert_called_once_with(21)
        vehicleMock.assert_called_once_with("KA-01-HH-1234", driverMock.return_value)
        self.parking_lot_service_mock.park_vehicle.assert_called_once_with(vehicleMock.return_value)
        self.assertEqual(output, 'Car with vehicle registration number "KA-01-HH-1234" has been parked at slot number 1')

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

        command = "Park "
        self.helper_to_test_missing_command_args_error(command)

        command = "Park VIP-001 driver_age "
        self.helper_to_test_missing_command_args_error(command)

        command = "Park driver_age 21"
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

    def test_park_with_valid_data(self):
        command = "Create_parking_lot 3"
        output = self.command_processor.process(command)
        self.assertEqual(output, "Created parking of 3 slots")
        command = "Park KA-01-HH-1234 driver_age 21"
        output = self.command_processor.process(command)
        self.assertEqual(output, 'Car with vehicle registration number "KA-01-HH-1234" has been parked at slot number 1')

        command = "Park KA-01-HH-1234 driver_age 21"
        output = self.command_processor.process(command)
        self.assertEqual(output, "Vehicle with this registration number is already parked.")

        command = "Park KA-01-HH-1235 driver_age 21"
        output = self.command_processor.process(command)
        self.assertEqual(output, 'Car with vehicle registration number "KA-01-HH-1235" has been parked at slot number 2')

        command = "Park KA-01-HH-1236 driver_age 21"
        output = self.command_processor.process(command)
        self.assertEqual(output, 'Car with vehicle registration number "KA-01-HH-1236" has been parked at slot number 3')

        command = "Park KA-01-HH-1237 driver_age 21"
        output = self.command_processor.process(command)
        self.assertEqual(output, 'Cannot park more vehicles because parking is full.')

class IntergrationTestQueryCommandsProcessMethod(TestCase):
    def setUp(self):
        self.command_processor = CommandProcessor()
        command = "Create_parking_lot 5"
        self.command_processor.process(command)
        command = "Park KA-01 driver_age 21"
        output = self.command_processor.process(command)

        command = "Park KA-02 driver_age 18"
        output = self.command_processor.process(command)

        command = "Park KA-03 driver_age 18"
        output = self.command_processor.process(command)

        command = "Park KA-04 driver_age 21"
        output = self.command_processor.process(command)

    def test_invalid_query(self):
        command = "Slot_number_for_car_with_number "
        with self.assertRaises(MalformedCommandError) as e:
            output = self.command_processor.process(command)
            self.assertEqual(e.msg, "Missing command arguments.")

        command = "Slot_numbers_for_driver_of_age "
        with self.assertRaises(MalformedCommandError) as e:
            output = self.command_processor.process(command)
            self.assertEqual(e.msg, "Missing command arguments.")

        command = "Vehicle_registration_number_for_driver_of_age "
        with self.assertRaises(MalformedCommandError) as e:
            output = self.command_processor.process(command)
            self.assertEqual(e.msg, "Missing command arguments.")

        command = "Slot_numbers_for_driver_of_age csd"
        with self.assertRaises(MalformedCommandError) as e:
            output = self.command_processor.process(command)
            self.assertEqual(e.msg, "csd is not int. Age should be int.")

        command = "Vehicle_registration_number_for_driver_of_age sdc"
        with self.assertRaises(MalformedCommandError) as e:
            output = self.command_processor.process(command)
            self.assertEqual(e.msg, "sdc is not int. Age should be int.")

    def test_valid_commands(self):
        command = "Slot_number_for_car_with_number KA-01"
        output = self.command_processor.process(command)
        self.assertEqual(output, "1")
        command = "Slot_number_for_car_with_number KA-02"
        output = self.command_processor.process(command)
        self.assertEqual(output, "2")
        command = "Slot_number_for_car_with_number KA-03"
        output = self.command_processor.process(command)
        self.assertEqual(output, "3")
        command = "Slot_number_for_car_with_number KA-04"
        output = self.command_processor.process(command)
        self.assertEqual(output, "4")

        command = "Slot_number_for_car_with_number KA-05"
        output = self.command_processor.process(command)
        self.assertEqual(output, "")

        command = "Slot_numbers_for_driver_of_age 18"
        output = self.command_processor.process(command)
        self.assertEqual(output, "2,3")

        command = "Slot_numbers_for_driver_of_age 21"
        output = self.command_processor.process(command)
        self.assertEqual(output, "1,4")

        command = "Slot_numbers_for_driver_of_age 14"
        output = self.command_processor.process(command)
        self.assertEqual(output, "")

        command = "Vehicle_registration_number_for_driver_of_age 14"
        output = self.command_processor.process(command)
        self.assertEqual(output, "")

        command = "Vehicle_registration_number_for_driver_of_age 21"
        output = self.command_processor.process(command)
        self.assertEqual(output, "KA-01,KA-04")

        command = "Vehicle_registration_number_for_driver_of_age 18"
        output = self.command_processor.process(command)
        self.assertEqual(output, "KA-02,KA-03")

class IntergrationTestUnparkParkProcessMethod(TestCase):
    def setUp(self):
        self.command_processor = CommandProcessor()
        command = "Create_parking_lot 5"
        self.command_processor.process(command)
        command = "Park KA-01 driver_age 21"
        output = self.command_processor.process(command)

        command = "Park KA-02 driver_age 18"
        output = self.command_processor.process(command)

        command = "Park KA-03 driver_age 18"
        output = self.command_processor.process(command)

        command = "Park KA-04 driver_age 21"
        output = self.command_processor.process(command)

    def test_invalid_query(self):
        command = "Leave "
        with self.assertRaises(MalformedCommandError) as e:
            output = self.command_processor.process(command)
            self.assertEqual(e.msg, "Missing command arguments.")

        command = "Leave string"
        with self.assertRaises(MalformedCommandError) as e:
            output = self.command_processor.process(command)
            self.assertEqual(e.msg, "string is not int. Slot number should be int.")

    def test_valid_commands(self):
        command = "Leave 2"
        output = self.command_processor.process(command)
        self.assertEqual(output, 'Slot number 2 vacated, the car with vehicle registration number "KA-02" left the space, the driver of the car was of age 18')

        command = "Leave 3"
        output = self.command_processor.process(command)
        self.assertEqual(output, 'Slot number 3 vacated, the car with vehicle registration number "KA-03" left the space, the driver of the car was of age 18')

        command = "Leave 3"
        output = self.command_processor.process(command)
        self.assertEqual(output, 'Slot already vacant')

        command = "Park KA-05 driver_age 21"
        output = self.command_processor.process(command)
        self.assertEqual(output, 'Car with vehicle registration number "KA-05" has been parked at slot number 2')
