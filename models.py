class Driver():
    def __init__(self, age):
        self.age = age

class Vehicle():
    def __init__(self, number, driver):
        self.number = number
        self.driver = driver

class ParkingSlot():
    def __init__(self, number, vehicle):
        self.number = number
        self.parked_vehicle = Vehicle
    def __lt__(self, other):
        return self.number < other.number