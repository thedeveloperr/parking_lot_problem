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
        pass

    def get_slot_numbers_for_driver_age(self, age):
        pass

    def get_slot_number_for_vehicle_number(self, number):
        pass

    def empty_slot(self, slot_number):
        pass

    def get_parked_vehicle_numbers_of_driver_age(self, age):
        pass

