from unittest import TestCase
from unittest.mock import MagicMock
from services.parking_lot_service import ParkingLotService
from data_access_objects.in_memory_parking_lot import ParkingLotDao
from models import ParkingSlot, Driver, Vehicle
from errors import (
    NoneVehicleError,
    DuplicateVehicleError,
    ParkingFullError,
    InvalidDriverError,
    ParkingNotCreatedError,
)


class UnitTestCreateParkingLotMethod(TestCase):
    def setUp(self):
        self.dao = MagicMock()
        self.service = ParkingLotService(self.dao)

    def test_with_valid_size(self):
        self.dao.create_slots = MagicMock(return_value=True)
        num_slots = self.service.create_parking_lot_of_size(6)
        self.assertEqual(6, num_slots)
        self.dao.create_slots.assert_called_once_with(6)

    def test_with_invalid_size(self):
        self.dao.create_slots = MagicMock(return_value=False)
        with self.assertRaises(ValueError) as e:
            num_slots = self.service.create_parking_lot_of_size(-6)
            output = self.command_processor.process(command)
        self.dao.create_slots.assert_not_called()

        with self.assertRaises(ValueError) as e:
            num_slots = self.service.create_parking_lot_of_size(6.3)
            output = self.command_processor.process(command)
        self.dao.create_slots.assert_not_called()

        with self.assertRaises(ValueError) as e:
            num_slots = self.service.create_parking_lot_of_size("6")
            output = self.command_processor.process(command)
        self.dao.create_slots.assert_not_called()


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
            v = Vehicle("rndomplate", driver)
            parked_slot = self.service.park_vehicle(v)
        with self.assertRaises(InvalidDriverError):
            driver = Driver(None)
            v = Vehicle("rndomplate", driver)
            parked_slot = self.service.park_vehicle(v)


class IntegrationTestGovtRegulationQueries(TestCase):
    def setUp(self):
        self.dao = ParkingLotDao()
        self.service = ParkingLotService(self.dao)
        self.service.create_parking_lot_of_size(3)

        d1 = Driver(18)
        v1 = Vehicle("num1", d1)
        self.service.park_vehicle(v1)

        d2 = Driver(18)
        v2 = Vehicle("num2", d2)
        self.service.park_vehicle(v2)

        d3 = Driver(20)
        v3 = Vehicle("num3", d3)
        self.service.park_vehicle(v3)

    def test_vehicle_number_to_slot_number(self):
        self.assertEqual(self.service.get_slot_number_for_vehicle_number("num1"), 1)
        self.assertEqual(self.service.get_slot_number_for_vehicle_number("num2"), 2)
        self.assertEqual(self.service.get_slot_number_for_vehicle_number("num3"), 3)

    def test_slot_numbers_for_age(self):
        slot_nums = self.service.get_slot_numbers_for_driver_age(18)
        self.assertEqual(slot_nums[0], 1)
        self.assertEqual(slot_nums[1], 2)

        slot_nums = self.service.get_slot_numbers_for_driver_age(18)
        self.assertEqual(slot_nums[0], 1)

        slot_nums = self.service.get_slot_numbers_for_driver_age(14)
        self.assertEqual(len(slot_nums), 0)

    def test_parked_vehicle_number_for_age(self):
        vehicle_nums = self.service.get_parked_vehicle_numbers_of_driver_age(18)
        self.assertEqual(vehicle_nums[0], "num1")
        self.assertEqual(vehicle_nums[1], "num2")

        vehicle_nums = self.service.get_parked_vehicle_numbers_of_driver_age(20)
        self.assertEqual(vehicle_nums[0], "num3")

        vehicle_nums = self.service.get_parked_vehicle_numbers_of_driver_age(12)
        self.assertEqual(len(vehicle_nums), 0)


class TestUnparkSlotNumber(TestCase):
    def test_interface(self):
        self.dao = MagicMock()
        mockVehicle = Vehicle("mock", Driver(15))
        self.dao.unpark_vehicle_at_slot_number = MagicMock(return_value=mockVehicle)
        self.service = ParkingLotService(self.dao)
        output = self.service.empty_slot(3)
        self.dao.unpark_vehicle_at_slot_number.assert_called_once_with(3)
        self.assertEqual(output, mockVehicle)
