from ultralytics import YOLO
from .cube import Cube
from .referenceQuarter import ReferenceQuarter
import time
import json
from datetime import datetime


class CubeReconstruction:
    def __init__(self):
        self.colorModel = YOLO(
            "ApexRaspiScripts/bilderkennung/models/cube_segmentation_2.pt"
        )
        self.quarterModel = YOLO(
            "ApexRaspiScripts/bilderkennung/models/reference_segmentation_2.pt"
        )
        self.imgFrontPath = "front_frame.jpg"
        self.imgBackPath = "back_frame.jpg"

        self.cubes = {}
        self.cubesBack = {}
        self.references = {}
        self.referencesBack = {}
        self.absolute_cubes = [None] * 8
        self.tempCubes = []

        self.puffer = 0.03

        # NoCube instance
        self.noCube = Cube(None, None, None, None, None, None, None, None, None)

        self.classes = {
            0: {"color": "red", "sideNumber": 1},
            1: {"color": "yellow", "sideNumber": 1},
            2: {"color": "yellow", "sideNumber": 2},
            3: {"color": "blue", "sideNumber": 2},
            4: {"color": "blue", "sideNumber": 1},
            5: {"color": "red", "sideNumber": 2},
        }

    def run_detection(self):
        front_cube_detections = self.colorModel(self.imgFrontPath)
        referenceDetectionResultsFront = self.quarterModel(self.imgFrontPath)
        cubeDetectionResultsBack = self.colorModel(self.imgBackPath)
        referenceDetectionResultsBack = self.quarterModel(self.imgBackPath)

        self.process_detections(
            front_cube_detections,
            referenceDetectionResultsFront,
            self.cubes,
            self.references,
            view="front",
        )
        self.process_detections(
            cubeDetectionResultsBack,
            referenceDetectionResultsBack,
            self.cubesBack,
            self.referencesBack,
            view="back",
        )
        time.sleep(2)
        self.referenceQuarterFront = self.saveMostConfident(self.references)
        self.referenceQuarterBack = self.saveMostConfident(self.referencesBack)

        self.reconstructRight()
        self.reconstructLeft()
        self.reconstructRightBack()
        self.reconstructLeftBack()

        print(self.cubes_to_json(self.absolute_cubes))

    def process_detections(
        self, cube_detections, reference_detections, cube_dict, reference_dict, view
    ):
        for cdr in cube_detections:
            for i in range(len(cdr.boxes.xyxyn)):
                tempCoordinates = cdr.boxes.xyxyn[i]
                cube_dict[i] = Cube(
                    i,
                    x1=tempCoordinates[0],
                    y1=tempCoordinates[1],
                    x2=tempCoordinates[2],
                    y2=tempCoordinates[3],
                    twoSided=self.getSidesNumber(cdr.boxes.cls[i].item()),
                    view=view,
                    color=self.getColor(cdr.boxes.cls[i].item()),
                    conf=cdr.boxes.conf[i],
                )
        for rdr in reference_detections:
            for j in range(len(rdr.boxes.xyxyn)):
                tempCoordinates = rdr.boxes.xyxyn[j]
                reference_dict[j] = ReferenceQuarter(
                    j,
                    x_coordinate=tempCoordinates[0],
                    y_coordinate=tempCoordinates[1],
                    width=tempCoordinates[2],
                    height=tempCoordinates[3],
                    view=view,
                    conf=rdr.boxes.conf[j],
                )

    def getColor(self, classIndex):
        return self.classes[classIndex]["color"] if classIndex in self.classes else None

    def getSidesNumber(self, classIndex):
        return (
            self.classes[classIndex]["sideNumber"] == 2
            if classIndex in self.classes
            else False
        )

    def saveMostConfident(self, references):
        max_conf = -1
        result = None
        for reference_id, referenceQuarter in references.items():
            if referenceQuarter.conf > max_conf:
                max_conf = referenceQuarter.conf
                result = referenceQuarter
        return result

    def reconstructRight(self):
        # Cube 1 Detection
        for cube_id, cube in self.cubes.items():
            if cube.x2 > (
                self.referenceQuarterFront.x_coordinate + self.puffer
            ) and cube.y2 > (self.referenceQuarterFront.y_coordinate + self.puffer):
                self.absolute_cubes[0] = cube
                if cube.twoSided:
                    self.absolute_cubes[4] = self.noCube
                else:
                    # Cube 5 Detection
                    self.tempCubes.clear()
                    for inner_cube_id, inner_cube in self.cubes.items():
                        if (
                            abs(inner_cube.x1 - self.absolute_cubes[0].x1) <= 0.05
                            and abs(inner_cube.x2 - self.absolute_cubes[0].x2) <= 0.05
                        ):  # get cube in .05 range of x axis of cube1
                            if inner_cube != self.absolute_cubes[0]:
                                self.tempCubes.append(inner_cube)

                    self.absolute_cubes[4] = max(self.tempCubes, key=lambda obj: obj.y2)
                break

    def reconstructLeft(self):
        for cube_id, cube in self.cubes.items():
            if cube.x2 < (
                self.referenceQuarterFront.x_coordinate + self.puffer
            ) and cube.y2 > (self.referenceQuarterFront.y_coordinate + self.puffer):
                self.absolute_cubes[3] = cube
                if cube.twoSided:
                    self.absolute_cubes[7] = self.noCube
                else:
                    # Cube 8 Detection
                    self.tempCubes.clear()
                    for inner_cube_id, inner_cube in self.cubes.items():
                        if (
                            abs(inner_cube.x1 - self.absolute_cubes[3].x1) <= 0.05
                            and abs(inner_cube.x2 - self.absolute_cubes[3].x2) <= 0.05
                        ):  # get cube in .05 range of x axis of cube1
                            if inner_cube != self.absolute_cubes[3]:
                                self.tempCubes.append(inner_cube)

                    self.absolute_cubes[7] = max(self.tempCubes, key=lambda obj: obj.y2)
                break

    def reconstructRightBack(self):
        for cube_id, cube in self.cubesBack.items():
            if cube.x2 > (
                self.referenceQuarterBack.x_coordinate + self.puffer
            ) and cube.y2 > (self.referenceQuarterBack.height + self.puffer):
                self.absolute_cubes[2] = cube
                if cube.twoSided:
                    self.absolute_cubes[6] = self.noCube
                else:
                    # Cube 7 Detection
                    self.tempCubes.clear()
                    for inner_cube_id, inner_cube in self.cubesBack.items():
                        if (
                            abs(inner_cube.x1 - self.absolute_cubes[2].x1) <= 0.05
                            and abs(inner_cube.x2 - self.absolute_cubes[2].x2) <= 0.05
                        ):  # get cube in .05 range of x axis of cube1
                            if inner_cube != self.absolute_cubes[2]:
                                self.tempCubes.append(inner_cube)

                    self.absolute_cubes[6] = max(self.tempCubes, key=lambda obj: obj.y2)
                break

    def reconstructLeftBack(self):
        for cube_id, cube in self.cubesBack.items():
            if cube.x2 < (
                self.referenceQuarterBack.x_coordinate + self.puffer
            ) and cube.y2 > (self.referenceQuarterBack.height + self.puffer):
                self.absolute_cubes[1] = cube
                if cube.twoSided:
                    self.absolute_cubes[5] = self.noCube
                else:
                    # Cube 6 Detection
                    self.tempCubes.clear()
                    for inner_cube_id, inner_cube in self.cubesBack.items():
                        if (
                            abs(inner_cube.x1 - self.absolute_cubes[1].x1) <= 0.05
                            and abs(inner_cube.x2 - self.absolute_cubes[1].x2) <= 0.05
                        ):  # get cube in .05 range of x axis of cube1
                            if inner_cube != self.absolute_cubes[1]:
                                self.tempCubes.append(inner_cube)

                    self.absolute_cubes[5] = max(self.tempCubes, key=lambda obj: obj.y2)
                break

    def cubes_to_json(self, cubes):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        config = {}
        for index, cube in enumerate(cubes, start=1):
            if cube is not None:
                config[str(index)] = cube.color if cube.color is not None else ""
            else:
                config[str(index)] = ""
        return json.dumps({"time": timestamp, "config": config}, indent=2)


if __name__ == "__main__":
    CubeReconstruction().run_detection()
