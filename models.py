from errors import InvalidDriverError


class Driver:
    def __init__(self, age):
        if not age:
            raise InvalidDriverError()

        if age <= 0:
            raise InvalidDriverError()
        self.age = age


class Vehicle:
    def __init__(self, number, driver):
        self.number = number
        self.driver = driver


class ParkingSlot:
    def __init__(self, number, vehicle):
        self.number = number
        self.parked_vehicle = vehicle

    def __lt__(self, other):
        return self.number < other.number
