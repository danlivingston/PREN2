from loguru import logger


class ReferenceQuarter:
    def __init__(self, id, x_coordinate, y_coordinate, width, height, view, conf):
        self.id = id
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.width = width
        self.height = height
        self.view = view
        self.area = self.width * self.height
        self.conf = conf

    def print_info(self):
        logger.trace(f"ID: {self.id}")
        logger.trace(f"X Coordinate: {self.x_coordinate}")
        logger.trace(f"Y Coordinate: {self.y_coordinate}")
        logger.trace(f"Width: {self.width}")
        logger.trace(f"Height: {self.height}")
        logger.trace(f"View: {self.view}")
        logger.trace(f"Area: {self.area}")
        logger.trace(f"Confidence: {self.conf}")
