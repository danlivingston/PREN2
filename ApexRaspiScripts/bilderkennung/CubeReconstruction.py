from ultralytics import YOLO
from ApexRaspiScripts.bilderkennung.cube import Cube
from ApexRaspiScripts.bilderkennung.referenceQuarter import ReferenceQuarter
import time
from datetime import datetime
import json



class CubeReconstruction:
    def __init__(self):
        self.colorModel = YOLO('ApexRaspiScripts/bilderkennung/models/cube_segmentation_2.pt')
        self.quarterModel = YOLO('ApexRaspiScripts/bilderkennung/models/reference_segmentation_2.pt')
        self.imgFrontPath = 'front_frame.jpg'
        self.imgBackPath = 'back_frame.jpg'
        self.imgWarmup = 'warmup.jpg'
        self.puffer = 0.03



        self.classes = {
            0: {"color": "red", "sideNumber": 1},
            1: {"color": "yellow", "sideNumber": 1},
            2: {"color": "yellow", "sideNumber": 2},
            3: {"color": "blue", "sideNumber": 2},
            4: {"color": "blue", "sideNumber": 1},
            5: {"color": "red", "sideNumber": 2}
        }
    def warmupModels(self):
        warmupresultCube = self.colorModel(self.imgWarmup)
        warmupresultReference = self.quarterModel(self.imgWarmup)
        
    def runModels(self):
        self.cubeDetectionResultsFront = self.colorModel(self.imgFrontPath)
        self.referenceDetectionResultsFront = self.quarterModel(self.imgFrontPath)
        self.cubeDetectionResultsBack = self.colorModel(self.imgBackPath)
        self.referenceDetectionResultsBack = self.quarterModel(self.imgBackPath)

        self.referenceQuarterFront = None
        self.referenceQuarterBack = None
        self.absolute_positions = [None] * 8
        self.cubes = {}
        self.cubesBack = {}
        self.absolute_cubes = [None] * 8
        self.tempCubes = []
        self.references = {}
        self.referencesBack = {}
        time.sleep(2)

    def getColor(self, classIndex):
        if classIndex in self.classes:
            return self.classes[classIndex]["color"]

    def getSidesNumber(self, classIndex):
        if classIndex in self.classes:
            if self.classes[classIndex]["sideNumber"] == 2:
                return True
        else:
            return False

    def saveHighestScoredQuarter(self, references):
        max_conf = -1
        best_reference = None
        for reference_id, referenceQuarter in references.items():
            if referenceQuarter.conf > max_conf:
                max_conf = referenceQuarter.conf
                best_reference = referenceQuarter
        return best_reference

    def processDetections(self):
        for cdrf in self.cubeDetectionResultsFront:
            for i in range(len(cdrf.boxes.xyxyn)):
                tempCoordinates = cdrf.boxes.xyxyn[i]
                self.cubes[i] = Cube(i, x1=tempCoordinates[0], y1=tempCoordinates[1], x2=tempCoordinates[2],
                                     y2=tempCoordinates[3],
                                     twoSided=self.getSidesNumber(cdrf.boxes.cls[i].item()), view="front",
                                     color=self.getColor(cdrf.boxes.cls[i].item()), conf=cdrf.boxes.conf[i])

        for rdrf in self.referenceDetectionResultsFront:
            for j in range(len(rdrf.boxes.xyxyn)):
                tempCoordinates = rdrf.boxes.xyxyn[j]
                self.references[j] = ReferenceQuarter(j, x_coordinate=tempCoordinates[0],
                                                      y_coordinate=tempCoordinates[1],
                                                      width=tempCoordinates[2], height=tempCoordinates[3], view="front",
                                                      conf=rdrf.boxes.conf[j])

        for cdrb in self.cubeDetectionResultsBack:
            for i in range(len(cdrb.boxes.xyxyn)):
                tempCoordinates = cdrb.boxes.xyxyn[i]
                self.cubesBack[i] = Cube(i, x1=tempCoordinates[0], y1=tempCoordinates[1], x2=tempCoordinates[2],
                                         y2=tempCoordinates[3],
                                         twoSided=self.getSidesNumber(cdrb.boxes.cls[i].item()), view="back",
                                         color=self.getColor(cdrb.boxes.cls[i].item()), conf=cdrb.boxes.conf[i])

        for rdrb in self.referenceDetectionResultsBack:
            for j in range(len(rdrb.boxes.xyxyn)):
                tempCoordinates = rdrb.boxes.xyxyn[j]
                self.referencesBack[j] = ReferenceQuarter(j, x_coordinate=tempCoordinates[0],
                                                          y_coordinate=tempCoordinates[1],
                                                          width=tempCoordinates[2], height=tempCoordinates[3],
                                                          view="back",
                                                          conf=rdrb.boxes.conf[j])

        self.referenceQuarterFront = self.saveHighestScoredQuarter(self.references)
        self.referenceQuarterBack = self.saveHighestScoredQuarter(self.referencesBack)
        self.referenceQuarterFront.print_info()


    def reconstructRight(self):
        noCube = Cube(1000, -1, -1, -1, -1, False, 'front', 'none', '-100')
        for cube_id, cube in self.cubes.items():
            if cube.x2 > (self.referenceQuarterFront.x_coordinate + self.puffer) and cube.y2 > (
                    self.referenceQuarterFront.y_coordinate + self.puffer):
                self.absolute_positions[0] = cube.color
                self.absolute_cubes[0] = cube
                if cube.twoSided:
                    self.absolute_positions[4] = 'empty'
                    self.absolute_cubes[4] = noCube
                else:
                    self.tempCubes.clear()
                    for inner_cube_id, inner_cube in self.cubes.items():
                        if abs(inner_cube.x1 - self.absolute_cubes[0].x1) <= 0.05 and abs(
                                inner_cube.x2 - self.absolute_cubes[0].x2) <= 0.05:
                            if inner_cube != self.absolute_cubes[0]:
                                self.tempCubes.append(inner_cube)

                    self.absolute_cubes[4] = max(self.tempCubes, key=lambda obj: obj.y2)
                    self.absolute_positions[4] = self.absolute_cubes[4].color
                break
            else:
                self.absolute_positions[0] = 'empty'
                self.absolute_positions[4] = 'empty'
                self.absolute_cubes[0] = noCube
                self.absolute_cubes[4] = noCube

    def reconstructLeft(self):
        noCube = Cube(1000, -1, -1, -1, -1, False, 'front', 'none', '-100')
        for cube_id, cube in self.cubes.items():
            if cube.x2 < (self.referenceQuarterFront.x_coordinate + self.puffer) and cube.y2 > (
                    self.referenceQuarterFront.y_coordinate + self.puffer):
                self.absolute_positions[3] = cube.color
                self.absolute_cubes[3] = cube
                if cube.twoSided:
                    self.absolute_positions[7] = 'empty'
                    self.absolute_cubes[7] = noCube
                else:
                    self.tempCubes.clear()
                    for inner_cube_id, inner_cube in self.cubes.items():
                        if abs(inner_cube.x1 - self.absolute_cubes[3].x1) <= 0.05 and abs(
                                inner_cube.x2 - self.absolute_cubes[3].x2) <= 0.05:
                            if inner_cube != self.absolute_cubes[3]:
                                self.tempCubes.append(inner_cube)

                    self.absolute_cubes[7] = max(self.tempCubes, key=lambda obj: obj.y2)
                    self.absolute_positions[7] = self.absolute_cubes[7].color
                break

    def reconstructRightBack(self):
        noCube = Cube(1000, -1, -1, -1, -1, False, 'back', 'none', '-100')
        for cube_id, cube in self.cubesBack.items():
            if cube.x2 > (self.referenceQuarterFront.x_coordinate + self.puffer) and cube.y2 > (
                    self.referenceQuarterBack.height + self.puffer):
                self.absolute_positions[2] = cube.color
                self.absolute_cubes[2] = cube
                if cube.twoSided:
                    self.absolute_positions[6] = 'empty'
                    self.absolute_cubes[6] = noCube
                else:
                    self.tempCubes.clear()
                    for inner_cube_id, inner_cube in self.cubesBack.items():
                        if abs(inner_cube.x1 - self.absolute_cubes[2].x1) <= 0.05 and abs(
                                inner_cube.x2 - self.absolute_cubes[2].x2) <= 0.05:
                            if inner_cube != self.absolute_cubes[2]:
                                self.tempCubes.append(inner_cube)

                    self.absolute_cubes[6] = max(self.tempCubes, key=lambda obj: obj.y2)
                    self.absolute_positions[6] = self.absolute_cubes[6].color
                break

    def reconstructLeftBack(self):
        noCube = Cube(1000, -1, -1, -1, -1, False, 'back', 'none', '-100')
        for cube_id, cube in self.cubesBack.items():
            if cube.x2 < (self.referenceQuarterFront.x_coordinate + self.puffer) and cube.y2 > (
                    self.referenceQuarterBack.height + self.puffer):
                self.absolute_positions[1] = cube.color
                self.absolute_cubes[1] = cube
                if cube.twoSided:
                    self.absolute_positions[5] = 'empty'
                    self.absolute_cubes[5] = noCube
                else:
                    self.tempCubes.clear()
                    for inner_cube_id, inner_cube in self.cubesBack.items():
                        if abs(inner_cube.x1 - self.absolute_cubes[1].x1) <= 0.05 and abs(
                                inner_cube.x2 - self.absolute_cubes[1].x2) <= 0.05:
                            if inner_cube != self.absolute_cubes[1]:
                                self.tempCubes.append(inner_cube)

                    self.absolute_cubes[5] = max(self.tempCubes, key=lambda obj: obj.y2)
                    self.absolute_positions[5] = self.absolute_cubes[5].color
                break

    def cubes_to_json(self, cubes):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        config = {}
        for index, cube in enumerate(cubes, start=1):
            if cube is not None and cube.color != "none":
                config[str(index)] = cube.color if cube.color is not None else ""
            else:
                config[str(index)] = ""
        return json.dumps({"time": timestamp, "config": config}, indent=2)

    def run_detection(self):
        self.runModels()
        self.processDetections()
        self.reconstructRight()
        self.reconstructLeft()
        self.reconstructRightBack()
        self.reconstructLeftBack()
        print(self.cubes_to_json(self.absolute_cubes))



if __name__ == "__main__":
    reconstruction = CubeReconstruction()
    reconstruction.warmupModels()
    reconstruction.run_detection()
