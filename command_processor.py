from services.parking_lot_service import ParkingLotService
from data_access_objects.in_memory_parking_lot import ParkingLotDao
from errors import MalformedCommandError, ParkingFullError, DuplicateVehicleError, SlotNotPresentError
from models import ParkingSlot, Driver, Vehicle

commands_to_operation_map = {
    "Create_parking_lot": "INIT",
    "Park": "PARK",
    "Slot_number_for_car_with_number": "VEHICLE_NUM_TO_SLOT_NUM",
    "Slot_numbers_for_driver_of_age": "AGE_TO_SLOT_NUMS",
    "Vehicle_registration_number_for_driver_of_age": "AGE_TO_VEHICLE_NUMS",
    "Leave": "UNPARK",
}


class CommandProcessor:
    def __init__(self):
        dao = ParkingLotDao()
        self.parking_lot_service = ParkingLotService(dao)

    def _read_input(self, input_arr, index):
        try:
            return input_arr[index]
        except IndexError:
            raise MalformedCommandError("Missing command arguments.")

    def process(self, command):
        input_arr = command.split()
        operationCommand = self._read_input(input_arr, 0)
        operation = commands_to_operation_map.get(operationCommand)
        if operation is None:
            raise MalformedCommandError(command + " missing valid operation.")
        if operation == "INIT":
            try:
                size = int(self._read_input(input_arr, 1))
            except ValueError:
                raise MalformedCommandError(
                    "{} is not int. Slot size should be int.".format(input_arr[1])
                )
            try:
                num_slots = self.parking_lot_service.create_parking_lot_of_size(size)
            except ValueError as e:
                raise MalformedCommandError("Lot size should be positive integer")
            return "Created parking of {} slots".format(num_slots)
        elif operation == "PARK":
            if self._read_input(input_arr, 2) != "driver_age":
                raise MalformedCommandError("Missing command arguments.")
            number_plate = self._read_input(input_arr, 1)
            try:
                driver_age = self._read_input(input_arr, 3)
            except ValueError:
                raise MalformedCommandError(
                    "{} is not int. Slot size should be int.".format(input_arr[3])
                )
            driver = Driver(int(driver_age))
            vehicle_to_park = Vehicle(number_plate, driver)
            try:
                parked_slot = self.parking_lot_service.park_vehicle(vehicle_to_park)
                return 'Car with vehicle registration number "{}" has been parked at slot number {}'.format(
                    parked_slot.parked_vehicle.number, parked_slot.number
                )
            except DuplicateVehicleError as e:
                return "Vehicle with this registration number is already parked."
            except ParkingFullError as e:
                return "Cannot park more vehicles because parking is full."
        elif operation == "VEHICLE_NUM_TO_SLOT_NUM":
            vehicle_number = self._read_input(input_arr, 1)
            slot_num = self.parking_lot_service.get_slot_number_for_vehicle_number(
                vehicle_number
            )
            if slot_num is None:
                return ""
            return str(slot_num)
        elif operation == "AGE_TO_SLOT_NUMS":
            try:
                age = int(self._read_input(input_arr, 1))
            except ValueError:
                raise MalformedCommandError(
                    "{} is not int. Age should be int.".format(input_arr[1])
                )
            slot_nums = self.parking_lot_service.get_slot_numbers_for_driver_age(age)
            return ",".join([str(item) for item in slot_nums])
        elif operation == "AGE_TO_VEHICLE_NUMS":
            try:
                age = int(self._read_input(input_arr, 1))
            except ValueError:
                raise MalformedCommandError(
                    "{} is not int. Age should be int.".format(input_arr[1])
                )
            nums = self.parking_lot_service.get_parked_vehicle_numbers_of_driver_age(
                age
            )
            return ",".join([str(item) for item in nums])
        elif operation == "UNPARK":
            try:
                slot_num = int(self._read_input(input_arr, 1))
                vehicle = self.parking_lot_service.empty_slot(slot_num)
            except ValueError:
                raise MalformedCommandError(
                    "{} is not int. Slot Number should be int.".format(input_arr[1])
                )
            except SlotNotPresentError:
                return 'Slot number not present.'
            if vehicle is None:
                return "Slot already vacant"
            return 'Slot number {} vacated, the car with vehicle registration number "{}" left the space, the driver of the car was of age {}'.format(
                slot_num, vehicle.number, vehicle.driver.age
            )
