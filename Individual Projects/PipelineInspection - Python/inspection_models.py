class RectangleBox:
    """
    Class that defines a rectangular box that might contain an anomaly in pipeline inspection
    """
    def __init__(self, longitudinal_position, circumferential_position, length, width):
        self.longitudinal_position = longitudinal_position       # initial position of the box in the longitudinal axis - in meters
        self.circumferential_position = circumferential_position # initial position of the box in the circumferential axis - in degrees, counter clockwise
        self.length = length                                     # length of the box along the longitudinal axis - in meters
        self.width = width                                       # width of the box in degrees along the circumferential axis

    def __str__(self):
        return "Longitudinal Position: %s, Circumferential Position: %s, Length: %s, Width: %s" % \
               (self.longitudinal_position, self.circumferential_position, self.length, self.width)

