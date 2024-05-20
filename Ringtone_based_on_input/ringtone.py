import pyaudio
import numpy as np
import threading
import keyboard

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

def main():
    global continue_playing, sound_thread, stream, p
    continue_playing = threading.Event()
    sound_thread = None

    # Set up the audio stream
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=44100,
                    output=True)

    # Bind spacebar events using the keyboard library
    keyboard.on_press_key("space", lambda _: continue_playing.set() if not continue_playing.is_set() else None)
    keyboard.on_release_key("space", lambda _: continue_playing.clear() if continue_playing.is_set() else None)

    # Start sound thread when spacebar is pressed
    while True:
        if continue_playing.is_set() and sound_thread is None:
            sound_thread = threading.Thread(target=play_sound)
            sound_thread.start()
        elif not continue_playing.is_set() and sound_thread is not None:
            sound_thread.join()
            sound_thread = None

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Clean up on exit
        stream.stop_stream()
        stream.close()
        p.terminate()
        print("Exited gracefully.")