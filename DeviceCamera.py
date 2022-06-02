from numpy.polynomial import polynomial
import Unit


class DeviceCamera(Unit.UnitDevice):

    def __init__(self, unit, camera):
        super().__init__(unit)
        self.camera = camera
        self.position_to_encoder_function = None


class CameraFocusCalibration(Unit.CalibrationProcedure):
    deg = 5  # The degree of the polynom to be fitted as the position-encoder function, optimal value needs to be tested
    stage_position_difference = 50  # The difference between each tested position of the stage.

    # Lower Value = more tested positions = Better fitted function. Optimal value needs to be tested.

    def __init__(self, device: DeviceCamera):
        super().__init__(device)

    def calibrate(self):
        positions = []
        optimal_encoder_values = []
        self.device.unit.reset()
        while self.device.unit.is_valid_position_relative(-50):
            self.device.unit.move_relative(-50)

        encoder_value = self.device.camera.get_min_encoder_value()

        positions.append(self.device.unit.get_position())
        encoder_value = self._find_optimal_encoder_value(encoder_value)
        optimal_encoder_values.append(encoder_value)

        while self.device.unit.is_valid_position_relative(50):
            self.device.unit.move_relative(50)
            positions.append(self.device.unit.get_position())
            encoder_value = self._find_optimal_encoder_value(encoder_value)
            optimal_encoder_values.append(encoder_value)

        self.device.position_to_encoder_function = polynomial.Polynomial.fit(positions, optimal_encoder_values, self.deg)
        self.device.calibrated_properties.append("Camera Focus")
        return self.device.position_to_encoder_function




    def _get_current_image_score(self):
        return self.device.camera.calc_score(self.device.camera.take_image())

    # Finds the optimal encoding value for the current position.
    # Since the focus of the camera can be thought of as a function with a single peak, we only need to find the spot where by going in each direction we are deceasing the focus.
    # If starting_encoding_value isn't set then the search starts from the minimum encoding position (going upwards), otherwise it starts from the set value
    def _find_optimal_encoder_value(self, starting_encoding_value=None):
        if starting_encoding_value is None:
            starting_encoding_value = self.device.camera.get_min_encoder_value()

        curr_score = -1
        curr_encoding_value = -1
        prev_score = -1
        prev_encoding_value = -1
        for curr_encoding_value in range(starting_encoding_value, self.device.camera.get_max_encoder_value() + 1):
            self.device.camera.set_encoder(curr_encoding_value)
            curr_score = self._get_current_image_score()
            if prev_score > curr_score:
                # We found the peak
                curr_encoding_value = prev_encoding_value
                curr_score = prev_score
                break
            prev_encoding_value = curr_encoding_value
            prev_score = curr_score

        # Sanity check
        if curr_encoding_value == -1 or curr_score == -1:
            raise "Optimal encoder-value search broke!"
        if curr_encoding_value > self.device.camera.get_min_encoder_value():
            self.device.camera.set_encoder(curr_encoding_value - 1)
            if self._get_current_image_score() > curr_score:
                raise "Starting encoding value is too high to find the optimal value"

        return curr_encoding_value
