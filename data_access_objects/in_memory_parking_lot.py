import heapq
from models import ParkingSlot, Driver, Vehicle
from copy import deepcopy
from errors import NoneVehicleError, DuplicateVehicleError, ParkingFullError, InvalidDriverError, ParkingNotCreatedError

class ParkingLotDao():
    def __init__(self):
        self.capacity = 0
        self.empty_slots_heap = []
        self.slot_number_to_slot = {}
        self.vehicle_number_to_slot = {}
        self.age_to_vehicle_number = {}

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

    def park_vehicle_at_closest_empty_slot(self, vehicle):
        if self.capacity == 0:
            raise ParkingNotCreatedError()
        if vehicle is None:
            raise NoneVehicleError()
        if self.vehicle_number_to_slot.get(vehicle.number):
            raise DuplicateVehicleError()
        if len(self.empty_slots_heap) == 0:
            raise ParkingFullError()
        if vehicle.driver is None:
            raise InvalidDriverError()
        if vehicle.driver.age is None:
            raise InvalidDriverError()
        empty_slot = heapq.heappop(self.empty_slots_heap)
        if empty_slot is None:
            return None
        empty_slot.parked_vehicle = deepcopy(vehicle)
        self.slot_number_to_slot[empty_slot.number] = empty_slot
        self.vehicle_number_to_slot[vehicle.number] = empty_slot

        if self.age_to_vehicle_number.get(vehicle.driver.age):
            self.age_to_vehicle_number[vehicle.driver.age].append(vehicle.number)
        else:
            self.age_to_vehicle_number[vehicle.driver.age] = [vehicle.number]
        return ParkingSlot(empty_slot.number, vehicle)

    def unpark_vehicle_at_slot_number(self, slot_number):
        slot = self.slot_number_to_slot.pop(slot_number, None)
        if slot is None:
            return None
        unparked_vehicle = slot.parked_vehicle
        del self.vehicle_number_to_slot[unparked_vehicle.number]
        self.age_to_vehicle_number[unparked_vehicle.driver.age].remove(unparked_vehicle.number)
        heapq.heappush(self.empty_slots_heap, ParkingSlot(slot.number, None))
        return unparked_vehicle

    def get_slots_by_driver_age(self, age):
        return [
            self.vehicle_number_to_slot.get(number) for number in self.age_to_vehicle_number.get(age,[])
        ]

    def get_slots_by_vehicle_number(self, vehicle_number):
        return self.vehicle_number_to_slot.get(vehicle_number, None)

    def get_parked_vehicles_of_driver_age(self, age):
        return [
            self.vehicle_number_to_slot.get(number).parked_vehicle for number in self.age_to_vehicle_number.get(age,[])
        ]

