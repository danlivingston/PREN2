import asyncio

from datetime import datetime

from loguru import logger

from ApexRaspiScripts.bilderkennung.getTwoSidesStream import CubeFaceDetector


from ApexRaspiScripts.bilderkennung.CubeReconstruction import CubeReconstruction
from cubepiler import (
    api,
    cube_placement,
    measurelib,
    motor_control,
    sound,
    testdata,
    configure_logger,
)

cube_reconstruction = CubeReconstruction()

is_reset = False

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
    ### ! Reset
    global is_reset
    if not is_reset:
        await reset()
    is_reset = False

    ### ! Start
    # sound.sound_start(600)
    measurelib.send_refresh_command()
    startTime = datetime.now()
    logger.info("Starting build")
    await q.put((PERCENTAGES["start"], "starting"))
    api.send_start_signal()

    ### ! Cube Scan
    logger.info("Scanning cubes")
    await q.put((PERCENTAGES["cube scan"], "scanning cubes"))
    # # TODO: replace with real image scan
    # scanned_cubes = testdata.config03
    gen_images = CubeFaceDetector()
    logger.debug("gen images initialized")
    gen_images.start_detection()
    logger.debug("images generated")
    scanned_cubes = cube_reconstruction.run_detection()
    logger.debug("cubes scanned")
    logger.trace(scanned_cubes)

    ### ! Cube Verification
    logger.info("Verifying cubes")
    await q.put((PERCENTAGES["cube verification"], "verifying cubes"))
    # verified_cubes = (
    #     scanned_cubes  # ? posssibly use scanned cubes if no verification happens
    # )
    api.send_cube_configuration(scanned_cubes)

    ### ! Cube Placement Calculation
    logger.info("Calculating cube placement")
    await q.put((PERCENTAGES["cube placement calculation"], "calculating placement"))
    actions = await cube_placement.get_cube_placing_actions(scanned_cubes)

    ### ! Cube Placement
    logger.info("Placing cubes")
    await q.put((PERCENTAGES["cube placement"], "placing cubes"))
    step = (PERCENTAGES["move platform"] - PERCENTAGES["cube placement"]) / len(actions)
    curr = 0
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
    motor_control.motor_stop()

    ### ! Move Platform Down
    logger.info("Moving platform down")
    await q.put((PERCENTAGES["move platform"], "moving platform"))
    motor_control.show_bed(30, 600, 2400)

    ### ! Done
    logger.info("Done with build")
    await q.put((PERCENTAGES["done"], "done"))
    # TODO: send stop api call
    api.send_end_signal(
        "https://oawz3wjih1.execute-api.eu-central-1.amazonaws.com",
        "team12",
        "R5SfQQ6gKr9A",
    )
    logger.success("Completed build")

    endTime = datetime.now()
    energy = measurelib.read_energy()
    # sound.sound_stop(600)
    # sound.sound_cleanup()
    logger.info(f"time: {endTime-startTime}")
    logger.info(f"energy used: {energy} W*s")


async def reset(q=asyncio.Queue()):
    global is_reset
    logger.info("Resetting positions")
    await q.put((0, "resetting"))
    # await asyncio.sleep(2)
    # motor_control.testFunctions()

    # motor_control.reset_platform_position()

    # raise Exception("Demo")

    ### ! Move platform up (async)
    ### ! Rotate shaft to starting position (async)
    ### ! await above: possibly not enough power

    await q.put((30, "zeroing bed"))
    motor_control.zero_bed()
    await q.put((70, "zeroing mag"))
    motor_control.zero_mag()

    await q.put((70, "setting pin outputs"))
    measurelib.send_ctrlreg_command()
    measurelib.send_chdis_command()
    measurelib.send_negpwr_command()

    # sound.play_melody()
    # api.test_server_reachability(
    #     "https://oawz3wjih1.execute-api.eu-central-1.amazonaws.com"
    # )

    is_reset = True
    await q.put((100, "ready"))
