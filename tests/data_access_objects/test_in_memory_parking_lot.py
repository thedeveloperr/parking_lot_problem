from unittest import TestCase
from data_access_objects.in_memory_parking_lot import ParkingLotDao
from models import ParkingSlot, Driver, Vehicle
from errors import NoneVehicleError, DuplicateVehicleError, ParkingFullError, InvalidDriverError, ParkingNotCreatedError


class UnitTestCreateslotsMethod(TestCase):
    def setUp(self):
        self.dao = ParkingLotDao()
        self.assertEqual(self.dao.capacity, 0)
        self.assertEqual(len(self.dao.empty_slots_heap), 0)
        self.assertEqual(len(self.dao.slot_number_to_slot), 0)

    def test_with_valid_size(self):
        self.assertTrue(self.dao.create_slots(3))
        self.assertEqual(self.dao.capacity, 3)
        self.assertEqual(len(self.dao.empty_slots_heap), 3)
        self.assertEqual(len(self.dao.slot_number_to_slot), 3)

    def test_with_invalid_size(self):
        self.assertFalse(self.dao.create_slots(-3))
        self.assertEqual(self.dao.capacity, 0)
        self.assertEqual(len(self.dao.empty_slots_heap), 0)
        self.assertEqual(len(self.dao.slot_number_to_slot), 0)

        self.assertFalse(self.dao.create_slots(3.2))
        self.assertEqual(self.dao.capacity, 0)
        self.assertEqual(len(self.dao.empty_slots_heap), 0)
        self.assertEqual(len(self.dao.slot_number_to_slot), 0)

        self.assertFalse(self.dao.create_slots("3"))
        self.assertEqual(self.dao.capacity, 0)
        self.assertEqual(len(self.dao.empty_slots_heap), 0)
        self.assertEqual(len(self.dao.slot_number_to_slot), 0)

class TestParkClosest(TestCase):
    def setUp(self):
        self.dao = ParkingLotDao()
        self.assertEqual(self.dao.capacity, 0)
        self.assertEqual(len(self.dao.empty_slots_heap), 0)
        self.assertEqual(len(self.dao.slot_number_to_slot), 0)

    def test_valid_vehicle_parking(self):
        self.assertTrue(self.dao.create_slots(3))
        self.assertEqual(self.dao.capacity, 3)
        self.assertEqual(len(self.dao.empty_slots_heap), 3)
        self.assertEqual(len(self.dao.slot_number_to_slot), 3)
        driver = Driver(22)
        vehicle1 = Vehicle("pb08-11-22-random", driver)
        parked_slot = self.dao.park_vehicle_at_closest_empty_slot(vehicle1)
        self.assertEqual(len(self.dao.empty_slots_heap), 2)
        self.assertEqual(parked_slot.number, 1)

        driver = Driver(23)
        vehicle1clone = Vehicle("pb08-11-22-random", driver)
        with self.assertRaises(DuplicateVehicleError):
            parked_slot = self.dao.park_vehicle_at_closest_empty_slot(vehicle1clone)
            self.assertEqual(len(self.dao.empty_slots_heap), 2)

        driver = Driver(23)
        vehicle2 = Vehicle("pb08-11-23-random", driver)
        parked_slot = self.dao.park_vehicle_at_closest_empty_slot(vehicle2)
        self.assertEqual(len(self.dao.empty_slots_heap), 1)
        self.assertEqual(parked_slot.number, 2)

        driver = Driver(23)
        vehicle3 = Vehicle("pb08-11-33-random", driver)
        parked_slot = self.dao.park_vehicle_at_closest_empty_slot(vehicle3)
        self.assertEqual(len(self.dao.empty_slots_heap), 0)
        self.assertEqual(parked_slot.number, 3)

        driver = Driver(23)
        vehicle4 = Vehicle("pb08-11-34-random", driver)
        with self.assertRaises(ParkingFullError):
            parked_slot = self.dao.park_vehicle_at_closest_empty_slot(vehicle4)
            self.assertEqual(len(self.dao.empty_slots_heap), 0)

    def test_with_not_created_parking_slot(self):
        with self.assertRaises(ParkingNotCreatedError):
            driver = Driver(18)
            v =Vehicle("rndomplate", driver)
            parked_slot = self.dao.park_vehicle_at_closest_empty_slot(v)

    def test_with_invalid_driver(self):
        self.assertTrue(self.dao.create_slots(3))
        with self.assertRaises(InvalidDriverError):
            driver = None
            v =Vehicle("rndomplate", driver)
            parked_slot = self.dao.park_vehicle_at_closest_empty_slot(v)
        with self.assertRaises(InvalidDriverError):
            driver = Driver(None)
            v =Vehicle("rndomplate", driver)
            parked_slot = self.dao.park_vehicle_at_closest_empty_slot(v)

    def test_with_none_vehicle(self):
        self.assertTrue(self.dao.create_slots(3))
        self.assertEqual(self.dao.capacity, 3)
        self.assertEqual(len(self.dao.empty_slots_heap), 3)
        self.assertEqual(len(self.dao.slot_number_to_slot), 3)
        with self.assertRaises(NoneVehicleError):
            parked_slot = self.dao.park_vehicle_at_closest_empty_slot(None)
        self.assertEqual(len(self.dao.empty_slots_heap), 3)

