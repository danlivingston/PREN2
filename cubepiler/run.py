import cube_placement
import testdata
from loguru import logger
from multiprocessing import Queue


@logger.catch()
def start(q):
    logger.info("starting cube rebuild")

    scanned_cubes = testdata.config01
    cube_placement.place_cubes(scanned_cubes)

    logger.success("successfully executed cube rebuild")


if __name__ == "__main__":
    start()
