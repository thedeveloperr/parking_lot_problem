from services.parking_lot_service import ParkingLotService
from data_access_objects.in_memory_parking_lot import ParkingLotDao
from errors import MalformedCommandError

commands_to_operation_map = {
    "Create_parking_lot": "INIT",
}

class CommandProcessor():
    def __init__(self):
        dao = ParkingLotDao()
        self.parkingLotService = ParkingLotService(dao)

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
                raise MalformedCommandError("{} is not int. Slot size should be int.".format(input_arr[1]))
            try:
                num_slots = self.parkingLotService.create_parking_lot_of_size(size)
            except ValueError as e:
                raise MalformedCommandError("Lot size should be positive integer")
            return "Created parking of {} slots".format(num_slots)
