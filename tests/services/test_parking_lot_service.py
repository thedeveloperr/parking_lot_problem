from unittest import TestCase
from unittest.mock import MagicMock
from services.parking_lot_service import ParkingLotService
from data_access_objects.in_memory_parking_lot import ParkingLotDao

class UnitTestCreateParkingLotMethod(TestCase):
    def setUp(self):
        self.dao = MagicMock()
        self.service = ParkingLotService(self.dao)

    def test_with_valid_size(self):
        self.dao.create_slots = MagicMock(return_value = True)
        num_slots = self.service.create_parking_lot_of_size(6)
        self.assertEqual(6, num_slots)
        self.dao.create_slots.assert_called_once_with(6);

    def test_with_invalid_size(self):
        self.dao.create_slots = MagicMock(return_value = False)
        with self.assertRaises(ValueError) as e:
            num_slots = self.service.create_parking_lot_of_size(-6)
            output = self.command_processor.process(command)
        self.dao.create_slots.assert_not_called();

        with self.assertRaises(ValueError) as e:
            num_slots = self.service.create_parking_lot_of_size(6.3)
            output = self.command_processor.process(command)
        self.dao.create_slots.assert_not_called();

        with self.assertRaises(ValueError) as e:
            num_slots = self.service.create_parking_lot_of_size("6")
            output = self.command_processor.process(command)
        self.dao.create_slots.assert_not_called();

class IntegrationTestCreateParkingLotMethod(TestCase):
    def setUp(self):
        self.dao = ParkingLotDao()
        self.service = ParkingLotService(self.dao)

    def test_with_valid_size(self):
        num_slots = self.service.create_parking_lot_of_size(6)
        self.assertEqual(6, num_slots)
