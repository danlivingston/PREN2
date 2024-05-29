import os
import asyncio
from datetime import datetime

from loguru import logger

from cubepiler import api, cube_placement

if os.getenv("MOCK") == "TRUE":
    logger.warning("MOCKING ENABLED")
    from cubepiler.mock import measurelib, motor_control, sound
else:
    from cubepiler import measurelib, motor_control, sound

if os.getenv("MOCK_CUBES") == "TRUE":
    from cubepiler.mock import gen_images, cube_reconstruction
else:
    from cubepiler.bilderkennung.CubeReconstruction import CubeReconstruction
    from cubepiler.bilderkennung.getTwoSidesStream import CubeFaceDetector

    gen_images = CubeFaceDetector()
    cube_reconstruction = CubeReconstruction()

is_reset = False


async def warmup_models():
    await gen_images.warmupModels()
    await cube_reconstruction.warmupModels()


async def run():
    try:
        global is_reset
        if not is_reset:
            await reset()
        is_reset = False

        logger.info("Starting build")
        loop = asyncio.get_event_loop()

        await sound.sound_start()
        await measurelib.send_refresh_command()  # Starts energy measurement

        asyncio.run_coroutine_threadsafe(api.send_start_signal(), loop)

        startTime = datetime.now()

        logger.info("Scanning cubes")

        await gen_images.start_detection()
        scanned_cubes = await cube_reconstruction.run_detection()

        asyncio.run_coroutine_threadsafe(
            api.send_cube_configuration(scanned_cubes), loop
        )

        logger.trace(scanned_cubes)

        logger.info("Calculating cube placement")

        actions = await cube_placement.get_cube_placing_actions(scanned_cubes)

        logger.info("Placing cubes")

        curr = 0
        for action in actions:
            curr += 1
            logger.info(f"Placed {curr}/{len(actions)} cubes")
            await motor_control.execute_action(action)

        await motor_control.motor_stop()

        logger.info("Moving platform down")

        await motor_control.show_bed(
            30, 600, 4050
        )  # TODO: remove params from function call

        logger.info("Done with build")

        asyncio.run_coroutine_threadsafe(api.send_end_signal(), loop)
        energy = await measurelib.read_energy()
        endTime = datetime.now()

        await sound.sound_stop()

        currententries = await api.get_current_entries()

        logger.success("Completed build")

        logger.trace(currententries)
        logger.info(f"time: {endTime-startTime}")
        logger.info(f"energy used: {energy} W*s")
    except Exception as e:
        logger.exception(e)
        raise Exception("Build Failed")


def run_mp():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(run())
    finally:
        loop.close()


async def reset():
    global is_reset
    logger.info("Resetting")
    await sound.sound_start()

    await motor_control.zero_bed()
    await motor_control.zero_mag()

    await measurelib.send_ctrlreg_command()
    await measurelib.send_chdis_command()
    await measurelib.send_negpwr_command()

    await api.test_server_reachability()  # TODO: remove params from function call
    await sound.sound_stop()

    is_reset = True
