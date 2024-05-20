import tkinter as tk
import winsound
import threading
import time

def on_press(event=None):
    global input_state
    input_state = '1'
    print("input state=", input_state)
    manage_sound()

def on_release(event=None):
    global input_state
    input_state = '0'
    print("input state=", input_state)
    manage_sound()

def manage_sound():
    global beep_thread, input_state
    if input_state == '1' and beep_thread is None:
        beep_thread = threading.Thread(target=beep)
        beep_thread.start()
    elif input_state == '0' and beep_thread is not None:
        beep_thread.do_run = False
        beep_thread.join()
        beep_thread = None

def beep():
    thread = threading.currentThread()
    thread.do_run = True
    while getattr(thread, "do_run", True):
        winsound.Beep(440, 1000)  # Beep for 1000 milliseconds
        time.sleep(0.1)  # Short pause to allow thread to terminate promptly if needed

# Setting up the Tkinter window
root = tk.Tk()
root.title("Beep Controlled by Input State")

input_state = '0'
beep_thread = None

# Creating a button that triggers the beep
button = tk.Button(root, text="Press and Hold for Beep", width=30, height=5)
button.pack(pady=20)

# Binding mouse press and release events
button.bind("<ButtonPress>", on_press)
button.bind("<ButtonRelease>", on_release)

root.mainloop()