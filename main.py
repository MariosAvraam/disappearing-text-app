import tkinter as tk
from tkinter import Text, Label

def on_key(event):
    """Callback when a key is pressed. We'll use this to reset and potentially restart the timer."""
    global remaining_time
    
    # If the timer has reached 0, we need to restart the countdown
    if remaining_time == 0:
        reset_timer()
        countdown()
    else:
        reset_timer()


def reset_timer():
    global remaining_time
    remaining_time = 5
    update_timer_label()

def update_timer_label():
    timer_label.config(text=f"Time remaining: {remaining_time}s")

def countdown():
    global remaining_time
    if remaining_time > 0:
        remaining_time -= 1
        update_timer_label()
        root.after(1000, countdown)
    else:
        text_widget.delete(1.0, tk.END)

root = tk.Tk()
root.title("Disappearing Text App")

text_widget = Text(root, wrap=tk.WORD, height=20, width=50)
text_widget.pack(pady=20, padx=20)
text_widget.bind("<Key>", on_key)

timer_label = Label(root, text="")
timer_label.pack(pady=20)
reset_timer()

countdown()
root.mainloop()
