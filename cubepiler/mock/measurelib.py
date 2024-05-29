from loguru import logger


async def send_refresh_command():
    logger.warning("mock send refresh command")


async def send_refresh_v_command():
    logger.warning("mock send refresh v command")


async def send_ctrlreg_command():
    logger.warning("mock ctrlreg command")


async def send_chdis_command():
    logger.warning("mock chdis command")


async def send_negpwr_command():
    logger.warning("mock negpwr command")


async def read_voltage():
    logger.warning("mock read voltage")
    return round(321, 2)


async def read_current():
    logger.warning("mock read current")
    return round(90, 3)


async def read_power():
    logger.warning("mock read power")
    return round(5678, 2)


async def read_energy():
    logger.warning("mock read energy")
    return round(1234, 8)
