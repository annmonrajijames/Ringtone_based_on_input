import tkinter as tk
import pyaudio
import threading
import numpy as np

# Function to start playing sound
def play_sound():
    global stream
    volume = 0.5     # range [0.0, 1.0]
    fs = 44100       # sampling rate, Hz
    f = 440.0        # sine frequency, Hz

    # Generate a continuous sine wave
    duration = 1.0   # Duration in seconds for each chunk
    samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)

    # Play the continuous sound
    while True:
        stream.write(volume * samples)
        if not continue_playing.is_set():
            break

# Start or stop sound based on the input
def manage_sound(input):
    global continue_playing, sound_thread, stream, p
    if input == '1' and not continue_playing.is_set():
        continue_playing.set()
        sound_thread = threading.Thread(target=play_sound)
        sound_thread.start()
        print("user input=", input)
    elif input == '0' and continue_playing.is_set():
        continue_playing.clear()
        sound_thread.join()
        print("user input=", input)

# GUI event handlers
def on_press(event=None):
    manage_sound('1')

def on_release(event=None):
    manage_sound('0')

# Set up the audio stream
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=44100,
                output=True)

# Set up the Tkinter window
root = tk.Tk()
root.title("Control Sound with Input")

# Flag and thread initialization
continue_playing = threading.Event()
sound_thread = None

# Create a button that controls the sound
button = tk.Button(root, text="Press and Hold for Sound", width=30, height=5)
button.pack(pady=20)

# Bind button events
button.bind("<ButtonPress>", on_press)
button.bind("<ButtonRelease>", on_release)

root.mainloop()

# Clean up on window close
stream.stop_stream()
stream.close()
p.terminate()
