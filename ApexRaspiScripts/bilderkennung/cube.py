class Cube:
    def __init__(self, id, x1, y1,x2, y2, twoSided, view, color, conf):
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
        print(f"ID: {self.id}")
        print(f"X Coordinate: {self.x1}")
        print(f"Y Coordinate: {self.y1}")
        print(f"X Coordinate 2: {self.x2}")
        print(f"Y Coordinate 2: {self.y2}")
        print(f"Two-Sided: {'Yes' if self.twoSided else 'No'}")
        print(f"View: {self.view}")
        print(f"Color: {self.color}")
        print(f"Confidence: {self.conf}")
