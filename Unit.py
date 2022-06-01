import Engine


# The machine itself
class Unit:
    def __init__(self, engine: Engine.Engine):
        self.engine = engine
        self.devices = []

    def reset(self):
        self.engine.reset()

    def add_device(self, device):
        self.devices.append(device)

    def get_position(self):
        return self._engine_position_to_unit_position(self.engine.get_position())

    def is_valid_position_absolute(self, pos):
        return self.engine.is_valid_position(Unit._unit_position_to_engine_position(pos))

    def is_valid_position_relative(self, pos):
        return self.is_valid_position_absolute(self.get_position()+pos)

    # moves the unit up or down to the exact position specified
    def move_absolute(self, pos):
        if not self.is_valid_position_absolute(pos):
            raise Exception("Position provided is not a valid position!")
        self.engine.move(self._unit_position_to_engine_position(pos))

    # moves the unit up or down relative to the current position of the unit
    def move_relative(self, pos):
        if not self.is_valid_position_relative(pos):
            raise Exception("Position provided is not a valid position!")
        self.move_absolute(self.get_position()+pos)

    # static methods
    @staticmethod
    def _unit_position_to_engine_position(pos):
        # Apply whatever transformation is needed to convert the position from unit units to the engine units
        return pos

    @staticmethod
    def _engine_position_to_unit_position(pos):
        # Apply whatever transformation is needed to convert the position from engine units to the unit units
        return pos


# For each device that fits on the unit (camera, sensors, ect.) we will create an appropriate class that inherits from this
class UnitDevice:
    def __init__(self, unit: Unit):
        self.unit = unit
        self.calibrated_properties = []


# For each property of a UnitDevice that should be calibrated we will create a procedure that inherits from this class
class CalibrationProcedure:
    def __init__(self, device: UnitDevice):
        self.device = device
        return

    def calibrate(self):
        self.device.calibrated_properties.append(self.__class__.__name__)
