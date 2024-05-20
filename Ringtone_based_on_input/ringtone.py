import pyaudio
import numpy as np
import threading
import keyboard

def play_sound():
    """Plays a continuous sound based on a global control flag."""
    global stream
    volume = 0.5     # Range [0.0, 1.0]
    fs = 44100       # Sampling rate, Hz
    f = 440.0        # Sine frequency, Hz
    # Reduced chunk duration for quicker response
    duration = 0.1   # Duration in seconds for each chunk
    samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)

    # Play the continuous sound while checking control flag more frequently
    while control_flag == 1:
        stream.write(volume * samples)
        if control_flag != 1:
            break

def main():
    global control_flag, sound_thread, stream, p
    control_flag = 0  # Control flag for playing sound (0 = off, 1 = on)
    sound_thread = None  # Sound thread object

    # Set up the audio stream
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=44100,
                    output=True)

    # Bind spacebar events using the keyboard library
    keyboard.on_press_key("space", lambda _: set_flag(1))
    keyboard.on_release_key("space", lambda _: set_flag(0))

    # Main loop to manage sound based on the control flag
    while True:
        if control_flag == 1 and sound_thread is None:
            # Start the sound thread if not already started
            sound_thread = threading.Thread(target=play_sound)
            sound_thread.start()
        elif control_flag == 0 and sound_thread is not None:
            # Wait for the sound thread to finish if control flag is cleared
            sound_thread.join()
            sound_thread = None

def set_flag(value):
    """Sets the control flag to the specified integer value and prints the status."""
    global control_flag
    control_flag = value
    print(f"Control flag {value}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Clean up on exit
        stream.stop_stream()
        stream.close()
        p.terminate()
        print("Exited gracefully.")
