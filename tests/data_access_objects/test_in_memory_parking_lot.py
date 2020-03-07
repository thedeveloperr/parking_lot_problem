from unittest import TestCase
from data_access_objects.in_memory_parking_lot import ParkingLotDao
from models import ParkingSlot, Driver, Vehicle
from errors import (
    NoneVehicleError,
    DuplicateVehicleError,
    ParkingFullError,
    InvalidDriverError,
    ParkingNotCreatedError,
    SlotNotPresentError
)


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
            v = Vehicle("rndomplate", driver)
            parked_slot = self.dao.park_vehicle_at_closest_empty_slot(v)

    def test_with_invalid_driver(self):
        self.assertTrue(self.dao.create_slots(3))
        with self.assertRaises(InvalidDriverError):
            driver = None
            v = Vehicle("rndomplate", driver)
            parked_slot = self.dao.park_vehicle_at_closest_empty_slot(v)
        with self.assertRaises(InvalidDriverError):
            driver = Driver(-23)
        with self.assertRaises(InvalidDriverError):
            driver = Driver(None)
            v = Vehicle("rndomplate", driver)
            parked_slot = self.dao.park_vehicle_at_closest_empty_slot(v)

    def test_with_none_vehicle(self):
        self.assertTrue(self.dao.create_slots(3))
        self.assertEqual(self.dao.capacity, 3)
        self.assertEqual(len(self.dao.empty_slots_heap), 3)
        self.assertEqual(len(self.dao.slot_number_to_slot), 3)
        with self.assertRaises(NoneVehicleError):
            parked_slot = self.dao.park_vehicle_at_closest_empty_slot(None)
        self.assertEqual(len(self.dao.empty_slots_heap), 3)

    def test_with_unpark(self):
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
        self.dao.unpark_vehicle_at_slot_number(3)
        self.dao.unpark_vehicle_at_slot_number(1)
        parked_slot = self.dao.park_vehicle_at_closest_empty_slot(vehicle4)
        self.assertEqual(len(self.dao.empty_slots_heap), 1)
        self.assertEqual(parked_slot.number, 1)


class TestUnparkSlotNumber(TestCase):
    def setUp(self):
        self.dao = ParkingLotDao()
        self.dao.create_slots(3)
        d1 = Driver(18)
        v1 = Vehicle("num1", d1)
        self.dao.park_vehicle_at_closest_empty_slot(v1)
        d2 = Driver(18)
        v2 = Vehicle("num2", d2)
        self.dao.park_vehicle_at_closest_empty_slot(v2)

        d3 = Driver(20)
        v3 = Vehicle("num3", d3)
        self.dao.park_vehicle_at_closest_empty_slot(v3)

    def test_unpark(self):
        unparked_vehicle = self.dao.unpark_vehicle_at_slot_number(2)
        self.assertEqual(unparked_vehicle.number, "num2")
        self.assertEqual(unparked_vehicle.driver.age, 18)

        unparked_vehicle = self.dao.unpark_vehicle_at_slot_number(1)
        self.assertEqual(unparked_vehicle.number, "num1")
        self.assertEqual(unparked_vehicle.driver.age, 18)

        unparked_vehicle = self.dao.unpark_vehicle_at_slot_number(3)
        self.assertEqual(unparked_vehicle.number, "num3")
        self.assertEqual(unparked_vehicle.driver.age, 20)

        unparked_vehicle = self.dao.unpark_vehicle_at_slot_number(3)
        self.assertEqual(unparked_vehicle, None)

        unparked_vehicle = self.dao.unpark_vehicle_at_slot_number(2)
        self.assertEqual(unparked_vehicle, None)

        unparked_vehicle = self.dao.unpark_vehicle_at_slot_number(1)
        self.assertEqual(unparked_vehicle, None)

        with self.assertRaises(SlotNotPresentError):
            unparked_vehicle = self.dao.unpark_vehicle_at_slot_number(4)
            self.assertEqual(unparked_vehicle, None)

        with self.assertRaises(SlotNotPresentError):
            unparked_vehicle = self.dao.unpark_vehicle_at_slot_number(-2)
            self.assertEqual(unparked_vehicle, None)

class IntegrationTestGovtRegulationQueries(TestCase):
    def setUp(self):
        self.dao = ParkingLotDao()
        self.dao.create_slots(3)
        d1 = Driver(18)
        v1 = Vehicle("num1", d1)
        self.dao.park_vehicle_at_closest_empty_slot(v1)
        d2 = Driver(18)
        v2 = Vehicle("num2", d2)
        self.dao.park_vehicle_at_closest_empty_slot(v2)

        d3 = Driver(20)
        v3 = Vehicle("num3", d3)
        self.dao.park_vehicle_at_closest_empty_slot(v3)

    def test_vehicle_number_to_slot(self):
        slot = self.dao.get_slots_by_vehicle_number("num1")
        self.assertEqual(slot.parked_vehicle.number, "num1")
        self.assertEqual(slot.number, 1)

        slot = self.dao.get_slots_by_vehicle_number("num3")
        self.assertEqual(slot.parked_vehicle.number, "num3")
        self.assertEqual(slot.number, 3)
        slot = self.dao.get_slots_by_vehicle_number("num2")
        self.assertEqual(slot.parked_vehicle.number, "num2")
        self.assertEqual(slot.number, 2)

        slot = self.dao.get_slots_by_vehicle_number("nonparkednumber")
        self.assertEqual(slot, None)

    def test_slot_from_age(self):
        slots = self.dao.get_slots_by_driver_age(18)
        self.assertEqual(slots[0].number, 1)
        self.assertEqual(slots[1].number, 2)

        slots = self.dao.get_slots_by_driver_age(20)
        self.assertEqual(slots[0].number, 3)

        slots = self.dao.get_slots_by_driver_age(14)
        self.assertEqual(len(slots), 0)

    def test_parked_vehicle_from_age(self):
        vehicles = self.dao.get_parked_vehicles_of_driver_age(18)
        self.assertEqual(vehicles[0].number, "num1")
        self.assertEqual(vehicles[1].number, "num2")

        vehicles = self.dao.get_parked_vehicles_of_driver_age(20)
        self.assertEqual(vehicles[0].number, "num3")

        vehicles = self.dao.get_parked_vehicles_of_driver_age(14)
        self.assertEqual(len(vehicles), 0)

    def test_with_unpark_commands(self):
        unparked_vehicle = self.dao.unpark_vehicle_at_slot_number(1)
        self.assertEqual(unparked_vehicle.number, "num1")
        self.assertEqual(unparked_vehicle.driver.age, 18)

        slots = self.dao.get_slots_by_driver_age(18)
        vehicles = self.dao.get_parked_vehicles_of_driver_age(18)
        self.assertEqual(slots[0].number, 2)
        self.assertEqual(vehicles[0].number, "num2")
        slot = self.dao.get_slots_by_vehicle_number("num1")
        self.assertEqual(slot, None)

        slots = self.dao.get_slots_by_driver_age(20)
        vehicles = self.dao.get_parked_vehicles_of_driver_age(18)

        self.dao.unpark_vehicle_at_slot_number(2)
        slots = self.dao.get_slots_by_driver_age(18)
        self.assertEqual(len(slots), 0)

        unparked_vehicle = self.dao.unpark_vehicle_at_slot_number(3)
        slots = self.dao.get_slots_by_driver_age(20)
        self.assertEqual(len(slots), 0)
        unparked_vehicle = self.dao.unpark_vehicle_at_slot_number(3)
        self.assertEqual(unparked_vehicle, None)
