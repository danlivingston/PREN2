import asyncio
import multiprocessing as mp
import platform
from enum import Enum

import customtkinter
from loguru import logger

# imported later in CubePiLerGUI.mainloop() for faster initial GUI loading
global runner

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# source: https://fonts.google.com/specimen/Source+Code+Pro
customtkinter.FontManager.load_font("fonts/SourceCodePro-SemiBold.ttf")
customtkinter.FontManager.load_font("fonts/SourceCodePro-Regular.ttf")

COLORS = {
    "black": "#000000",
    "white": "#FFFBFE",
    "green": "#1EC276",
    "orange": "#FFA630",
    "red": "#B80600",
    "blue": "#1CA3C4",
}

STATES = Enum(
    "STATES",
    [
        "START",
        "READY",
        "RUNNING",
        "EXCEPTION",
        "SUCCESS",
        "DEBUG",
        "STOP",
    ],
)


class CubePiLerGUI(customtkinter.CTk):
    def __init__(self, loop, autofullscreen=True):
        self.state = STATES.START
        self.status = mp.Array("c", 200)
        self.is_reset = mp.Value("b", False)
        self.loop = loop
        self.fullscreen = False
        self.running_task = None

        self.root = customtkinter.CTk()
        self.root.title("CubePiLer")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.geometry("800x480+0+0")
        self.root.protocol(
            "WM_DELETE_WINDOW",
            lambda: self.loop.create_task(self.exit()),
        )

        self.autofullscreen = autofullscreen
        self.root.bind(
            "<F11>", lambda e=None: self.loop.create_task(self.toggle_fullscreen())
        )

        self.frame = customtkinter.CTkFrame(
            master=self.root, corner_radius=0, fg_color=COLORS["black"]
        )
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_rowconfigure(0, weight=1, uniform="u")
        self.frame.grid_rowconfigure(1, weight=1, uniform="u")
        self.frame.grid_rowconfigure(2, weight=1, uniform="u")
        self.frame.grid_rowconfigure(3, weight=1, uniform="u")
        self.frame.grid_rowconfigure(4, weight=1, uniform="u")
        self.frame.grid_rowconfigure(5, weight=1, uniform="u")
        self.frame.columnconfigure(0, weight=1, uniform="u")
        self.frame.columnconfigure(1, weight=1, uniform="u")

        self.semi_bold_font = customtkinter.CTkFont(
            family="Source Code Pro SemiBold",
            size=75,
        )
        self.regular_font = customtkinter.CTkFont(
            family="Source Code Pro",
            size=60,
        )
        self.regular_font_s = customtkinter.CTkFont(
            family="Source Code Pro",
            size=40,
        )

        self.start_button = customtkinter.CTkButton(
            master=self.frame,
            text="start",
            command=lambda: setattr(
                self, "running_task", self.loop.create_task(self.start_build())
            ),
            corner_radius=0,
            font=self.semi_bold_font,
            fg_color=COLORS["green"],
            hover_color=COLORS["green"],
            text_color=COLORS["white"],
        )

        self.stop_button = customtkinter.CTkButton(
            master=self.frame,
            text="cancel",
            command=lambda: self.loop.create_task(self.cancel_process()),
            corner_radius=0,
            font=self.semi_bold_font,
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
            font=self.semi_bold_font,
            fg_color=COLORS["orange"],
            hover_color=COLORS["orange"],
            text_color=COLORS["white"],
        )

        self.debug_button = customtkinter.CTkButton(
            master=self.frame,
            text="debug",
            command=lambda: setattr(
                self, "running_task", self.loop.create_task(self.enter_debug_mode())
            ),
            corner_radius=0,
            font=self.semi_bold_font,
            fg_color=COLORS["red"],
            hover_color=COLORS["red"],
            text_color=COLORS["white"],
        )

        self.debug_show_bed_button = customtkinter.CTkButton(
            master=self.frame,
            text="show bed",
            command=lambda: setattr(
                self, "running_task", self.loop.create_task(self.start_show_bed())
            ),
            corner_radius=0,
            font=self.regular_font,
            fg_color=COLORS["red"],
            hover_color=COLORS["red"],
            text_color=COLORS["white"],
        )

        self.debug_zero_bed_button = customtkinter.CTkButton(
            master=self.frame,
            text="zero bed",
            command=lambda: setattr(
                self, "running_task", self.loop.create_task(self.start_zero_bed())
            ),
            corner_radius=0,
            font=self.regular_font,
            fg_color=COLORS["orange"],
            hover_color=COLORS["orange"],
            text_color=COLORS["white"],
        )

        self.debug_zero_mag_button = customtkinter.CTkButton(
            master=self.frame,
            text="zero mag",
            command=lambda: setattr(
                self, "running_task", self.loop.create_task(self.start_zero_mag())
            ),
            corner_radius=0,
            font=self.regular_font,
            fg_color=COLORS["orange"],
            hover_color=COLORS["orange"],
            text_color=COLORS["white"],
        )

        self.debug_eject_mag_button = customtkinter.CTkButton(
            master=self.frame,
            text="eject mag",
            command=lambda: setattr(
                self, "running_task", self.loop.create_task(self.start_eject_mag())
            ),
            corner_radius=0,
            font=self.regular_font,
            fg_color=COLORS["red"],
            hover_color=COLORS["red"],
            text_color=COLORS["white"],
        )

        self.debug_buzzer_button = customtkinter.CTkButton(
            master=self.frame,
            text="buzzer",
            command=lambda: setattr(
                self, "running_task", self.loop.create_task(self.start_buzzer())
            ),
            corner_radius=0,
            font=self.regular_font,
            fg_color=COLORS["green"],
            hover_color=COLORS["green"],
            text_color=COLORS["white"],
        )

        self.back_button = customtkinter.CTkButton(
            master=self.frame,
            text="BACK",
            command=lambda: setattr(
                self, "running_task", self.loop.create_task(self.dismiss_button())
            ),
            corner_radius=0,
            font=self.semi_bold_font,
            fg_color=COLORS["blue"],
            hover_color=COLORS["blue"],
            text_color=COLORS["white"],
        )

        self.success_button = customtkinter.CTkButton(
            master=self.frame,
            text="SUCCESS",
            command=lambda: setattr(
                self, "running_task", self.loop.create_task(self.dismiss_button())
            ),
            corner_radius=0,
            font=self.semi_bold_font,
            fg_color=COLORS["green"],
            hover_color=COLORS["green"],
            text_color=COLORS["white"],
        )

        self.exception_button = customtkinter.CTkButton(
            master=self.frame,
            text="ERROR",
            command=lambda: setattr(
                self, "running_task", self.loop.create_task(self.dismiss_button())
            ),
            corner_radius=0,
            font=self.semi_bold_font,
            fg_color=COLORS["red"],
            hover_color=COLORS["red"],
            text_color=COLORS["white"],
        )

        self.startup_button = customtkinter.CTkButton(
            master=self.frame,
            text="INITIALIZING...",
            corner_radius=0,
            font=self.semi_bold_font,
            fg_color=COLORS["black"],
            hover_color=COLORS["black"],
            text_color=COLORS["white"],
        )

        self.status_button = customtkinter.CTkButton(
            master=self.frame,
            text="LOREM",
            corner_radius=0,
            font=self.regular_font,
            fg_color=COLORS["black"],
            hover_color=COLORS["black"],
            text_color=COLORS["white"],
        )

        self.progress_bar = customtkinter.CTkProgressBar(
            master=self.frame,
            orientation="horizontal",
            corner_radius=0,
            progress_color=COLORS["blue"],
            fg_color=COLORS["black"],
            mode="indeterminate",
            indeterminate_speed=3,
        )

    async def mainloop(self):
        # shows gui as early as possbile
        logger.debug("initializing")
        if self.autofullscreen:
            await self.toggle_fullscreen()
        self.state_switch_gui()
        self.root.update()

        # not very nice but this saves time importing the module after gui has started, might break in future
        global runner
        from cubepiler import runner

        await runner.warmup_models()

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
        if platform.system() == "Windows":
            self.root.state("normal" if self.fullscreen else "zoomed")
        self.root.attributes("-fullscreen", not self.fullscreen)
        self.fullscreen = not self.fullscreen

    async def exit(self, event=None):
        logger.debug("exiting")
        await self.cancel_process()
        self.state = STATES.STOP

    async def run_process(
        self, target, args, name, startstate=STATES.READY, endstate=STATES.SUCCESS
    ):
        logger.trace(
            f"start process {name}, {target}({args}), {startstate} -> {endstate}"
        )
        p = None

        self.status.value = f"starting {name}".encode()

        try:
            if not self.state == startstate:
                return
            self.state = STATES.RUNNING
            self.state_switch_gui()
            p = mp.Process(target=target, args=args, name=f"{name} runner")
            p.start()
            while p.is_alive():
                self.status_button.configure(text=self.status.value.decode())
                await asyncio.sleep(0.1)
            if self.status.value.decode().startswith("!!!ERR!!!"):
                self.state = STATES.EXCEPTION
                self.status.value = f"{self.status.value.decode()[9:]}".encode()
            else:
                self.state = endstate
        except asyncio.CancelledError:
            if p is not None and p.is_alive():
                p.kill()
                p.join()
            logger.debug("cancelled build")
            self.status.value = b"aborted manually"
            self.state = STATES.EXCEPTION
        except Exception as e:
            logger.exception(e)
            self.status.value = f"{e}".encode()
            self.state = STATES.EXCEPTION
        finally:
            self.status_button.configure(text=self.status.value.decode())
            self.state_switch_gui()

    async def cancel_process(self, event=None):
        if not self.running_task or self.running_task is None:
            return
        logger.debug("cancelling task")
        self.running_task.cancel()  # ? will only exit at first opportunity unless try catch is used in build_task
        await self.running_task
        self.running_task = None
        logger.debug("cancelled task")

    async def start_build(self, event=None):
        await self.run_process(
            runner.run_mp,
            (
                self.status,
                self.is_reset,
            ),
            "build",
        )

    async def reset_build(self, event=None):
        await self.run_process(
            runner.reset_mp,
            (
                self.status,
                self.is_reset,
            ),
            "reset",
            STATES.READY,
            STATES.READY,
        )

    async def start_zero_mag(self, event=None):
        await self.run_process(
            runner.zero_mag, (self.status,), "zero mag", STATES.DEBUG, STATES.DEBUG
        )

    async def start_zero_bed(self, event=None):
        await self.run_process(
            runner.zero_bed, (self.status,), "zero bed", STATES.DEBUG, STATES.DEBUG
        )

    async def start_show_bed(self, event=None):
        await self.run_process(
            runner.show_bed, (self.status,), "show bed", STATES.DEBUG, STATES.DEBUG
        )

    async def start_eject_mag(self, event=None):
        await self.run_process(
            runner.eject_mag, (self.status,), "eject mag", STATES.DEBUG, STATES.DEBUG
        )

    async def start_buzzer(self, event=None):
        await self.run_process(
            runner.test_buzzer,
            (self.status,),
            "buzzer test",
            STATES.DEBUG,
            STATES.DEBUG,
        )

    async def dismiss_button(self):
        logger.debug("dismiss")
        self.state = STATES.READY
        self.state_switch_gui()

    async def enter_debug_mode(self):
        logger.debug("debug mode")
        self.state = STATES.DEBUG
        self.state_switch_gui()

    def remove_all_gui_elements(self):
        self.start_button.grid_remove()
        self.stop_button.grid_remove()
        self.reset_button.grid_remove()
        self.debug_button.grid_remove()
        self.back_button.grid_remove()
        self.success_button.grid_remove()
        self.exception_button.grid_remove()
        self.startup_button.grid_remove()
        self.status_button.grid_remove()
        self.progress_bar.grid_remove()
        self.progress_bar.stop()
        self.debug_eject_mag_button.grid_remove()
        self.debug_show_bed_button.grid_remove()
        self.debug_zero_bed_button.grid_remove()
        self.debug_zero_mag_button.grid_remove()
        self.debug_buzzer_button.grid_remove()

    def state_switch_gui(self):
        self.remove_all_gui_elements()
        logger.trace(f"switching gui state to {self.state}")
        match self.state:
            case STATES.READY:
                self.start_button.grid(
                    sticky="nsew", column=0, row=0, rowspan=3, columnspan=2
                )
                self.reset_button.grid(
                    sticky="nsew",
                    column=0,
                    row=3,
                    rowspan=3,
                )
                self.debug_button.grid(
                    sticky="nsew",
                    column=1,
                    row=3,
                    rowspan=3,
                )

            case STATES.RUNNING:
                self.stop_button.grid(
                    sticky="nsew", column=0, row=0, rowspan=3, columnspan=2
                )
                self.status_button.configure(font=self.regular_font)
                self.status_button.grid(
                    sticky="nsew", column=0, row=3, rowspan=2, columnspan=2
                )
                self.progress_bar.grid(
                    sticky="nsew", column=0, row=5, rowspan=1, columnspan=2
                )
                self.progress_bar.start()

            case STATES.SUCCESS:
                self.success_button.grid(
                    sticky="nsew", column=0, row=0, rowspan=3, columnspan=2
                )
                self.status_button.configure(font=self.regular_font_s)
                self.status_button.grid(
                    sticky="nsew", column=0, row=3, rowspan=3, columnspan=2
                )

            case STATES.EXCEPTION:
                self.exception_button.grid(
                    sticky="nsew", column=0, row=0, rowspan=3, columnspan=2
                )
                self.status_button.grid(
                    sticky="nsew", column=0, row=3, rowspan=3, columnspan=2
                )

            case STATES.START:
                self.startup_button.grid(
                    sticky="nsew", column=0, row=0, rowspan=6, columnspan=2
                )

            case STATES.DEBUG:
                self.back_button.grid(
                    sticky="nsew", column=0, row=0, rowspan=2, columnspan=1
                )
                self.debug_buzzer_button.grid(
                    sticky="nsew",
                    column=1,
                    row=0,
                    rowspan=2,
                )
                self.debug_zero_mag_button.grid(
                    sticky="nsew", column=0, row=2, rowspan=2
                )
                self.debug_eject_mag_button.grid(
                    sticky="nsew", column=1, row=2, rowspan=2
                )
                self.debug_zero_bed_button.grid(
                    sticky="nsew", column=0, row=4, rowspan=2
                )
                self.debug_show_bed_button.grid(
                    sticky="nsew", column=1, row=4, rowspan=2
                )

            case _ as state:
                logger.warning("unknown state")
                self.state = STATES.EXCEPTION
                self.status.value = f"GUI state {state} unknown".encode()
                self.status_button.configure(text=self.status.value.decode())
                self.state_switch_gui()
