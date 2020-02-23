import heapq
from models import ParkingSlot

class ParkingLotDao():
    def __init__(self):
        self.capacity = 0
        self.empty_slots_heap = []
        self.occupied_slots_number_set = set()
        self.slot_number_to_slot = {}

    def create_slots(self, number):
        if not isinstance(number, int):
            return False
        if number < 0:
            return False
        self.capacity = number
        for i in range(1, number+1):
            slot = ParkingSlot(i, None)
            self.empty_slots_heap.append(slot)
            self.slot_number_to_slot[i] = slot
        heapq.heapify(self.empty_slots_heap)
        return True

    def get_closest_empty_slot_number(self):
        pass

    def park_vehicle_at_slot_number(self, vehicle, slot_number):
        pass

    def unpark_vehicle_at_slot_number(self,slot_number):
        pass

    def get_slots_by_driver_age(self, age):
        pass

    def get_slots_by_vehicle_number(self, vehicle_number):
        pass

    def get_parked_vehicles_of_driver_age(self, age):
        pass

