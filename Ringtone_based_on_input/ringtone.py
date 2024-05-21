import pyaudio
import numpy as np
import threading
import keyboard
import time

# Define global variables
control_flag = 0
sound_thread = None
frames = []
store = {"store1": [], "store2": [], "store3": [], "store4": [], "store5": []}
current_store_key = ""
events = []

def set_flag(value):
    """Sets the global control flag for playing sound and logs the event."""
    global control_flag, events
    control_flag = value
    events.append((value, time.time()))
    print(f"Control flag set to {value} at {time.time()}")

def play_and_record():
    """Plays and records the sound based on user control."""
    global stream, frames, start_time, duration
    volume = 0.5  # Range [0.0, 1.0]
    fs = 44100    # Sampling rate, Hz
    f = 440.0     # Sine frequency, Hz
    chunk_duration = 0.1  # Duration in seconds for each chunk
    samples = (np.sin(2*np.pi*np.arange(fs*chunk_duration)*f/fs)).astype(np.float32)

    while time.time() - start_time < duration:
        adjusted_samples = (volume * samples).astype(np.float32) if control_flag == 1 else (np.zeros(int(fs*chunk_duration))).astype(np.float32)
        stream.write(adjusted_samples.tobytes())
        frames.append(adjusted_samples.tobytes())

def setup_recording():
    """Sets up the recording session."""
    global start_time, duration, current_store_key
    duration = float(input("Enter the duration to record in seconds: "))
    current_store_key = input("Choose the storage variable (store1, store2, store3, store4, store5): ")
    start_time = time.time()

def save_recording():
    """Saves the recorded frames and events to the selected storage."""
    global store, current_store_key, frames, events
    store[current_store_key] = {
        "frames": frames.copy(),
        "events": events.copy()
    }
    frames.clear()
    events.clear()

def play_stored_sound(key):
    """Plays the sound stored in the selected 'store' variable."""
    global store, p, stream
    if key in store and "frames" in store[key]:
        for frame in store[key]["frames"]:
            stream.write(frame)

def main():
    global stream, p

    # Set up the audio stream
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=44100,
                    output=True)

    # Bind spacebar events using the keyboard library
    keyboard.on_press_key("space", lambda _: set_flag(1))
    keyboard.on_release_key("space", lambda _: set_flag(0))

    setup_recording()
    
    # Start recording and playing sound
    threading.Thread(target=play_and_record).start()
    
    time.sleep(duration)  # Wait for the duration to pass
    save_recording()

    # User command to play stored sound
    choice = input("Enter the storage key to play (store1, store2, etc.): ")
    play_stored_sound(choice)

    # Cleanup
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Finished playing stored sound.")

if __name__ == "__main__":
    main()
