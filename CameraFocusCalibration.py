import Unit


class CameraFocusCalibration(Unit.CalibrationProcedure):

    def __init__(self, unit: Unit.Unit):
        super(CameraFocusCalibration, self).__init__()
        self.camera = unit.camera

    def calibrate(self):
        self.unit.calibrated_properties.append("Camera Focus")
        return
