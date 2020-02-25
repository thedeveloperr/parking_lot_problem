from unittest import TestCase
from unittest.mock import MagicMock
from services.parking_lot_service import ParkingLotService
from data_access_objects.in_memory_parking_lot import ParkingLotDao
from models import ParkingSlot, Driver, Vehicle
from errors import NoneVehicleError, DuplicateVehicleError, ParkingFullError, InvalidDriverError, ParkingNotCreatedError

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

class UnitTestParkVehicleMethod(TestCase):
    def setUp(self):
        self.dao = MagicMock()
        self.dao.create_slots = MagicMock(return_value=True)
        self.service = ParkingLotService(self.dao)

    def test_with_valid_vehicle(self):
        driver = Driver(33)
        vehicle = Vehicle("random", driver)
        slot = ParkingSlot(1, vehicle)
        self.dao.park_vehicle_at_closest_empty_slot = MagicMock(return_value=slot)
        res = self.service.park_vehicle(vehicle)
        self.dao.park_vehicle_at_closest_empty_slot.assert_called_once_with(vehicle)
        self.assertEqual(res, slot)

class IntegrationTestParkVehicle(TestCase):
    def setUp(self):
        self.dao = ParkingLotDao()
        self.service = ParkingLotService(self.dao)

    def test_with_valid_vehicle(self):
        num_slots = self.service.create_parking_lot_of_size(2)
        self.assertEqual(2, num_slots)
        driver = Driver(22)
        vehicle1 = Vehicle("pb08-11-22-random", driver)
        parked_slot = self.service.park_vehicle(vehicle1)
        self.assertEqual(parked_slot.number, 1)
        self.assertEqual(parked_slot.parked_vehicle.number, "pb08-11-22-random")
        driver = Driver(23)
        vehicle1clone = Vehicle("pb08-11-22-random", driver)
        with self.assertRaises(DuplicateVehicleError):
            parked_slot = self.service.park_vehicle(vehicle1clone)

        driver = Driver(23)
        vehicle2 = Vehicle("pb08-11-23-random", driver)
        parked_slot = self.service.park_vehicle(vehicle2)
        self.assertEqual(parked_slot.number, 2)
        self.assertEqual(parked_slot.parked_vehicle.number, "pb08-11-23-random")

        driver = Driver(23)
        vehicle4 = Vehicle("pb08-11-34-random", driver)
        with self.assertRaises(ParkingFullError):
            parked_slot = self.service.park_vehicle(vehicle4)
            self.assertEqual(len(self.dao.empty_slots_heap), 0)


    def test_with_none_vehicle(self):
        num_slots = self.service.create_parking_lot_of_size(2)
        self.assertEqual(2, num_slots)
        with self.assertRaises(NoneVehicleError):
            parked_slot = self.service.park_vehicle(None)


    def test_with_invalid_driver(self):
        num_slots = self.service.create_parking_lot_of_size(2)
        self.assertEqual(2, num_slots)
        with self.assertRaises(InvalidDriverError):
            driver = None
            v =Vehicle("rndomplate", driver)
            parked_slot = self.service.park_vehicle(v)
        with self.assertRaises(InvalidDriverError):
            driver = Driver(None)
            v =Vehicle("rndomplate", driver)
            parked_slot = self.service.park_vehicle(v)

