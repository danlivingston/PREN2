import asyncio
import os
from datetime import datetime

from loguru import logger

from cubepiler import api, cube_placement

if os.getenv("MOCK") == "TRUE":
    logger.warning("MOCKING ENABLED")
    from cubepiler.mock import measurelib, motor_control, sound
else:
    from cubepiler import measurelib, motor_control
    from cubepiler.mock import sound

    # from cubepiler import buzzer_controller as sound

if os.getenv("MOCK_CUBES") == "TRUE":
    from cubepiler.mock import cube_reconstruction, gen_images
else:
    from cubepiler.bilderkennung.CubeReconstruction import CubeReconstruction
    from cubepiler.bilderkennung.getTwoSidesStream import CubeFaceDetector

    gen_images = CubeFaceDetector()
    cube_reconstruction = CubeReconstruction()

is_reset = False


async def warmup_models():
    await asyncio.gather(gen_images.warmupModels(), cube_reconstruction.warmupModels())


def run_mp(status):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(run(status))
    finally:
        loop.close()


def reset_mp(status):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(reset(status))
    finally:
        loop.close()


async def run(status):
    try:
        global is_reset
        if not is_reset:
            logger.warning("resetting as it was not previously reset")
            await reset(status)
        is_reset = False

        logger.info("Starting build")
        loop = asyncio.get_event_loop()

        await sound.sound_start()
        await measurelib.send_refresh_command()  # Starts energy measurement

        asyncio.run_coroutine_threadsafe(api.send_start_signal(), loop)

        startTime = datetime.now()

        logger.info("Scanning cubes")
        status.value = b"scanning cubes"

        await gen_images.start_detection()

        status.value = b"analyzing cubes"
        scanned_cubes = await cube_reconstruction.run_detection()

        asyncio.run_coroutine_threadsafe(
            api.send_cube_configuration(scanned_cubes), loop
        )

        logger.trace(scanned_cubes)

        logger.info("Calculating cube placement")

        status.value = b"calculating placement"
        actions = await cube_placement.get_cube_placing_actions(scanned_cubes)

        logger.info("Placing cubes")
        status.value = b"placing cubes"

        curr = 0
        for action in actions:
            curr += 1
            logger.info(f"Placed {curr}/{len(actions)} cubes")

            status.value = f"placed {curr}/{len(actions)} cubes".encode()
            await motor_control.execute_action(action)

        await motor_control.motor_stop()

        logger.info("Moving platform down")
        status.value = b"showing cubes"

        await motor_control.show_bed()

        logger.info("Done with build")

        energy = await measurelib.read_energy()
        endTime = datetime.now()
        # asyncio.run_coroutine_threadsafe(api.send_end_signal(), loop)
        await api.send_end_signal()
        await sound.sound_stop()

        currententries = await api.get_current_entries()

        logger.success("Completed build")

        logger.trace(currententries)
        logger.info(f"time: {endTime-startTime}")
        logger.info(f"energy used: {energy} W*s")

        status.value = (
            f"time: {currententries['start_to_end']}s\nenergy: {energy} W*s".encode()
        )
    except Exception as e:
        logger.exception(e)
        try:
            status.value = f"!!!ERR!!!{e}".encode()
        finally:
            pass


async def reset(status):
    global is_reset
    logger.info("Resetting")

    status.value = b"resetting"
    await sound.sound_start()

    status.value = b"zeroing bed"
    await motor_control.zero_bed()
    status.value = b"zeroing mag"
    await motor_control.zero_mag()

    status.value = b"energy reset"
    await measurelib.send_ctrlreg_command()
    await measurelib.send_chdis_command()
    await measurelib.send_negpwr_command()

    # status.value = b"api test"
    # loop = asyncio.get_event_loop()
    # asyncio.run_coroutine_threadsafe(api.test_server_reachability(), loop)

    await sound.sound_stop()

    status.value = b"reset done"
    is_reset = True
    logger.info(f"reset {is_reset}")


def zero_bed(status):
    status.value = b"zeroing bed"
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(motor_control.zero_bed())
    finally:
        loop.close()


def zero_mag(status):
    status.value = b"zeroing mag"
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(motor_control.zero_mag())
    finally:
        loop.close()


def show_bed(status):
    status.value = b"showing bed"
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(motor_control.show_bed())
    finally:
        loop.close()


def eject_mag(status):
    status.value = b"ejecting mag"
    # TODO: Implement ejection of all cubes (5x each mag slot)
    status.value = b"!!!ERR!!!Not Implemented Yet"
