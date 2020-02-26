from errors import ParkingFullError

class ParkingLotService():
    def __init__(self, dao):
        self.dao = dao

    def create_parking_lot_of_size(self, size):
        if (not isinstance(size, int)):
            raise ValueError("Lot Size should be integer")
        if (size <= 0):
            raise ValueError("Lot Size should be greater than 0.")
        self.dao.create_slots(size)
        return size

    def park_vehicle(self, vehicle):
        parked_slot = self.dao.park_vehicle_at_closest_empty_slot(vehicle);
        return parked_slot

    def get_slot_numbers_for_driver_age(self, age):
        return [ slot.number for slot in self.dao.get_slots_by_driver_age(age) ]

    def get_slot_number_for_vehicle_number(self, number):
        slot = self.dao.get_slots_by_vehicle_number(number)
        if slot is None:
            return None
        return slot.number

    def empty_slot(self, slot_number):
        pass

    def get_parked_vehicle_numbers_of_driver_age(self, age):
        return [ vehicle.number for vehicle in self.dao.get_parked_vehicles_of_driver_age(age) ]

