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
        print(f"ID: {self.id}")
        print(f"X Coordinate: {self.x_coordinate}")
        print(f"Y Coordinate: {self.y_coordinate}")
        print(f"Width: {self.width}")
        print(f"Height: {self.height}")
        print(f"View: {self.view}")
        print(f"Area: {self.area}")
        print(f"Confidence: {self.conf}")
