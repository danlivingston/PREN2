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
}

STATES = Enum("STATES", ["START", "READY", "RESETTING", "RUNNING", "EXCEPTION", "STOP"])


class CubePiLerGUI(customtkinter.CTk):
    def __init__(self, loop):
        self.state = STATES.START
        self.loop = loop
        self.fullscreen = False
        self.build_task = None
        self.progress_queue = asyncio.Queue()

        self.root = customtkinter.CTk()
        self.root.title("CubePiLer")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.geometry("600x400+0+0")
        self.root.protocol(
            "WM_DELETE_WINDOW",
            lambda: self.loop.create_task(self.exit()),
        )
        # self.root.after(1, self.root.focus)
        self.root.after(1, lambda: self.loop.create_task(self.toggle_fullscreen()))
        self.root.bind(
            "<F11>", lambda e=None: self.loop.create_task(self.toggle_fullscreen())
        )

        # self.root.configure(bg="transparent")
        # self.root.wm_attributes("-transparentcolor", "black")

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
            fg_color=COLORS["engineering orange"],
            hover_color=COLORS["engineering orange"],
            text_color=COLORS["snow"],
        )
        # self.stop_button.grid(sticky="nsew", column=0, row=1)
        self.progress_bar = customtkinter.CTkProgressBar(
            master=self.frame,
            orientation="horizontal",
            corner_radius=0,
            progress_color=COLORS["pacific cyan"],
            mode="determinate",
            # mode="indeterminate",
        )
        self.progress_label = customtkinter.CTkLabel(
            master=self.frame,
            text="...",
            fg_color="transparent",
            # bg_color="black",
            # bg_color="transparent",
            # bg_color=COLORS["mantis"],
            text_color=COLORS["snow"],
            font=("monospace", 100),
        )

    async def mainloop(self):
        logger.debug("showing GUI")

        self.state = STATES.READY

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
            # self.start_button.configure(state="disabled")
            self.stop_button.grid(sticky="nsew", column=0, row=0)
            self.progress_bar.configure(progress_color=COLORS["pacific cyan"])
            self.progress_bar.grid(sticky="nsew", column=0, row=1)
            self.progress_label.grid(column=0, row=1)
            # self.progress_bar.place(x=0, y=0, relwidth=1, relheight=1)
            # self.progress_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.start_button.grid_remove()

            if not self.state == STATES.READY:
                return

            self.state = STATES.RUNNING
            pb = self.loop.create_task(self.run_progress_bar())

            logger.debug("start build")

            # await asyncio.sleep(10)
            await runner.run(self.progress_queue)

            logger.debug("finished build")

            await pb
            pb = None

        except asyncio.CancelledError:
            logger.debug("cancelled build")

        finally:
            if not pb == None:
                pb.cancel()

            self.start_button.grid(sticky="nsew", column=0, row=0)
            self.stop_button.grid_remove()
            self.progress_bar.grid_remove()
            self.progress_label.grid_remove()
            self.state = STATES.READY
            # self.start_button.configure(state="enabled")

    async def cancel_build(self, event=None):
        if not self.build_task or self.build_task is None:
            return

        logger.debug("cancelling build task")

        self.build_task.cancel()  # ? will only exit at first opportunity unless try catch is used in build_task
        await self.build_task
        self.build_task = None

        logger.debug("cancelled build task")

    async def run_progress_bar(self):
        try:
            # self.build_progress_bar.set(0)
            curr = 0

            while self.state == STATES.RUNNING or self.state == STATES.RESETTING:
                prog, label = await self.progress_queue.get()
                self.progress_label.configure(text=label)

                while not curr >= prog:
                    curr += 1
                    self.progress_bar.set(curr / 100)
                    await asyncio.sleep(0.01)

                if prog >= 100:
                    self.progress_bar.configure(progress_color=COLORS["emerald"])
                    await asyncio.sleep(3)
                    break
        except asyncio.CancelledError:
            pass
        finally:
            logger.debug("RUN PB DONE")
