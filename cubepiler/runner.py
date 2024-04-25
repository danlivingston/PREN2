import asyncio

from loguru import logger

from cubepiler import cube_placement, motor_control, testdata

PERCENTAGES = {
    "start": 0,
    "cube scan": 10,
    "cube verification": 40,
    "cube placement calculation": 45,
    "cube placement": 50,
    "move platform": 90,
    "done": 100,
}


async def run(q=asyncio.Queue()):

    ### ! Start
    logger.info("Starting build")
    await q.put((PERCENTAGES["start"], "starting"))
    # TODO: send start api call
    # TODO: ensure reset was done before or do now; add checking function (maybe at start of reset function for simplicity)
    # await reset()

    ### ! Cube Scan
    logger.info("Scanning cubes")
    await q.put((PERCENTAGES["cube scan"], "scanning cubes"))
    # TODO: replace with real image scan
    scanned_cubes = testdata.config03
    await asyncio.sleep(5)

    ### ! Cube Verification
    logger.info("Verifying cubes")
    await q.put((PERCENTAGES["cube verification"], "verifying cubes"))
    # TODO: replace with cube verification api call
    verified_cubes = scanned_cubes
    await asyncio.sleep(1)

    ### ! Cube Placement Calculation
    logger.info("Calculating cube placement")
    await q.put((PERCENTAGES["cube placement calculation"], "calculating placement"))
    actions = await cube_placement.get_cube_placing_actions(verified_cubes)

    ### ! Cube Placement
    logger.info("Placing cubes")
    await q.put((PERCENTAGES["cube placement"], "placing cubes"))
    step = (PERCENTAGES["move platform"] - PERCENTAGES["cube placement"]) / len(actions)
    curr = 0
    # TODO
    for action in actions:
        curr += 1
        logger.info(f"Placed {curr}/{len(actions)} cubes")
        await q.put(
            (
                PERCENTAGES["cube placement"] + curr * step,
                f"placing {curr}/{len(actions)}",
            )
        )
        await motor_control.execute_action(action)

    ### ! Move Platform Down
    logger.info("Moving platform down")
    await q.put((PERCENTAGES["move platform"], "moving platform"))
    await asyncio.sleep(5)
    # TODO

    ### ! Done
    logger.info("Done with build")
    await q.put((PERCENTAGES["done"], "done"))
    # TODO: send stop api call
    logger.success("Completed build")


async def reset(q=asyncio.Queue()):
    logger.info("Resetting positions")
    await q.put((0, "resetting"))
    # await asyncio.sleep(2)
    motor_control.testFunctions()
    # motor_control.reset_platform_position()

    # raise Exception("Demo")

    await q.put((100, "ready"))

    ### ! Move platform up (async)
    ### ! Rotate shaft to starting position (async)
    ### ! await above
    # TODO
