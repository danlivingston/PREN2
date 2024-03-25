# import subprocess
from multiprocessing import JoinableQueue, Process, Queue
from threading import Thread

import customtkinter
from loguru import logger

from cubepiler.cube_placement import place_cubes
from cubepiler.testdata import config01, config02, config03

# Modes: system (default), light, dark
customtkinter.set_appearance_mode("dark")
# Themes: blue (default), dark-blue, green
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


class CubePiLerGUI:
    app = None
    frame = None
    start_stop_button = None
    reset_button = None
    build_progress_bar = None
    reset_progress_bar = None
    fullscreen = False
    build_process = None
    reset_process = None
    q = Queue()

    def _init_app(self):
        self.app = customtkinter.CTk()
        self.app.rowconfigure(0, weight=1)
        self.app.columnconfigure(0, weight=1)
        self.app.title("CubePiLer")

        self.frame = customtkinter.CTkFrame(master=self.app, corner_radius=0)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_rowconfigure((0, 1), weight=1, uniform="u")
        self.frame.columnconfigure(0, weight=1, uniform="u")

    def _init_buttons(self):
        self.start_stop_button = customtkinter.CTkButton(
            master=self.frame,
            text="start",
            command=self.start,
            corner_radius=0,
            font=("monospace", 200),
            fg_color=COLORS["mantis"],
            hover_color=COLORS["mantis"],
            text_color=COLORS["snow"],
        )
        self.start_stop_button.grid(sticky="nsew", column=0, row=0)

        self.reset_button = customtkinter.CTkButton(
            master=self.frame,
            text="reset",
            command=self.reset,
            corner_radius=0,
            font=("monospace", 200),
            fg_color=COLORS["orange peel"],
            hover_color=COLORS["orange peel"],
            text_color=COLORS["snow"],
        )
        self.reset_button.grid(sticky="nsew", column=0, row=1)

    def _init_progress_bars(self):
        self.reset_progress_bar = customtkinter.CTkProgressBar(
            self.frame,
            orientation="horizontal",
            corner_radius=0,
            progress_color=COLORS["pacific cyan"],
            mode="indeterminate",
        )
        self.build_progress_bar = customtkinter.CTkProgressBar(
            self.frame,
            orientation="horizontal",
            corner_radius=0,
            progress_color=COLORS["mantis"],
            mode="indeterminate",
        )
        # self.reset_progress_bar.grid(sticky="nsew", column=0, row=0)
        # self.reset_progress_bar.start()

    def _start_app(self):
        self.app.geometry("600x400+0+0")
        self.app.bind("<F11>", self._toggle_fullscreen)
        self.app.after(1, self._toggle_fullscreen)
        self.app.after(1, self.app.focus)
        self.app.mainloop()

    def _toggle_fullscreen(self, x=None):
        self.app.state("normal" if self.fullscreen else "zoomed")
        self.app.attributes("-fullscreen", not self.fullscreen)
        self.fullscreen = not self.fullscreen

    def _configure_start_stop_button(self, new_action):
        if new_action == "start":
            self.start_stop_button.configure(
                text="start",
                command=self.start,
                fg_color=COLORS["mantis"],
                hover_color=COLORS["mantis"],
            )
            self.start_stop_button.grid(sticky="nsew", column=0, row=0)
            self.reset_progress_bar.grid_remove()
        elif new_action == "stop":
            self.start_stop_button.configure(
                text="stop",
                command=self.stop,
                fg_color=COLORS["engineering orange"],
                hover_color=COLORS["engineering orange"],
            )
            self.start_stop_button.grid(sticky="nsew", column=0, row=0)
            self.reset_progress_bar.grid_remove()
        elif new_action == "loading":
            self.reset_progress_bar.grid(sticky="nsew", column=0, row=0)
            self.start_stop_button.grid_remove()
            self.reset_progress_bar.start()

    def _configure_reset_button(self, new):
        if new == "reset":
            self.reset_button.configure(text="reset", command=self.reset)
            self.reset_button.grid(sticky="nsew", column=0, row=1)
            self.build_progress_bar.grid_remove()
        elif new == "stop":
            self.reset_button.configure(text="stop", command=self.stop)
            self.reset_button.grid(sticky="nsew", column=0, row=1)
            self.build_progress_bar.grid_remove()
        elif new == "loading":
            self.build_progress_bar.grid(sticky="nsew", column=0, row=1)
            self.reset_button.grid_remove()
            self.build_progress_bar.start()

    def __init__(self):
        logger.info("Initializing GUI")
        self._init_app()
        self._init_buttons()
        self._init_progress_bars()
        logger.info("Starting GUI")
        self._start_app()
        logger.info("Exiting GUI")

    @logger.catch(level="CRITICAL")
    def start(self, x=None):
        logger.info("Starting...")
        self._configure_start_stop_button("stop")
        self._configure_reset_button("loading")
        t = Thread(target=self.start_build, name="build")
        t.start()
        logger.info("Started")

    @logger.catch(level="CRITICAL")
    def stop(self, x=None):
        logger.info("Stopping...")
        if self.build_process:
            self.build_process.kill()
            # self.build_process.join(0)
            self.build_process = None
        if self.reset_process:
            self.reset_process.kill()
            # self.reset_process.join(0)
            self.reset_process = None
        self._configure_start_stop_button("start")
        self._configure_reset_button("reset")
        logger.info("Stopped")

    @logger.catch(level="CRITICAL")
    def reset(self, x=None):
        logger.info("Resetting...")
        self._configure_start_stop_button("loading")
        self._configure_reset_button("stop")
        t = Thread(target=self.start_reset, name="reset")
        t.start()
        logger.info("Reset")

    def start_build(self):
        self.build_process = Process(target=place_cubes, args=(config01,))
        self.build_process.start()
        self.build_process.join()
        # place_cubes(config01)
        self.stop()

    def start_reset(self):
        self.reset_process = Process(target=place_cubes, args=(config01,))
        self.reset_process.start()
        self.reset_process.join()
        # place_cubes(config02)
        self.stop()


if __name__ == "__main__":
    gui = CubePiLerGUI()
