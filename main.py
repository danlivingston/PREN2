import asyncio

from loguru import logger

from cubepiler.gui_asyncio import CubePiLerGUI


class Main:
    @logger.catch(level="CRITICAL")
    async def exec(self):
        self.gui = CubePiLerGUI(asyncio.get_event_loop())
        await self.gui.mainloop()


if __name__ == "__main__":
    logger.debug("starting main")
    asyncio.run(Main().exec())
    logger.debug("exiting main")
