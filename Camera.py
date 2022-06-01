# This is what I assume the camera class is implementing
class Camera:
    def __init__(self):
        return

    def take_image(self):
        return 0

    def calc_score(self, image): # I assume this function returns only non-negative values
        return 0

    def set_encoder(self, value):
        return

    def get_encoder(self):
        return 0

    def get_min_encoder_value(self):
        return 1

    def get_max_encoder_value(self):
        return 5000