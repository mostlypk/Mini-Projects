import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import scrolledtext
from tkcalendar import Calendar
import winsound  # For Windows sound notification

DATA_FILE = "mood_diary.json"

# Mood options and their color coding
MOOD_OPTIONS = {
    "Angry": "red",
    "Sad": "blue",
    "Exhausted": "gray",
    "Happy": "yellow",
    "Overwhelmed": "orange",
    "Content": "green"
}

# Change this path to your own sound file
NOTIFICATION_SOUND = "your_notification_sound.wav"  # Add a sound file in your directory

def load_entries():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

def save_entries(entries):
    with open(DATA_FILE, "w") as file:
        json.dump(entries, file, indent=4)

class MoodDiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mood Diary")
        self.entries = load_entries()
        
        self.setup_ui()

    def setup_ui(self):
        self.root.configure(bg="#f0f8ff")  # Light blue background
        
        # Frame for displaying entries
        self.entry_frame = tk.Frame(self.root, bg="#f0f8ff")
        self.entry_frame.pack(pady=10)

        self.display_text = scrolledtext.ScrolledText(self.entry_frame, width=50, height=10, wrap=tk.WORD, bg="#ffffff", fg="#000000", font=("Arial", 12))
        self.display_text.pack(padx=10)

        self.view_button = tk.Button(self.root, text="View Entries", command=self.display_entries, bg="#add8e6", font=("Arial", 12))
        self.view_button.pack(pady=5)

        self.add_button = tk.Button(self.root, text="Add Entry", command=self.add_entry, bg="#add8e6", font=("Arial", 12))
        self.add_button.pack(pady=5)

        self.calendar_button = tk.Button(self.root, text="Show Calendar", command=self.show_calendar, bg="#add8e6", font=("Arial", 12))
        self.calendar_button.pack(pady=5)

        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.quit, bg="#ffcccb", font=("Arial", 12))
        self.exit_button.pack(pady=5)

    def display_entries(self):
        self.display_text.delete(1.0, tk.END)  # Clear existing text
        if not self.entries:
            self.display_text.insert(tk.END, "No entries found. Start logging your mood!")
            return
        for entry in self.entries:
            self.display_text.insert(tk.END, f"{entry['date']} - Mood: {entry['mood']}, Notes: {entry['notes']}\n")
            # Color coding based on mood
            self.display_text.tag_add(entry['mood'], "1.0", tk.END)
            self.display_text.tag_config(entry['mood'], foreground=MOOD_OPTIONS[entry['mood']])
        self.display_text.insert(tk.END, "-----------------------\n")

    def add_entry(self):
        # Limit to one entry per day
        today = datetime.now().strftime("%Y-%m-%d")
        if any(entry['date'] == today for entry in self.entries):
            messagebox.showwarning("Warning", "You have already logged your mood for today.")
            return
        
        mood = simpledialog.askstring("Mood Entry", "How are you feeling today? (Angry, Sad, Exhausted, Happy, Overwhelmed, Content)")
        notes = simpledialog.askstring("Mood Entry", "Any notes or thoughts?")
        if mood in MOOD_OPTIONS and notes:
            self.entries.append({
                "date": today,
                "mood": mood,
                "notes": notes
            })
            save_entries(self.entries)
            self.play_sound(NOTIFICATION_SOUND)  # Play the notification sound
            messagebox.showinfo("Success", "Mood entry added!")
        else:
            messagebox.showwarning("Warning", "Invalid mood or notes cannot be empty.")

    def play_sound(self, sound_file):
        # Play the notification sound
        if os.path.exists(sound_file):
            winsound.PlaySound(sound_file, winsound.SND_FILENAME)

    def show_calendar(self):
        # Open a new window with the calendar
        calendar_window = tk.Toplevel(self.root)
        calendar_window.title("Mood Calendar")
        cal = Calendar(calendar_window, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        cal.pack(pady=20)

        # Display mood for the selected date
        def show_mood():
            selected_date = cal.get_date()
            selected_date_str = datetime.strptime(selected_date, '%m/%d/%y').strftime("%Y-%m-%d")
            mood_entries = [entry for entry in self.entries if entry['date'] == selected_date_str]
            if mood_entries:
                mood_summary = f"Mood on {selected_date}:\n"
                mood_colors = ', '.join(entry['mood'] for entry in mood_entries)
                mood_summary += f"Moods logged: {mood_colors}\n"
                # Get the mood color of the last entry
                last_entry = mood_entries[-1]
                mood_color = MOOD_OPTIONS[last_entry['mood']]
                messagebox.showinfo("Mood Entry", mood_summary, icon='info')
                # Set the window color based on the mood
                calendar_window.configure(bg=mood_color)

                # Edit mood entry option
                if messagebox.askyesno("Edit Mood Entry", "Do you want to edit the notes for this date?"):
                    new_notes = simpledialog.askstring("Edit Notes", "Enter new notes:")
                    if new_notes:
                        last_entry['notes'] = new_notes  # Update the last entry's notes
                        save_entries(self.entries)
                        messagebox.showinfo("Success", "Mood entry updated!")
            else:
                messagebox.showinfo("Mood Entry", "No mood logged for this date.")

        show_button = tk.Button(calendar_window, text="Show Mood", command=show_mood)
        show_button.pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = MoodDiaryApp(root)
    root.mainloop()
