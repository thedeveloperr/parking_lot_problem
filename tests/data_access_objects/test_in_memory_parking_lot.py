from unittest import TestCase
from data_access_objects.in_memory_parking_lot import ParkingLotDao

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
