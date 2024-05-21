import pyaudio
import numpy as np
import threading
import keyboard
import time

# Define global variables
control_flag = 0
frames = []
store = {"store1": [], "store2": [], "store3": [], "store4": [], "store5": []}
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

def save_recording():
    """Saves the recorded frames and events to the selected storage."""
    global store, frames, events
    storage_key = input("Choose the storage variable (store1, store2, store3, store4, store5): ")
    store[storage_key] = {
        "frames": frames.copy(),
        "events": events.copy()
    }
    frames.clear()
    events.clear()
    print(f"Recording saved in {storage_key}.")

def play_stored_sound():
    """Plays the sound stored in the selected 'store' variable."""
    key = input("Enter the storage key to play (store1, store2, etc.): ")
    if key in store and "frames" in store[key]:
        for frame in store[key]["frames"]:
            stream.write(frame)
        print(f"Finished playing stored sound from {key}.")
    else:
        print("Invalid key or no recording found.")

def main():
    global stream, p, duration

    # Set up the audio stream
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=44100,
                    output=True)

    # Bind spacebar events using the keyboard library
    keyboard.on_press_key("space", lambda _: set_flag(1))
    keyboard.on_release_key("space", lambda _: set_flag(0))

    while True:
        print("\nRecording Session: Enter the duration to record in seconds or type 'exit' to quit.")
        input_duration = input()
        if input_duration.lower() == 'exit':
            break
        duration = float(input_duration)

        global start_time
        start_time = time.time()

        # Start recording and playing sound
        threading.Thread(target=play_and_record).start()
        
        time.sleep(duration)  # Wait for the duration to pass
        save_recording()

        print("\nPlayback Session: Choose an option or type 'skip' to start a new recording.")
        action = input("Type 'play' to playback or 'skip' to continue recording: ")
        if action.lower() == 'play':
            play_stored_sound()

    # Cleanup
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Program terminated.")

if __name__ == "__main__":
    main()