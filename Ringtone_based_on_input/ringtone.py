import pyaudio
import numpy as np
import threading
import keyboard
import time

def set_flag(value):
    """Sets the global control flag for playing sound."""
    global control_flag
    control_flag = value
    print(f"Control flag set to {value}")

def play_and_record():
    """Plays and records the sound based on user control."""
    global stream, frames, start_time, duration, silent_samples
    volume = 0.5     # Range [0.0, 1.0]
    fs = 44100       # Sampling rate, Hz
    f = 440.0        # Sine frequency, Hz
    chunk_duration = 0.1   # Duration in seconds for each chunk
    samples = (np.sin(2*np.pi*np.arange(fs*chunk_duration)*f/fs)).astype(np.float32)
    silent_samples = (np.zeros(int(fs*chunk_duration))).astype(np.float32)

    while time.time() - start_time < duration:
        if control_flag == 1:
            adjusted_samples = (volume * samples).astype(np.float32)
            stream.write(adjusted_samples.tobytes())
            frames.append(adjusted_samples.tobytes())
        else:
            adjusted_silent_samples = (volume * silent_samples).astype(np.float32)
            stream.write(adjusted_silent_samples.tobytes())
            frames.append(adjusted_silent_samples.tobytes())

def play_stored_sound():
    """Plays the sound stored in the 'store' variable."""
    global store, p
    for frame in store:
        stream.write(frame)

def main():
    global control_flag, sound_thread, stream, frames, store, start_time, duration
    control_flag = 0  # Control flag for playing sound (0 = off, 1 = on)
    frames = []  # Storage for recorded frames

    duration = float(input("Enter the duration to record in seconds: "))

    # Set up the audio stream
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=44100,
                    output=True)

    # Bind spacebar events using the keyboard library
    keyboard.on_press_key("space", lambda _: set_flag(1))
    keyboard.on_release_key("space", lambda _: set_flag(0))

    start_time = time.time()

    # Start recording and playing sound
    sound_thread = threading.Thread(target=play_and_record)
    sound_thread.start()
    sound_thread.join()

    # Store the recorded frames for later playback
    store = frames.copy()

    # User command to play stored sound
    input("Press Enter to play the stored sound...")
    play_stored_sound()

    # Cleanup
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Finished playing stored sound.")

if __name__ == "__main__":
    main()
