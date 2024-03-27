import asyncio
from enum import Enum

import customtkinter
from loguru import logger

from cubepiler import runner

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
    "DIVIDER": "",
    "black": "#000000",
    "white": "#FFFBFE",
    "green": "#1EC276",
    "orange": "#FFA630",
    "red": "#B80600",
    "blue": "#1CA3C4",
}

STATES = Enum("STATES", ["START", "READY", "RESETTING", "RUNNING", "EXCEPTION", "STOP"])


class CubePiLerGUI(customtkinter.CTk):
    def __init__(self, loop):
        self.state = STATES.START
        self.loop = loop
        self.fullscreen = False
        self.running_task = None
        self.progress_queue = asyncio.Queue()

        self.root = customtkinter.CTk()
        self.root.title("CubePiLer")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.geometry("800x480+0+0")
        self.root.protocol(
            "WM_DELETE_WINDOW",
            lambda: self.loop.create_task(self.exit()),
        )
        # self.root.after(1, lambda: self.loop.create_task(self.toggle_fullscreen())) # * for use on pi for auto fullscreen
        self.root.bind(
            "<F11>", lambda e=None: self.loop.create_task(self.toggle_fullscreen())
        )

        self.frame = customtkinter.CTkFrame(
            master=self.root, corner_radius=0, fg_color=COLORS["black"]
        )
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_rowconfigure(0, weight=3, uniform="u")
        self.frame.grid_rowconfigure(1, weight=1, uniform="u")
        self.frame.grid_rowconfigure(2, weight=2, uniform="u")
        self.frame.columnconfigure(0, weight=1, uniform="u")

        self.start_button = customtkinter.CTkButton(
            master=self.frame,
            text="start",
            command=lambda: setattr(
                self, "running_task", self.loop.create_task(self.start_build())
            ),
            corner_radius=0,
            font=("monospace", 200),
            fg_color=COLORS["green"],
            hover_color=COLORS["green"],
            text_color=COLORS["white"],
        )

        self.stop_button = customtkinter.CTkButton(
            master=self.frame,
            text="stop",
            command=lambda: self.loop.create_task(self.cancel_build()),
            corner_radius=0,
            font=("monospace", 200),
            fg_color=COLORS["red"],
            hover_color=COLORS["red"],
            text_color=COLORS["white"],
        )

        self.reset_button = customtkinter.CTkButton(
            master=self.frame,
            text="reset",
            command=lambda: setattr(
                self, "running_task", self.loop.create_task(self.reset_build())
            ),
            corner_radius=0,
            font=("monospace", 200),
            fg_color=COLORS["orange"],
            hover_color=COLORS["orange"],
            text_color=COLORS["white"],
        )

        self.progress_bar = customtkinter.CTkProgressBar(
            master=self.frame,
            orientation="horizontal",
            corner_radius=0,
            progress_color=COLORS["blue"],
            fg_color=COLORS["black"],
            mode="determinate",
        )
        self.progress_label = customtkinter.CTkLabel(
            master=self.frame,
            text="...",
            fg_color=COLORS["black"],
            text_color=COLORS["white"],
            font=("monospace", 70),
        )

    async def mainloop(self):
        logger.debug("showing GUI")
        self.state = STATES.READY
        self.state_switch_gui()
        while not self.state == STATES.STOP:
            self.root.update()
            await asyncio.sleep(0.1)
        logger.debug("destroying GUI")
        self.root.destroy()
        logger.debug("destroyed GUI")

    async def toggle_fullscreen(self, event=None):
        logger.debug("toggling fullscreen")
        self.root.state("normal" if self.fullscreen else "zoomed")
        self.root.attributes("-fullscreen", not self.fullscreen)
        self.fullscreen = not self.fullscreen

    async def exit(self, event=None):
        logger.debug("exiting")
        await self.cancel_build()
        self.state = STATES.STOP

    async def start_build(self, event=None):
        pb = None
        try:
            if not self.state == STATES.READY:
                return
            self.state = STATES.RUNNING
            self.state_switch_gui()
            pb = self.loop.create_task(self.run_progress_bar())
            logger.debug("start build")
            await runner.run(self.progress_queue)
            logger.debug("finished build")
            await pb
            pb = None
        except asyncio.CancelledError:
            logger.debug("cancelled build")
        finally:
            if not pb == None:
                pb.cancel()
            self.state = STATES.READY
            self.state_switch_gui()

    async def cancel_build(self, event=None):
        if not self.running_task or self.running_task is None:
            return
        logger.debug("cancelling build task")
        self.running_task.cancel()  # ? will only exit at first opportunity unless try catch is used in build_task
        await self.running_task
        self.running_task = None
        logger.debug("cancelled build task")

    async def reset_build(self, event=None):
        pb = None
        try:
            if not self.state == STATES.READY:
                return
            self.state = STATES.RESETTING
            self.state_switch_gui()
            pb = self.loop.create_task(self.run_progress_bar())
            logger.debug("start reset")
            await runner.reset(self.progress_queue)
            logger.debug("finished reset")
            await pb
            pb = None
        except asyncio.CancelledError:
            logger.debug("cancelled reset")
        finally:
            if not pb == None:
                pb.cancel()
            self.state = STATES.READY
            self.state_switch_gui()

    async def run_progress_bar(self):
        try:
            self.progress_bar.configure(progress_color=COLORS["blue"])
            self.progress_bar.set(0)
            curr = 0
            while self.state == STATES.RUNNING or self.state == STATES.RESETTING:
                prog, label = await self.progress_queue.get()
                self.progress_label.configure(text=label)
                while not curr >= prog:
                    curr += 1
                    self.progress_bar.set(curr / 100)
                    await asyncio.sleep(0.01)
                if prog >= 100:
                    self.progress_bar.configure(progress_color=COLORS["green"])
                    await asyncio.sleep(3)
                    break
        except asyncio.CancelledError:
            pass
        finally:
            pass

    def state_switch_gui(self):
        # TODO: End/Success Screen
        # ? TODO: Aborted Screen
        # ? TODO: Starting Screen
        match self.state:
            case STATES.READY:
                self.start_button.grid(sticky="nsew", column=0, row=0)
                self.stop_button.grid_remove()
                self.reset_button.grid(sticky="nsew", column=0, row=1, rowspan=2)
                self.progress_bar.grid_remove()
                self.progress_label.grid_remove()
            case STATES.RUNNING | STATES.RESETTING:
                self.start_button.grid_remove()
                self.stop_button.grid(sticky="nsew", column=0, row=0)
                self.reset_button.grid_remove()
                self.progress_bar.grid(sticky="nsew", column=0, row=2)
                self.progress_label.grid(column=0, row=1)
            case _:
                pass
