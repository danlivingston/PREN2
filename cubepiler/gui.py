import asyncio
import multiprocessing as mp
import platform
from enum import Enum

import customtkinter
from loguru import logger

# from cubepiler import runner
global runner

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")
# TODO: reduce to used fonts only
# customtkinter.FontManager.load_font("fonts/SourceCodePro-Black.ttf")
# customtkinter.FontManager.load_font("fonts/SourceCodePro-ExtraBold.ttf")
# customtkinter.FontManager.load_font("fonts/SourceCodePro-Bold.ttf")
customtkinter.FontManager.load_font("fonts/SourceCodePro-SemiBold.ttf")
customtkinter.FontManager.load_font("fonts/SourceCodePro-Regular.ttf")
# customtkinter.FontManager.load_font("fonts/SourceCodePro-Medium.ttf")
# customtkinter.FontManager.load_font("fonts/SourceCodePro-Light.ttf")
# customtkinter.FontManager.load_font("fonts/SourceCodePro-ExtraLight.ttf")

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
        "RESETTING",
        "RUNNING",
        "EXCEPTION",
        "SUCCESS",
        "ABORTED",
        "DEBUG",
        "STOP",
    ],
)


# TODO import stuff during init phase of gui
class CubePiLerGUI(customtkinter.CTk):
    def __init__(self, loop, autofullscreen=True):
        self.state = STATES.START
        self.status = mp.Array("c", 200)
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
        if autofullscreen:
            # for use on pi for auto fullscreen when it starts; can disable for development in .env
            self.root.after(1, lambda: self.loop.create_task(self.toggle_fullscreen()))
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

        button_font = customtkinter.CTkFont(family="Source Code Pro SemiBold", size=40)
        progress_bar_font = customtkinter.CTkFont(family="Source Code Pro", size=30)

        self.start_button = customtkinter.CTkButton(
            master=self.frame,
            text="start",
            command=lambda: setattr(
                self, "running_task", self.loop.create_task(self.start_build())
            ),
            corner_radius=0,
            font=button_font,
            fg_color=COLORS["green"],
            hover_color=COLORS["green"],
            text_color=COLORS["white"],
        )

        self.stop_button = customtkinter.CTkButton(
            master=self.frame,
            text="cancel",
            command=lambda: self.loop.create_task(self.cancel_build()),
            corner_radius=0,
            font=button_font,
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
            font=button_font,
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
            font=button_font,
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
            font=button_font,
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
            font=button_font,
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
            font=button_font,
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
            font=button_font,
            fg_color=COLORS["red"],
            hover_color=COLORS["red"],
            text_color=COLORS["white"],
        )

        self.back_button = customtkinter.CTkButton(
            master=self.frame,
            text="BACK",
            command=lambda: setattr(
                self, "running_task", self.loop.create_task(self.dismiss_button())
            ),
            corner_radius=0,
            font=button_font,
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
            font=button_font,
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
            font=button_font,
            fg_color=COLORS["red"],
            hover_color=COLORS["red"],
            text_color=COLORS["white"],
        )

        self.startup_button = customtkinter.CTkButton(
            master=self.frame,
            text="INITIALIZING...",
            corner_radius=0,
            font=progress_bar_font,
            fg_color=COLORS["black"],
            hover_color=COLORS["black"],
            text_color=COLORS["white"],
        )

        self.status_button = customtkinter.CTkButton(
            master=self.frame,
            text="LOREM",
            corner_radius=0,
            font=progress_bar_font,
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

        # self.progress_label = customtkinter.CTkLabel(
        #     master=self.frame,
        #     text="...",
        #     fg_color=COLORS["black"],
        #     text_color=COLORS["white"],
        #     font=progress_bar_font,
        # )

    async def mainloop(self):
        # shows gui as early as possbile
        logger.debug("initializing")
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
        await self.cancel_build()
        self.state = STATES.STOP

    async def start_build(self, event=None):
        p = None

        self.status.value = b"starting"

        try:
            if not self.state == STATES.READY:
                return
            self.state = STATES.RUNNING
            self.state_switch_gui()
            p = mp.Process(
                target=runner.run_mp, args=(self.status,), name="build runner"
            )
            p.start()
            while p.is_alive():
                self.status_button.configure(text=self.status.value.decode())
                await asyncio.sleep(0.1)
            self.state = STATES.SUCCESS
            self.status_button.configure(text=self.status.value.decode())
        except asyncio.CancelledError:
            if p is not None and p.is_alive():
                p.kill()
                p.join()
            logger.debug("cancelled build")
            self.state = STATES.READY  # TODO aborted status
        except Exception as e:
            logger.exception(e)
            self.state = STATES.EXCEPTION
        finally:
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
        p = None
        try:
            if not self.state == STATES.READY:
                return
            self.state = STATES.RESETTING
            self.state_switch_gui()
            p = mp.Process(target=runner.reset_mp, name="reset runner")
            p.start()
            while p.is_alive():
                await asyncio.sleep(0.1)
            self.state = STATES.SUCCESS
        except asyncio.CancelledError:
            if p is not None and p.is_alive():
                p.kill()
                p.join()
            logger.debug("cancelled reset")
            self.state = STATES.READY  # TODO aborted status
        except Exception as e:
            logger.exception(e)
            self.state = STATES.EXCEPTION
        finally:
            self.state_switch_gui()

    async def start_zero_mag(self, event=None):
        p = None

        self.status.value = b"starting"

        try:
            if not self.state == STATES.DEBUG:
                return
            self.state = STATES.RUNNING
            self.state_switch_gui()
            p = mp.Process(
                target=runner.zero_mag, args=(self.status,), name="zero mag runner"
            )
            p.start()
            while p.is_alive():
                self.status_button.configure(text=self.status.value.decode())
                await asyncio.sleep(0.1)
            self.state = STATES.DEBUG
        except asyncio.CancelledError:
            if p is not None and p.is_alive():
                p.kill()
                p.join()
            logger.debug("cancelled")
            self.state = STATES.READY  # TODO aborted status
        except Exception as e:
            logger.exception(e)
            self.state = STATES.EXCEPTION
        finally:
            self.state_switch_gui()

    async def start_zero_bed(self, event=None):
        p = None

        self.status.value = b"starting"

        try:
            if not self.state == STATES.DEBUG:
                return
            self.state = STATES.RUNNING
            self.state_switch_gui()
            p = mp.Process(
                target=runner.zero_bed, args=(self.status,), name="zero bed runner"
            )
            p.start()
            while p.is_alive():
                self.status_button.configure(text=self.status.value.decode())
                await asyncio.sleep(0.1)
            self.state = STATES.DEBUG
        except asyncio.CancelledError:
            if p is not None and p.is_alive():
                p.kill()
                p.join()
            logger.debug("cancelled")
            self.state = STATES.READY  # TODO aborted status
        except Exception as e:
            logger.exception(e)
            self.state = STATES.EXCEPTION
        finally:
            self.state_switch_gui()

    async def start_show_bed(self, event=None):
        p = None

        self.status.value = b"starting"

        try:
            if not self.state == STATES.DEBUG:
                return
            self.state = STATES.RUNNING
            self.state_switch_gui()
            p = mp.Process(
                target=runner.show_bed, args=(self.status,), name="show bed runner"
            )
            p.start()
            while p.is_alive():
                self.status_button.configure(text=self.status.value.decode())
                await asyncio.sleep(0.1)
            self.state = STATES.DEBUG
        except asyncio.CancelledError:
            if p is not None and p.is_alive():
                p.kill()
                p.join()
            logger.debug("cancelled")
            self.state = STATES.READY  # TODO aborted status
        except Exception as e:
            logger.exception(e)
            self.state = STATES.EXCEPTION
        finally:
            self.state_switch_gui()

    async def start_eject_mag(self, event=None):
        p = None

        self.status.value = b"starting"

        try:
            if not self.state == STATES.DEBUG:
                return
            self.state = STATES.RUNNING
            self.state_switch_gui()
            p = mp.Process(
                target=runner.eject_mag, args=(self.status,), name="eject mag runner"
            )
            p.start()
            while p.is_alive():
                self.status_button.configure(text=self.status.value.decode())
                await asyncio.sleep(0.1)
            self.state = STATES.DEBUG
        except asyncio.CancelledError:
            if p is not None and p.is_alive():
                p.kill()
                p.join()
            logger.debug("cancelled")
            self.state = STATES.READY  # TODO aborted status
        except Exception as e:
            logger.exception(e)
            self.state = STATES.EXCEPTION
        finally:
            self.state_switch_gui()

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
        # self.progress_label.grid_remove()
        self.startup_button.grid_remove()
        self.status_button.grid_remove()
        self.progress_bar.grid_remove()
        self.progress_bar.stop()
        self.debug_eject_mag_button.grid_remove()
        self.debug_show_bed_button.grid_remove()
        self.debug_zero_bed_button.grid_remove()
        self.debug_zero_mag_button.grid_remove()

    def state_switch_gui(self):
        # ? TODO: Aborted Screen
        # ? TODO: Starting Screen
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
            case STATES.RUNNING | STATES.RESETTING:
                self.stop_button.grid(
                    sticky="nsew", column=0, row=0, rowspan=3, columnspan=2
                )
                self.status_button.grid(
                    sticky="nsew", column=0, row=3, rowspan=2, columnspan=2
                )
                self.progress_bar.grid(
                    sticky="nsew", column=0, row=5, rowspan=1, columnspan=2
                )
                self.progress_bar.start()
            case STATES.SUCCESS:
                self.success_button.grid(
                    sticky="nsew", column=0, row=0, rowspan=3, columnspan=1
                )
                self.back_button.grid(
                    sticky="nsew", column=1, row=0, rowspan=3, columnspan=1
                )
                self.status_button.grid(
                    sticky="nsew", column=0, row=3, rowspan=3, columnspan=2
                )
                # self.progress_label.grid(
                #     sticky="nsew", column=0, row=3, rowspan=3, columnspan=2
                # )
            case STATES.EXCEPTION:
                self.exception_button.grid(
                    sticky="nsew", column=0, row=0, rowspan=2, columnspan=2
                )
            case STATES.START:
                self.startup_button.grid(
                    sticky="nsew", column=0, row=0, rowspan=6, columnspan=2
                )
            case STATES.DEBUG:
                self.back_button.grid(
                    sticky="nsew", column=0, row=0, rowspan=2, columnspan=2
                )
                # self.startup_button.grid(sticky="nsew", column=1, row=0, rowspan=2)
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
            case _:
                logger.warning("unknown state")
                self.state = STATES.EXCEPTION
                self.state_switch_gui()
