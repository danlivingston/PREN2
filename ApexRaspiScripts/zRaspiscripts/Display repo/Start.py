import os
import subprocess
import tkinter as tk

# Directory containing the file to be executed
# Replace this with the path to your directory
file_directory = "/home/Display/Desktop/Demo/Testaufbau"


def start_file():
    global process
    # Change to the directory where the file is located
    os.chdir(file_directory)
    # Replace 'Testaufbau_Programm.py' with the name of the file you want to start
    process = subprocess.Popen(["python", "Testaufbau_Programm.py"])


def stop_file():
    if process:
        process.terminate()


# Set up the main window
root = tk.Tk()
root.title("TALIS")

# Define button size and font
button_font = ("Arial", 400)  # Adjust the font size as needed
button_width = 100  # Adjust the button width as needed
button_height = 20  # Adjust the button height as needed

# Create and place the Start button
start_button = tk.Button(
    root,
    text="Start",
    command=start_file,
    bg="green",
    font=button_font,
    width=button_width,
    height=button_height,
)
start_button.pack(side=tk.LEFT, padx=10, pady=10)


# Start the Tkinter event loop
root.mainloop()
