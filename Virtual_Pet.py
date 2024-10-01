import tkinter as tk
from tkinter import ttk, messagebox
import random

class VirtualPet:
    def __init__(self, name, pet_type):
        self.name = name
        self.pet_type = pet_type
        self.happiness = 5
        self.hunger = 5

    def feed(self):
        if self.hunger < 10:
            self.hunger += 1
            return f"{self.name} is fed! Hunger level: {self.hunger}"
        else:
            return f"{self.name} is not hungry!"

    def play(self):
        if self.happiness < 10:
            self.happiness += 1
            return f"You played with {self.name}! Happiness level: {self.happiness}"
        else:
            return f"{self.name} is already very happy!"

    def get_status(self):
        return (f"Happiness: {self.happiness}/10\n"
                f"Hunger: {self.hunger}/10")


class PetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Pet Simulator")
        self.root.geometry("500x500")
        self.root.config(bg="#f0f8ff")

        self.selected_pet_type = tk.StringVar()
        self.pet = None

        self.canvas = tk.Canvas(self.root, width=500, height=400, bg="white")
        self.canvas.pack()

        self.setup_widgets()
        self.pet_id = None  # Store the ID of the drawn pet
        self.pet_position = [250, 200]  # Initial position of the pet

    def setup_widgets(self):
        ttk.Label(self.root, text="Choose your pet:", font=("Helvetica", 16), background="#f0f8ff").pack(pady=10)
        
        pets = ["Rabbit", "Cat", "Dog", "Goat", "Bird"]
        for pet in pets:
            ttk.Radiobutton(self.root, text=pet, variable=self.selected_pet_type, value=pet, command=self.start_pet).pack(anchor='w', padx=20)

        # Entry for pet name with placeholder
        self.name_entry = ttk.Entry(self.root, font=("Helvetica", 14))
        self.name_entry.insert(0, "Enter your pet's name")
        self.name_entry.bind("<FocusIn>", self.clear_placeholder)
        self.name_entry.bind("<FocusOut>", self.set_placeholder)
        self.name_entry.pack(pady=10)

        # Status label
        self.status_label = ttk.Label(self.root, text="", font=("Helvetica", 14), background="#f0f8ff")
        self.status_label.pack(pady=20)

        # Action buttons
        self.feed_button = ttk.Button(self.root, text="Feed", command=self.feed_pet, state=tk.DISABLED)
        self.feed_button.pack(pady=5)

        self.play_button = ttk.Button(self.root, text="Play", command=self.play_pet, state=tk.DISABLED)
        self.play_button.pack(pady=5)

        self.exit_button = ttk.Button(self.root, text="Exit", command=self.exit_app, state=tk.DISABLED)
        self.exit_button.pack(pady=5)

    def clear_placeholder(self, event):
        if self.name_entry.get() == "Enter your pet's name":
            self.name_entry.delete(0, tk.END)  # Clear the placeholder text
            self.name_entry.config(foreground="black")  # Change text color to black for user input

    def set_placeholder(self, event):
        if not self.name_entry.get():  # If the entry is empty
            self.name_entry.insert(0, "Enter your pet's name")  # Insert placeholder text
            self.name_entry.config(foreground="gray")  # Change text color to gray for placeholder


    def start_pet(self):
        pet_name = self.name_entry.get()
        pet_type = self.selected_pet_type.get()
        if not pet_name or pet_type not in ["Rabbit", "Cat", "Dog", "Goat", "Bird"]:
            messagebox.showwarning("Warning", "Please enter a pet name and select a pet type.")
            return
        self.pet = VirtualPet(pet_name, pet_type)
        self.name_entry.config(state=tk.DISABLED)
        self.feed_button.config(state=tk.NORMAL)
        self.play_button.config(state=tk.NORMAL)
        self.exit_button.config(state=tk.NORMAL)
        self.update_status()
        self.animate_pet()

    def update_status(self):
        if self.pet:
            self.status_label.config(text=self.pet.get_status())

    def draw_pet(self):
        if self.pet_id:
            self.canvas.delete(self.pet_id)

        # Choose a shape for each pet type
        if self.pet.pet_type == "Rabbit":
            shape = self.canvas.create_oval(self.pet_position[0], self.pet_position[1],
                                             self.pet_position[0] + 30, self.pet_position[1] + 20, fill="pink", outline="black")
        elif self.pet.pet_type == "Cat":
            shape = self.canvas.create_polygon(self.pet_position[0], self.pet_position[1],
                                                self.pet_position[0] + 15, self.pet_position[1] - 15,
                                                self.pet_position[0] + 30, self.pet_position[1],
                                                fill="gray", outline="black")
        elif self.pet.pet_type == "Dog":
            shape = self.canvas.create_rectangle(self.pet_position[0], self.pet_position[1],
                                                  self.pet_position[0] + 30, self.pet_position[1] + 20,
                                                  fill="brown", outline="black")
        elif self.pet.pet_type == "Goat":
            shape = self.canvas.create_rectangle(self.pet_position[0], self.pet_position[1],
                                                  self.pet_position[0] + 20, self.pet_position[1] + 20,
                                                  fill="white", outline="black")
        elif self.pet.pet_type == "Bird":
            shape = self.canvas.create_oval(self.pet_position[0], self.pet_position[1],
                                             self.pet_position[0] + 20, self.pet_position[1] + 20, fill="yellow", outline="black")

        self.pet_id = shape

    def animate_pet(self):
        self.draw_pet()  # Draw the pet
        self.move_pet()  # Start moving the pet

    def move_pet(self):
        if self.pet_id:
            # Randomly change position
            dx = random.choice([-5, 5])  # Random move left or right
            dy = random.choice([-5, 5])  # Random move up or down

            # Get the current position of the pet
            coords = self.canvas.coords(self.pet_id)
            x1, y1, x2, y2 = coords
            
            # Calculate new position
            new_x1 = x1 + dx
            new_y1 = y1 + dy
            new_x2 = x2 + dx
            new_y2 = y2 + dy

            # Check bounds
            if new_x1 < 0 or new_x2 > 500 or new_y1 < 0 or new_y2 > 400:
                return  # Don't move if it goes out of bounds

            # Move the pet
            self.canvas.move(self.pet_id, dx, dy)

        self.root.after(100, self.move_pet)  # Move the pet every 100 ms

    def feed_pet(self):
        if self.pet:
            message = self.pet.feed()
            messagebox.showinfo("Feed Pet", message)
            self.update_status()

    def play_pet(self):
        if self.pet:
            message = self.pet.play()
            messagebox.showinfo("Play with Pet", message)
            self.update_status()

    def exit_app(self):
        messagebox.showinfo("Goodbye", f"Goodbye! {self.pet.name} will miss you!")
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = PetApp(root)
    root.mainloop()
