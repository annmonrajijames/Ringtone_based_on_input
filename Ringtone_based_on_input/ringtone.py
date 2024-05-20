import tkinter as tk
import winsound
import threading

def on_press(event=None):
    global beep_thread
    beep_thread = threading.Thread(target=beep)
    beep_thread.start()
    print("Button pressed (1)")

def on_release(event=None):
    global beep_thread
    beep_thread.do_run = False
    beep_thread.join()
    print("Button released (0)")

def beep():
    thread = threading.currentThread()
    thread.do_run = True
    while getattr(thread, "do_run", True):
        winsound.Beep(440, 100)  # 440 Hz for 100 milliseconds

# Setting up the Tkinter window
root = tk.Tk()
root.title("Beep on Button Hold")

beep_thread = None

# Creating a button that triggers the beep
button = tk.Button(root, text="Press and Hold", width=30, height=5)
button.pack(pady=20)

# Binding mouse press and release events
button.bind("<ButtonPress>", on_press)
button.bind("<ButtonRelease>", on_release)

root.mainloop()