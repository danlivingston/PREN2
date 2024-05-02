import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
buzzer = 11

GPIO.setup(buzzer, GPIO.OUT)


# # Frequencies for the notes
# C4 = 261.63
# D4 = 293.66
# E4 = 329.63
# G4 = 392.00
# A4 = 440.00
# C5 = 523.25

# # Duration of each note (in seconds)
# quarter_note = 0.5
# eighth_note = 0.25

# # Melody and note durations
# melody = [C4, D4, E4, C4, E4, D4, C4, D4, E4, G4, A4, G4, E4, C5, C4]
# durations = [
#     quarter_note,
#     eighth_note,
#     eighth_note,
#     quarter_note,
#     eighth_note,
#     eighth_note,
#     quarter_note,
#     eighth_note,
#     eighth_note,
#     quarter_note,
#     eighth_note,
#     eighth_note,
#     quarter_note,
#     quarter_note,
#     quarter_note,
# ]

# Frequencies for the notes
# D4 = 293.66
# D5 = 587.33
# A4 = 440.00
# A5 = 880.00
# G4 = 392.00
# G5 = 784.00
# F4 = 349.23
# F5 = 698.46
# E4 = 329.63
# E5 = 659.25
# C5 = 523.25

# # Duration of each note (in seconds)
# quarter_note = 0.5
# eighth_note = 0.25
# sixteenth_note = 0.125

# # Melody and note durations for Megalovania
# melody = [D4, D4, D5, A4, A5, G4, G5, F4, F5, E4, E5, D4, D5, C5, D4]
# durations = [
#     sixteenth_note,
#     sixteenth_note,
#     sixteenth_note,
#     sixteenth_note,
#     sixteenth_note,
#     sixteenth_note,
#     sixteenth_note,
#     sixteenth_note,
#     sixteenth_note,
#     sixteenth_note,
#     sixteenth_note,
#     sixteenth_note,
#     sixteenth_note,
#     sixteenth_note,
#     quarter_note,
# ]
# Frequencies for the notes
NOTE_E4 = 329.63
NOTE_G4 = 392.00
NOTE_A4 = 440.00
NOTE_B4 = 493.88
NOTE_C5 = 523.25
NOTE_D5 = 587.33
NOTE_E5 = 659.25
NOTE_F5 = 698.46
NOTE_G5 = 784.00
REST = 1.0

# Duration of each note (in seconds)
whole_note = 1.0
half_note = 0.5
quarter_note = 0.25
eighth_note = 0.125
melody = [
    NOTE_E4,
    NOTE_G4,
    NOTE_A4,
    NOTE_A4,
    REST,
    NOTE_A4,
    NOTE_B4,
    NOTE_C5,
    NOTE_C5,
    REST,
    NOTE_C5,
    NOTE_D5,
    NOTE_B4,
    NOTE_B4,
    REST,
    NOTE_A4,
    NOTE_G4,
    NOTE_A4,
    REST,
    NOTE_E4,
    NOTE_G4,
    NOTE_A4,
    NOTE_A4,
    REST,
    NOTE_A4,
    NOTE_B4,
    NOTE_C5,
    NOTE_C5,
    REST,
    NOTE_C5,
    NOTE_D5,
    NOTE_B4,
    NOTE_B4,
    REST,
    NOTE_A4,
    NOTE_G4,
    NOTE_A4,
    REST,
    NOTE_E4,
    NOTE_G4,
    NOTE_A4,
    NOTE_A4,
    REST,
    NOTE_A4,
    NOTE_C5,
    NOTE_D5,
    NOTE_D5,
    REST,
    NOTE_D5,
    NOTE_E5,
    NOTE_F5,
    NOTE_F5,
    REST,
    NOTE_E5,
    NOTE_D5,
    NOTE_E5,
    NOTE_A4,
    REST,
    NOTE_A4,
    NOTE_B4,
    NOTE_C5,
    NOTE_C5,
    REST,
    NOTE_D5,
    NOTE_E5,
    NOTE_A4,
    REST,
    NOTE_A4,
    NOTE_C5,
    NOTE_B4,
    NOTE_B4,
    REST,
    NOTE_C5,
    NOTE_A4,
    NOTE_B4,
    REST,
    NOTE_A4,
    NOTE_A4,
    NOTE_A4,
    NOTE_B4,
    NOTE_C5,
    NOTE_C5,
    REST,
    NOTE_C5,
    NOTE_D5,
    NOTE_B4,
    NOTE_B4,
    REST,
    NOTE_A4,
    NOTE_G4,
    NOTE_A4,
    REST,
    NOTE_E4,
    NOTE_G4,
    NOTE_A4,
    NOTE_A4,
    REST,
    NOTE_A4,
    NOTE_B4,
    NOTE_C5,
    NOTE_C5,
    REST,
    NOTE_C5,
    NOTE_D5,
    NOTE_B4,
    NOTE_B4,
    REST,
    NOTE_A4,
    NOTE_G4,
    NOTE_A4,
    REST,
    NOTE_E4,
    NOTE_G4,
    NOTE_A4,
    NOTE_A4,
    REST,
    NOTE_A4,
    NOTE_C5,
    NOTE_D5,
    NOTE_D5,
    REST,
    NOTE_D5,
    NOTE_E5,
    NOTE_F5,
    NOTE_F5,
    REST,
    NOTE_E5,
    NOTE_D5,
    NOTE_E5,
    NOTE_A4,
    REST,
    NOTE_A4,
    NOTE_B4,
    NOTE_C5,
    NOTE_C5,
    REST,
    NOTE_D5,
    NOTE_E5,
    NOTE_A4,
    REST,
    NOTE_A4,
    NOTE_C5,
    NOTE_B4,
    NOTE_B4,
    REST,
    NOTE_C5,
    NOTE_A4,
    NOTE_B4,
    REST,
    NOTE_E5,
    REST,
    REST,
    NOTE_F5,
    REST,
    REST,
    NOTE_E5,
    NOTE_E5,
    REST,
    NOTE_G5,
    REST,
    NOTE_E5,
    NOTE_D5,
    REST,
    REST,
    NOTE_D5,
    REST,
    REST,
    NOTE_C5,
    REST,
    REST,
    NOTE_B4,
    NOTE_C5,
    REST,
    NOTE_B4,
    REST,
    NOTE_A4,
    NOTE_E5,
    REST,
    REST,
    NOTE_F5,
    REST,
    REST,
    NOTE_E5,
    NOTE_E5,
    REST,
    NOTE_G5,
    REST,
    NOTE_E5,
    NOTE_D5,
    REST,
    REST,
    NOTE_D5,
    REST,
    REST,
    NOTE_C5,
    REST,
    REST,
    NOTE_B4,
    NOTE_C5,
    REST,
    NOTE_B4,
    REST,
    NOTE_A4,
]
durations = [
    eighth_note,
    eighth_note,
    quarter_note,
    eighth_note,
    eighth_note,
    eighth_note,
    eighth_note,
    quarter_note,
    eighth_note,
    eighth_note,
    eighth_note,
    eighth_note,
    quarter_note,
    eighth_note,
    eighth_note,
    eighth_note,
    eighth_note,
    quarter_note,
    eighth_note,
    eighth_note,
    eighth_note,
    quarter_note,
    eighth_note,
    eighth_note,
    eighth_note,
    eighth_note,
    quarter_note,
    eighth_note,
    eighth_note,
    eighth_note,
    eighth_note,
    quarter_note,
    eighth_note,
    eighth_note,
    eighth_note,
    eighth_note,
    quarter_note,
    eighth_note,
    eighth_note,
    eighth_note,
    quarter_note,
    eighth_note,
    eighth_note,
    eighth_note,
    eighth_note,
    quarter_note,
    eighth_note,
    eighth_note,
    eighth_note,
    eighth_note,
    quarter_note,
    eighth_note,
    eighth_note,
    eighth_note,
    eighth_note,
    eighth_note,
    quarter_note,
    eighth_note,
    eighth_note,
    eighth_note,
    quarter_note,
    eighth_note,
    eighth_note,
    quarter_note,
    eighth_note,
    quarter_note,
    eighth_note,
    eighth_note,
    eighth_note,
    quarter_note,
    eighth_note,
    eighth_note,
    eighth_note,
    eighth_note,
    quarter_note,
    quarter_note,
    quarter_note,
    eighth_note,
    eighth_note,
    eighth_note,
    quarter_note,
    eighth_note,
    eighth_note,
    eighth_note,
    eighth_note,
    quarter_note,
    eighth_note,
    eighth_note,
    eighth_note,
    eighth_note,
    quarter_note,
    eighth_note,
    eighth_note,
    eighth_note,
    quarter_note,
    eighth_note,
    eighth_note,
    eighth_note,
    eighth_note,
    quarter_note,
    eighth_note,
    eighth_note,
    eighth_note,
    eighth_note,
    quarter_note,
    eighth_note,
    eighth_note,
    eighth_note,
    eighth_note,
    quarter_note,
    eighth_note,
    eighth_note,
    eighth_note,
    quarter_note,
    eighth_note,
    eighth_note,
    eighth_note,
    eighth_note,
    quarter_note,
    eighth_note,
    eighth_note,
    eighth_note,
    eighth_note,
    quarter_note,
    eighth_note,
    eighth_note,
    eighth_note,
    eighth_note,
    eighth_note,
    quarter_note,
    eighth_note,
    eighth_note,
    eighth_note,
    quarter_note,
    eighth_note,
    eighth_note,
    quarter_note,
    eighth_note,
    quarter_note,
    eighth_note,
    eighth_note,
    eighth_note,
    quarter_note,
    eighth_note,
    eighth_note,
    eighth_note,
    eighth_note,
    quarter_note,
    quarter_note,
    quarter_note,
    eighth_note,
    quarter_note,
    quarter_note,
    eighth_note,
    quarter_note,
    eighth_note,
    eighth_note,
    eighth_note,
    eighth_note,
    eighth_note,
    eighth_note,
    eighth_note,
    eighth_note,
    quarter_note,
    quarter_note,
    eighth_note,
    quarter_note,
    quarter_note,
    eighth_note,
    quarter_note,
    eighth_note,
    eighth_note,
    eighth_note,
    eighth_note,
    eighth_note,
    half_note,
    quarter_note,
    eighth_note,
    quarter_note,
    quarter_note,
    eighth_note,
    quarter_note,
    eighth_note,
    eighth_note,
    eighth_note,
    eighth_note,
    eighth_note,
    eighth_note,
    eighth_note,
    eighth_note,
    quarter_note,
    quarter_note,
    eighth_note,
    quarter_note,
    quarter_note,
    eighth_note,
    quarter_note,
    eighth_note,
    eighth_note,
    eighth_note,
    eighth_note,
    eighth_note,
    half_note,
]


def play_note(freq, duration):
    delay = 1.0 / freq
    num_cycles = int(freq * duration)

    for _ in range(num_cycles):
        GPIO.output(buzzer, True)
        time.sleep(delay)
        GPIO.output(buzzer, False)
        time.sleep(delay)


def play_melody():
    for freq, duration in zip(melody, durations):
        play_note(freq, duration)


def sound_start(freq):
    i = 0
    delay = 0.5 / freq
    while i < 70:
        GPIO.output(buzzer, whole_note)
        time.sleep(delay)
        GPIO.output(buzzer, 0)
        time.sleep(delay)
        i += whole_note
    delay = delay / 10
    i = 0
    while i < 300:
        GPIO.output(buzzer, whole_note)
        time.sleep(delay)
        GPIO.output(buzzer, 0)
        time.sleep(delay)
        i += whole_note


def sound_stop(freq):
    i = 0
    delay = 0.05 / freq
    while i < 300:
        GPIO.output(buzzer, whole_note)
        time.sleep(delay)
        GPIO.output(buzzer, 0)
        time.sleep(delay)
        i += whole_note
    delay = 0.5 / freq
    i = 0
    while i < 70:
        GPIO.output(buzzer, whole_note)
        time.sleep(delay)
        GPIO.output(buzzer, 0)
        time.sleep(delay)
        i += whole_note


# sound_start(600)
# time.sleep(whole_note)
# sound_stop(600)


def sound_cleanup():
    GPIO.cleanup()
