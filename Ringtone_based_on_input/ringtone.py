import pyaudio
import numpy as np
import threading
import keyboard
import time

def play_and_record():
    """Plays and records a continuous sound based on a global control flag."""
    global stream, recorded_data
    volume = 0.5
    fs = 44100
    f = 440.0
    duration = 0.1
    samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)
    
    start_time = time.time()
    while time.time() - start_time < record_duration:
        if control_flag == 1:
            stream.write(volume * samples)
            recorded_data = np.append(recorded_data, volume * samples)  # Append recorded data
        else:
            # Write silence if no key is pressed
            silence = np.zeros_like(samples)
            stream.write(silence)
            recorded_data = np.append(recorded_data, silence)
        if record_duration and time.time() - start_time >= record_duration:
            break

def replay_recorded_sound():
    """Replays the recorded sound."""
    global stream, recorded_data
    stream.write(recorded_data.tobytes())

def main():
    global control_flag, sound_thread, stream, p, recorded_data, record_duration
    control_flag = 0
    sound_thread = None
    recorded_data = np.array([], dtype=np.float32)
    
    # Set up the audio stream
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=44100,
                    output=True)

    # User input for duration
    record_duration = float(input("Enter duration to record in seconds: "))
    
    # Bind spacebar events using the keyboard library
    keyboard.on_press_key("space", lambda _: set_flag(1))
    keyboard.on_release_key("space", lambda _: set_flag(0))

    # Start recording and playing thread
    sound_thread = threading.Thread(target=play_and_record)
    sound_thread.start()
    sound_thread.join()

    # Replay or save logic here
    print("Replaying recorded sound...")
    replay_recorded_sound()

def set_flag(value):
    """Sets the control flag to the specified integer value."""
    global control_flag
    control_flag = value

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Clean up on exit
        stream.stop_stream()
        stream.close()
        p.terminate()
        print("Exited gracefully.")
