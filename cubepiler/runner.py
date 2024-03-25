from loguru import logger

import cubepiler.cube_placement as cube_placement
import cubepiler.testdata as testdata


async def kill():
    pass


async def start():
    logger.info("starting cube rebuild")

    scanned_cubes = testdata.config01
    cube_placement.place_cubes(scanned_cubes)

    logger.success("successfully executed cube rebuild")


if __name__ == "__main__":
    start()
