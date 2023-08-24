import tkinter as tk
from tkinter import Text, Label, filedialog
import pygame.mixer
import string


class DisappearingTextApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Disappearing Text App")
        pygame.mixer.init()

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
        
        # Define the font sizes
        large_font = ("Arial", 16)
        medium_font = ("Arial", 14)
        small_font = ("Arial", 12)

        # Top Frame for Timer, Word Count & Dropdown
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10, padx=20, fill=tk.X, anchor=tk.N)

        # Timer Label
        self.timer_label = Label(top_frame, text="", font=medium_font)
        self.timer_label.pack(side=tk.LEFT, padx=10)

        # Word Count Label
        self.word_count_label = tk.Label(top_frame, text="", font=medium_font)
        self.word_count_label.pack(side=tk.LEFT, padx=10)

        # Dropdown for timer duration
        timer_options = [5, 10, 15, 20]
        self.timer_var = tk.StringVar(self.root)
        self.timer_var.set(timer_options[0])
        timer_dropdown = tk.OptionMenu(top_frame, self.timer_var, *timer_options, command=self.change_timer_duration)
        timer_dropdown.config(font=small_font)
        timer_dropdown.pack(side=tk.RIGHT, padx=10)

        # Text widget for user input
        self.text_widget = Text(self.root, wrap=tk.WORD, height=20, width=50, font=large_font)
        self.text_widget.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        self.text_widget.bind("<KeyRelease>", self.on_key)

        # Bottom Frame for Buttons
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(pady=10, padx=20, fill=tk.X, anchor=tk.S)

        # Start and Pause buttons
        self.start_button = tk.Button(bottom_frame, text="Start", command=self.start_countdown, font=medium_font)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = tk.Button(bottom_frame, text="Pause", command=self.pause_countdown, font=medium_font)
        self.pause_button.pack(side=tk.LEFT, padx=5)

        # Save button
        save_button = tk.Button(bottom_frame, text="Save", command=self.save_content, font=medium_font)
        save_button.pack(side=tk.LEFT, padx=5)

        # Fullscreen toggle button
        fullscreen_button = tk.Button(bottom_frame, text="Toggle Fullscreen", command=self.toggle_fullscreen, font=medium_font)
        fullscreen_button.pack(side=tk.RIGHT, padx=5)

        self.reset_timer()

        # Disable the text widget initially
        self.text_widget.config(state=tk.DISABLED)


    def on_key(self, event):
        """Callback when a key is pressed. Reset and potentially restart the timer."""

        # List of keysyms for characters that should reset the timer
        valid_keysyms = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789' + string.punctuation)

        # Check if the keysym is valid or if the character is alphanumeric, punctuation, or space
        valid_char = event.char in valid_keysyms or event.char.isspace()

        if valid_char:
            if self.countdown_running:
                if self.remaining_time == 0:
                    self.reset_timer()
                    self.countdown()
                else:
                    self.reset_timer()

            # Update the word count every time a key is pressed
            self.update_word_count()

    def update_word_count(self):
        """Update the word count label."""
        content = self.text_widget.get(1.0, tk.END).strip()
        word_count = len(content.split())
        self.word_count_label.config(text=f"Word Count: {word_count}")

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
            color = "goldenrod"
        else:
            color = "red"
            self.play_timer_tick_sound()
        
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

                self.play_end_tick_sound()

                # Disable the "Start" button and enable the "Pause" button
                self.start_button.config(state=tk.DISABLED)
                self.pause_button.config(state=tk.NORMAL)

                self.word_count_label.config(text=f"Word Count: 0")

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
        self.pause_countdown()
        self.text_widget.config(state=tk.DISABLED)

        # Open a save file dialog
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        
        # If a file path is provided, write the content of the text widget to the file
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_widget.get(1.0, tk.END))

    def toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))

    def play_timer_tick_sound(self):
        pygame.mixer.music.load("./sound_alerts/timer.mp3")
        pygame.mixer.music.play()

    def play_end_tick_sound(self):
        pygame.mixer.music.load("./sound_alerts/end.mp3")
        pygame.mixer.music.play()