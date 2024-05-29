from loguru import logger


class Cube:
    def __init__(self, id, x1, y1, x2, y2, twoSided, view, color, conf):
        self.id = id
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.twoSided = twoSided
        self.view = view
        self.color = color
        self.conf = conf

    def print_info(self):
        logger.trace(f"ID: {self.id}")
        logger.trace(f"X Coordinate: {self.x1}")
        logger.trace(f"Y Coordinate: {self.y1}")
        logger.trace(f"X Coordinate 2: {self.x2}")
        logger.trace(f"Y Coordinate 2: {self.y2}")
        logger.trace(f"Two-Sided: {'Yes' if self.twoSided else 'No'}")
        logger.trace(f"View: {self.view}")
        logger.trace(f"Color: {self.color}")
        logger.trace(f"Confidence: {self.conf}")
