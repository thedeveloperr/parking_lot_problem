class MalformedCommandError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class ParkingNotCreatedError(Exception):
    pass


class ParkingFullError(Exception):
    pass


class NoneVehicleError(Exception):
    pass


class InvalidDriverError(Exception):
    pass


class DuplicateVehicleError(Exception):
    pass
