import tkinter as tk
from tkinter import Text, Label, filedialog

class DisappearingTextApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Disappearing Text App")

        # Initialize values
        self.countdown_running = False # Boolean to check if the timer is running
        self.timer_duration = 5  # Default timer duration
        self.remaining_time = self.timer_duration # Time left on the timer. Initially set to timer_duration
        
        # Set up the GUI
        self.setup_gui()

        # Start the countdown
        self.countdown()

    def setup_gui(self):
        """Set up the GUI components."""
        # Text widget for user input
        self.text_widget = Text(self.root, wrap=tk.WORD, height=20, width=50)
        self.text_widget.pack(pady=20, padx=20)
        self.text_widget.bind("<Key>", self.on_key)

        # Dropdown for timer duration
        timer_options = [5, 10, 15, 20]
        self.timer_var = tk.StringVar(self.root)
        self.timer_var.set(timer_options[0])  # default value
        timer_dropdown = tk.OptionMenu(self.root, self.timer_var, *timer_options, command=self.change_timer_duration)
        timer_dropdown.pack(pady=10)

        # Start and Pause buttons
        self.start_button = tk.Button(self.root, text="Start", command=self.start_countdown)
        self.start_button.pack(pady=10, side=tk.LEFT, padx=5)

        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause_countdown)
        self.pause_button.pack(pady=10, side=tk.LEFT, padx=5)

        # Label for timer
        self.timer_label = Label(self.root, text="")
        self.timer_label.pack(pady=20)

        # Save button
        save_button = tk.Button(self.root, text="Save", command=self.save_content)
        save_button.pack(pady=10, side=tk.LEFT, padx=5)

        self.reset_timer()

        # Disable the text widget initially
        self.text_widget.config(state=tk.DISABLED)

    def on_key(self, event):
        """Callback when a key is pressed. Reset and potentially restart the timer."""
        if self.countdown_running:
            if self.remaining_time == 0:
                self.reset_timer()
                self.countdown()
            else:
                self.reset_timer()

    def reset_timer(self):
        """Reset the countdown timer to the specified duration."""
        self.remaining_time = self.timer_duration
        self.update_timer_label()

    def update_timer_label(self):
        """Update the timer label with the remaining time and adjust its color."""
        self.timer_label.config(text=f"Time remaining: {self.remaining_time}s")
        
        # Determine the color based on the remaining time
        fraction = self.remaining_time / self.timer_duration
        if fraction > 0.5:
            color = "green"
        elif fraction > 0.25:
            color = "yellow"
        else:
            color = "red"
        
        self.timer_label.config(fg=color)


    def countdown(self):
        """Handle the countdown logic and text deletion."""
        if self.countdown_running:
            if self.remaining_time > 0:
                self.remaining_time -= 1
                self.update_timer_label()
                self.root.after(1000, self.countdown)
            else:
                self.text_widget.delete(1.0, tk.END)

                # Disable the "Start" button and enable the "Pause" button
                self.start_button.config(state=tk.DISABLED)
                self.pause_button.config(state=tk.NORMAL)

    def start_countdown(self):
        """Start or resume the countdown."""
        self.reset_timer()
        self.countdown_running = True
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.focus_set()
        self.countdown()

        # Disable the "Start" button and enable the "Pause" button
        self.start_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)

    def pause_countdown(self):
        """Pause the countdown."""
        self.countdown_running = False
        self.text_widget.config(state=tk.DISABLED)

        # Enable the "Start" button and disable the "Pause" button
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)

    def change_timer_duration(self, event):
        """Change the timer duration based on user selection."""
        self.timer_duration = int(self.timer_var.get())
        self.reset_timer()

    def save_content(self):
        """Save the content of the text widget to a file."""
        # Open a save file dialog
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        
        # If a file path is provided, write the content of the text widget to the file
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_widget.get(1.0, tk.END))