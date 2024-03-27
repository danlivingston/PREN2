import asyncio

from loguru import logger

from cubepiler import cube_placement, testdata, motor_control


PERCENTAGES = {
    "start": 0,
    "cube scan": 35,
    "cube verification": 40,
    "cube placement calculation": 45,
    "cube placement": 50,
    "move platform": 90,
    "done": 100,
}


async def run(q=asyncio.Queue()):

    ### ! Start
    await q.put((PERCENTAGES["start"], "starting"))
    # TODO: send start api signal
    # TODO: ensure reset was done before or do now
    await reset()

    ### ! Cube Scan
    await q.put((PERCENTAGES["cube scan"], "scanning cubes"))
    # TODO: replace with real image scan
    scanned_cubes = testdata.config03
    await asyncio.sleep(10)

    ### ! Cube Verification
    await q.put((PERCENTAGES["cube verification"], "verifying cubes"))
    # TODO: replace with cube verification
    verified_cubes = scanned_cubes
    await asyncio.sleep(1)

    ### ! Cube Placement Calculation
    await q.put((PERCENTAGES["cube placement calculation"], "calculating placement"))
    actions = await cube_placement.get_cube_placing_actions(verified_cubes)

    ### ! Cube Placement
    await q.put((PERCENTAGES["cube placement"], "placing cubes"))
    step = (PERCENTAGES["move platform"] - PERCENTAGES["cube placement"]) / len(actions)
    curr = 0
    # TODO
    for action in actions:
        curr += 1
        await q.put(
            (
                PERCENTAGES["cube placement"] + curr * step,
                f"placing {curr}/{len(actions)}",
            )
        )
        await motor_control.execute_action(action)

    ### ! Move Platform Down
    await q.put((PERCENTAGES["move platform"], "moving platform"))
    await asyncio.sleep(5)
    # TODO

    ### ! Done
    await q.put((PERCENTAGES["done"], "done"))
    # TODO: send stop api signal


async def reset(q=asyncio.Queue()):
    await q.put((0, "resetting"))
    await asyncio.sleep(2)
    await q.put((100, "ready"))
