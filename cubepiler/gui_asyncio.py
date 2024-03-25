import asyncio
from enum import Enum

import customtkinter
from loguru import logger

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

COLORS = {
    "dim gray": "#706677",
    "mantis": "#7BC950",
    "snow": "#FFFBFE",
    "gunmetal": "#13262B",
    "pacific cyan": "#1CA3C4",
    "engineering orange": "#B80600",
    "emerald": "#1EC276",
    "orange peel": "#FFA630",
}

STATES = Enum("STATES", ["START", "READY", "RESETTING", "RUNNING", "EXCEPTION", "STOP"])


class CubePiLerGUI(customtkinter.CTk):
    def __init__(self, loop):
        self.state = STATES.START
        self.loop = loop
        self.fullscreen = False

        self.root = customtkinter.CTk()
        self.root.title("CubePiLer")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.geometry("600x400+0+0")
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.after(3, self.toggle_fullscreen)
        self.root.after(3, self.root.focus)
        self.root.protocol("WM_DELETE_WINDOW", self.exit)

        self.frame = customtkinter.CTkFrame(master=self.root, corner_radius=0)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_rowconfigure((0, 1), weight=1, uniform="u")
        self.frame.columnconfigure(0, weight=1, uniform="u")

        self.start_button = customtkinter.CTkButton(
            master=self.frame,
            text="start",
            command=lambda: setattr(
                self, "build_task", self.loop.create_task(self.start_build())
            ),
            corner_radius=0,
            font=("monospace", 200),
            fg_color=COLORS["mantis"],
            hover_color=COLORS["mantis"],
            text_color=COLORS["snow"],
        )
        self.start_button.grid(sticky="nsew", column=0, row=0)
        self.stop_button = customtkinter.CTkButton(
            master=self.frame,
            text="stop",
            command=lambda: self.loop.create_task(self.cancel_build()),
            corner_radius=0,
            font=("monospace", 200),
            fg_color=COLORS["mantis"],
            hover_color=COLORS["mantis"],
            text_color=COLORS["snow"],
        )
        self.stop_button.grid(sticky="nsew", column=0, row=1)

    async def mainloop(self):
        logger.debug("showing GUI")
        self.state = STATES.READY
        while not self.state == STATES.STOP:
            self.root.update()
            await asyncio.sleep(0.1)
        logger.debug("destroying GUI")
        self.root.destroy()
        logger.debug("destroyed GUI")

    def toggle_fullscreen(self, event=None):
        logger.debug("toggling fullscreen")
        self.root.state("normal" if self.fullscreen else "zoomed")
        self.root.attributes("-fullscreen", not self.fullscreen)
        self.fullscreen = not self.fullscreen

    def exit(self, event=None):
        logger.debug("exiting")
        self.state = STATES.STOP

    async def start_build(self, event=None):
        try:
            self.start_button.configure(state="disabled")
            if not self.state == STATES.READY:
                return
            self.state = STATES.RUNNING
            logger.debug("start build")
            await asyncio.sleep(10)
            logger.debug("finished build")
        except asyncio.CancelledError:
            logger.debug("cancelled build")
        finally:
            self.state = STATES.READY
            self.start_button.configure(state="enabled")

    async def cancel_build(self, event=None):
        if self.build_task is None:
            return

        logger.debug("cancelling build task")
        self.build_task.cancel()  # ? will only exit at first opportunity
        await self.build_task
        self.build_task = None
        logger.debug("cancelled build task")
