import customtkinter

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme(
    "blue"
)  # Themes: blue (default), dark-blue, green


class CubePiLerGUI:
    app = None
    frame = None
    button = None
    fullscreen = False

    def __init__(self):
        self.app = customtkinter.CTk()
        self.app.rowconfigure(0, weight=1)
        self.app.columnconfigure(0, weight=1)

        self.frame = customtkinter.CTkFrame(master=self.app, corner_radius=0)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

        self.button = customtkinter.CTkButton(
            master=self.frame,
            text="setup",
            command=self.setup,
            corner_radius=0,
            font=("Consolas", 200),
            fg_color="blue",
            hover_color="blue",
        )
        self.button.grid(sticky="nsew", column=0, row=0)

        self.app.geometry("600x400+0+0")
        self.app.bind("<F11>", self.toggle_fullscreen)
        self.app.after(1, self.toggle_fullscreen)
        self.app.mainloop()

    def toggle_fullscreen(self, x=None):
        self.app.state("normal" if self.fullscreen else "zoomed")
        self.app.attributes("-fullscreen", not self.fullscreen)
        # print(self.app._current_width, self.app._current_height)
        self.fullscreen = not self.fullscreen
        # self.button.configure(
        #     width=self.app._current_width,
        #     height=self.app._current_height,
        # )

    def setup(self, x=None):
        self.button.configure(
            text="start",
            command=self.start,
            fg_color="green",
            hover_color="green",
        )

    def start(self, x=None):
        self.button.configure(
            text="stop",
            command=self.stop,
            fg_color="red",
            hover_color="red",
        )

    def stop(self, x=None):
        self.button.configure(
            text="start",
            command=self.start,
            fg_color="green",
            hover_color="green",
        )

    # Use CTkButton instead of tkinter Button
    # button = customtkinter.CTkButton(
    #     master=app, text="start", command=start
    # )
    # button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)


gui = CubePiLerGUI()
