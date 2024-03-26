from loguru import logger
import asyncio

import cubepiler.cube_placement as cube_placement
import cubepiler.testdata as testdata


async def run(q=asyncio.Queue()):
    logger.info("starting cube rebuild")
    await q.put((0, "starting"))

    scan_complete = False
    scan_prog_faker = 0

    while not scan_complete and scan_prog_faker < 50:
        scan_prog_faker += 10
        await q.put((scan_prog_faker, "scanning cubes"))
        await asyncio.sleep(1)

    scanned_cubes = testdata.config01

    await cube_placement.place_cubes(scanned_cubes, q)

    await q.put((100, "done"))

    logger.success("successfully executed cube rebuild")


async def reset(q=asyncio.Queue()):
    await q.put((0, "resetting"))
    await q.put((100, "ready"))
