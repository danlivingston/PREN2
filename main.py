import asyncio
import os
import sys

from dotenv import load_dotenv
from loguru import logger

from cubepiler import configure_logger

load_dotenv()


class Main:
    @logger.catch(level="CRITICAL")
    async def exec(self):
        from cubepiler.gui import CubePiLerGUI

        autofullscreen = not os.getenv("AUTOFULLSCREEN", "TRUE") == "FALSE"
        loop = asyncio.get_event_loop()
        self.gui = CubePiLerGUI(loop, autofullscreen)
        await self.gui.mainloop()


if __name__ == "__main__":
    # LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")  # Defaults to INFO if not set
    # logger.remove(0)
    # logger.add(
    #     sys.stdout,
    #     level=LOG_LEVEL,
    # )
    # logger.add(
    #     "logs/trace_{time:YYYY-MM-DD}.log",
    #     enqueue=True,
    #     level="TRACE",
    #     rotation="00:00",
    #     retention="10d",
    # )

    configure_logger.configure("main")

    logger.debug("starting main")
    asyncio.run(Main().exec())
    logger.debug("exiting main")
