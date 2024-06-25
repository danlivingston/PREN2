import asyncio
import os
from datetime import datetime

from loguru import logger

from cubepiler import api, cube_placement

if os.getenv("MOCK") == "TRUE":
    logger.warning("MOCKING ENABLED")
    from cubepiler.mock import measurelib, motor_control, sound
else:
    # from cubepiler.mock import sound
    from cubepiler import buzzer_controller as sound
    from cubepiler import measurelib, motor_control

if os.getenv("MOCK_CUBES") == "TRUE":
    from cubepiler.mock import cube_reconstruction, gen_images
else:
    from cubepiler.bilderkennung.CubeReconstruction import CubeReconstruction
    from cubepiler.bilderkennung.getTwoSidesStream import CubeFaceDetector

    gen_images = CubeFaceDetector()
    cube_reconstruction = CubeReconstruction()

# TODO: fix not working anymore (multiprocessing problem?)
# is_reset = False
# from multiprocessing import Manager

# manager = Manager()
# is_reset = manager.Value("b", False)


async def warmup_models():
    await asyncio.gather(gen_images.warmupModels(), cube_reconstruction.warmupModels())


def run_mp(status, is_reset):
    logger.trace(f"is_reset {is_reset.value}")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(run(status, is_reset))
    finally:
        loop.close()


def reset_mp(status, is_reset):
    logger.trace(f"is_reset {is_reset.value}")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(reset(status, is_reset))
    finally:
        loop.close()


async def run(status, is_reset):
    try:
        if not is_reset.value:
            logger.warning("resetting as it was not previously reset")
            await reset(status, is_reset)
        is_reset.value = False

        logger.info("Starting build")
        loop = asyncio.get_event_loop()

        await sound.sound_start()
        await measurelib.send_refresh_command()  # Starts energy measurement

        # asyncio.run_coroutine_threadsafe(api.send_start_signal(), loop)
        await api.send_start_signal()

        startTime = datetime.now()

        logger.info("Scanning cubes")
        status.value = b"scanning cubes"

        await gen_images.start_detection()

        status.value = b"analyzing cubes"
        scanned_cubes = await cube_reconstruction.run_detection()

        # asyncio.run_coroutine_threadsafe(
        #     api.send_cube_configuration(scanned_cubes), loop
        # )
        await api.send_cube_configuration()

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

        # asyncio.run_coroutine_threadsafe(api.get_current_entries(), loop)

        logger.success("Completed build")

        time_diff = endTime - startTime

        minutes = time_diff.seconds // 60
        seconds = time_diff.seconds % 60
        milliseconds = time_diff.microseconds // 1000

        formatted_time_diff = f"{minutes:02}:{seconds:02}.{milliseconds:03}"

        logger.info(f"time: {formatted_time_diff}")
        logger.info(f"energy used: {energy}e-3 Wh")

        status.value = f"time: {formatted_time_diff}\nenergy: {energy}e-3 Wh".encode()
        # await api.get_current_entries()
    except Exception as e:
        logger.exception(e)
        try:
            status.value = f"!!!ERR!!!{e}".encode()
        finally:
            pass


async def reset(status, is_reset):
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
    is_reset.value = True
    logger.info(f"reset {is_reset.value}")


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


def test_buzzer(status):
    status.value = b"testing buzzer"
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(sound.sound_start())
        loop.run_until_complete(asyncio.sleep(1))
        loop.run_until_complete(sound.sound_stop())
        loop.run_until_complete(asyncio.sleep(1))
        loop.run_until_complete(sound.sound_touch())
        loop.run_until_complete(asyncio.sleep(1))
    finally:
        loop.close()


def eject_mag(status):
    status.value = b"ejecting mag"
    status.value = b"!!!ERR!!!No you don't"
