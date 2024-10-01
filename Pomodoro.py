import tkinter as tk
import time
import json
from playsound import playsound  # Import playsound for playing sound
import matplotlib.pyplot as plt
from datetime import datetime

# Constants for timings
SESSION_DURATION = 25 * 60  # 25 minutes in seconds
SHORT_BREAK_DURATION = 5 * 60  # 5 minutes in seconds
LONG_BREAK_DURATION = 15 * 60  # 15 minutes in seconds
DATA_FILE = 'study_data.json'  # JSON file to store study hours

# Customize colors and fonts
BACKGROUND_COLOR = "#f0f8ff"  # Light blue background
FONT_COLOR = "#333"  # Dark text
BUTTON_COLOR = "#4caf50"  # Green buttons
BUTTON_HOVER_COLOR = "#45a049"  # Darker green for hover
FONT_NAME = "Helvetica"  # Font style
BUTTON_FONT = (FONT_NAME, 14)  # Button font size
TIMER_FONT = (FONT_NAME, 48)  # Timer font size

# Path to the bird chirping sound
BIRD_SOUND_PATH = r"P:\birds-flapmp3-14504.mp3"


class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("500x400")  # Adjusted window size for better appearance
        self.root.config(bg=BACKGROUND_COLOR)  # Set background color
        self.is_running = False
        self.is_paused = False
        self.remaining_time = SESSION_DURATION
        self.session_count = 0
        
        # Timer label
        self.timer_label = tk.Label(root, text="Time left: 25:00", font=TIMER_FONT, bg=BACKGROUND_COLOR, fg=FONT_COLOR)
        self.timer_label.pack(pady=20)

        # Frame for buttons
        self.button_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
        self.button_frame.pack(pady=20)

        # Start button
        self.start_button = tk.Button(self.button_frame, text="Start", command=self.start_timer, font=BUTTON_FONT, bg=BUTTON_COLOR, fg="white", activebackground=BUTTON_HOVER_COLOR, width=10)
        self.start_button.grid(row=0, column=0, padx=10)

        # Stop button
        self.stop_button = tk.Button(self.button_frame, text="Stop", command=self.stop_timer, font=BUTTON_FONT, bg=BUTTON_COLOR, fg="white", activebackground=BUTTON_HOVER_COLOR, width=10)
        self.stop_button.grid(row=0, column=1, padx=10)

        # Pause/Resume button
        self.pause_resume_button = tk.Button(self.button_frame, text="Pause", command=self.pause_resume_timer, font=BUTTON_FONT, bg=BUTTON_COLOR, fg="white", activebackground=BUTTON_HOVER_COLOR, width=10)
        self.pause_resume_button.grid(row=0, column=2, padx=10)

        self.log_button = tk.Button(self.button_frame, text="Log Study Hours", command=self.plot_study_hours, font=BUTTON_FONT, bg=BUTTON_COLOR, fg="white", activebackground=BUTTON_HOVER_COLOR, width=15)
        self.log_button.grid(row=1, column=0, pady=10)

        self.timer_running_id = None  # Timer ID for after method

    def play_alarm(self):
        """Play the bird chirping sound."""
        playsound(BIRD_SOUND_PATH)

    def log_study_hours(self, hours):
        """Log daily study hours into a JSON file."""
        today = datetime.now().date().isoformat()
        
        # Load existing data
        try:
            with open(DATA_FILE, 'r') as file:
                study_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            study_data = {}
        
        # Update today's study hours
        study_data[today] = study_data.get(today, 0) + hours
        print(f"Logging study hours for {today}: {study_data[today]} hours")  # Debugging line

        # Write back to the file
        with open(DATA_FILE, 'w') as file:
            json.dump(study_data, file)


    def plot_study_hours(self):
        """Plot the study hours using matplotlib."""
        try:
            with open(DATA_FILE, 'r') as file:
                study_data = json.load(file)
            
            dates = list(study_data.keys())
            hours = list(study_data.values())

            plt.figure(figsize=(10, 5))
            plt.plot(dates, hours, marker='o', color='#4caf50')  # Green line
            plt.title('Daily Study Hours', fontsize=16)
            plt.xlabel('Date', fontsize=14)
            plt.ylabel('Hours Studied', fontsize=14)
            plt.xticks(rotation=45)
            plt.grid()
            plt.tight_layout()
            plt.show()
        except (FileNotFoundError, json.JSONDecodeError):
            print("No study data found.")

    def countdown_timer(self):
        """Countdown timer to display remaining time."""
        if self.remaining_time >= 0 and self.is_running:
            mins, secs = divmod(self.remaining_time, 60)
            timer_format = '{:02d}:{:02d}'.format(mins, secs)
            self.timer_label.config(text=f"Time left: {timer_format}")
            self.remaining_time -= 1  # Decrease the time remaining
            self.timer_running_id = self.root.after(1000, self.countdown_timer)  # Call countdown_timer every second
        elif self.is_running:
            self.play_alarm()  # Play bird chirping sound at the end of session
            self.session_count += 1
            self.log_study_hours(SESSION_DURATION / 3600)  # Log hours studied
        
            # Decide on break duration
            if self.session_count % 4 == 0:
                self.start_break(LONG_BREAK_DURATION)
            else:
                self.start_break(SHORT_BREAK_DURATION)

    def start_break(self, duration):
        """Start a break session."""
        self.timer_label.config(text="Break time!", fg="#ff5722")  # Change text color for break
        self.root.update()
        self.remaining_time = duration
        self.countdown_timer()

    def start_timer(self):
        """Start the timer."""
        if not self.is_running:
            self.is_running = True
            self.play_alarm()  # Play bird chirping sound at the start of session
            self.remaining_time = SESSION_DURATION
            self.countdown_timer()
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.pause_resume_button.config(state=tk.NORMAL)

    def stop_timer(self):
        """Stop the timer."""
        self.is_running = False
        if self.timer_running_id is not None:
            self.root.after_cancel(self.timer_running_id)
            self.timer_running_id = None
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.pause_resume_button.config(state=tk.DISABLED)
        self.timer_label.config(text="Time left: 25:00")  # Reset timer display

    def pause_resume_timer(self):
        """Pause or resume the timer."""
        if self.is_running:
            if not self.is_paused:
                self.is_paused = True
                self.pause_resume_button.config(text="Resume")
                if self.timer_running_id is not None:
                    self.root.after_cancel(self.timer_running_id)  # Stop the countdown
                    self.timer_running_id = None
            else:
                self.is_paused = False
                self.pause_resume_button.config(text="Pause")
                self.countdown_timer()  # Resume countdown

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
