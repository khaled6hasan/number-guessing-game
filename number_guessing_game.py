import tkinter as tk
from tkinter import messagebox
import random
import csv
import os
import pygame

pygame.mixer.init()

number_to_guess = 0
attempts = 0
timer_running = False
time_left = 60
dark_mode = False
muted = False
current_user = ""
difficulty_var = None

def play_sound(sound_file):
    if not muted:
        try:
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play()
        except:
            pass

def start_game():
    global number_to_guess, attempts, timer_running, time_left
    attempts = 0
    timer_running = True
    time_left = 60
    difficulty = difficulty_var.get()
    if difficulty == "Easy":
        number_to_guess = random.randint(1, 50)
    elif difficulty == "Hard":
        number_to_guess = random.randint(1, 200)
    else:
        number_to_guess = random.randint(1, 100)
    update_status("Game started! Guess a number.")
    update_timer()

def update_timer():
    global time_left, timer_running
    if timer_running and time_left > 0:
        time_left -= 1
        timer_label.config(text=f"Time Left: {time_left}s")
        root.after(1000, update_timer)
    elif time_left == 0:
        timer_running = False
        update_status(f"Time's up! The number was {number_to_guess}.")
        play_sound("fail.wav")

def check_guess():
    global attempts, timer_running
    if not timer_running:
        return
    try:
        guess = int(guess_entry.get())
        attempts += 1
        if guess < number_to_guess:
            update_status("Try higher!")
        elif guess > number_to_guess:
            update_status("Try lower!")
        else:
            timer_running = False
            update_status(f"Correct! You guessed it in {attempts} tries.")
            save_score(current_user, attempts)
            play_sound("success.wav")
    except ValueError:
        update_status("Enter a valid number!")

def save_score(name, score):
    if name:
        with open("leaderboard.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([name, score])

def load_leaderboard():
    if not os.path.exists("leaderboard.csv"):
        return []
    with open("leaderboard.csv", "r") as file:
        reader = csv.reader(file)
        return sorted(reader, key=lambda x: int(x[1]))

def show_leaderboard():
    scores = load_leaderboard()
    top_scores = "\n".join([f"{i+1}. {name} - {score} tries" for i, (name, score) in enumerate(scores[:10])])
    messagebox.showinfo("Leaderboard", top_scores if top_scores else "No scores yet!")

def save_game():
    if current_user:
        with open(f"{current_user}_save.txt", "w") as file:
            file.write(f"{number_to_guess},{attempts},{time_left}")

def load_game():
    global number_to_guess, attempts, time_left, timer_running
    try:
        with open(f"{current_user}_save.txt", "r") as file:
            data = file.read().split(",")
            number_to_guess = int(data[0])
            attempts = int(data[1])
            time_left = int(data[2])
            timer_running = True
            update_status("Game loaded. Continue guessing!")
            update_timer()
    except:
        update_status("No saved game found.")

def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    bg = "#333" if dark_mode else "#fff"
    fg = "#fff" if dark_mode else "#000"
    root.config(bg=bg)
    for widget in root.winfo_children():
        if isinstance(widget, (tk.Button, tk.Label, tk.Entry, tk.OptionMenu)):
            widget.config(bg=bg, fg=fg, highlightbackground=bg)

def change_theme():
    import random
    color = random.choice(["#ffcccc", "#ccffcc", "#ccccff", "#ffffcc", "#ccffff", "#ffccff"])
    root.config(bg=color)
    for widget in root.winfo_children():
        if isinstance(widget, (tk.Button, tk.Label, tk.Entry, tk.OptionMenu)):
            widget.config(bg=color)

def toggle_mute():
    global muted
    muted = not muted

def show_hint():
    if number_to_guess:
        hint = "even" if number_to_guess % 2 == 0 else "odd"
        update_status(f"Hint: It's an {hint} number.")

def update_status(msg):
    status_label.config(text=msg)

def ask_username():
    global current_user
    current_user = username_entry.get()
    if not current_user:
        messagebox.showwarning("Login", "Please enter a name.")
        return
    update_status(f"Welcome, {current_user}!")

# UI Setup
root = tk.Tk()
root.title("🎯 Number Guessing Game")
root.geometry("360x420")
root.resizable(False, False)

# Top
tk.Label(root, text="Name:").pack(pady=(8, 0))
username_entry = tk.Entry(root)
username_entry.pack()
tk.Button(root, text="Login", command=ask_username).pack(pady=2)

# Guess
guess_entry = tk.Entry(root)
guess_entry.pack()
tk.Button(root, text="Guess", command=check_guess).pack(pady=2)

# Difficulty
difficulty_var = tk.StringVar(value="Medium")
tk.Label(root, text="Difficulty:").pack()
tk.OptionMenu(root, difficulty_var, "Easy", "Medium", "Hard").pack()

# Game buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Start Game", command=start_game, width=10).grid(row=0, column=0, padx=5, pady=2)
tk.Button(btn_frame, text="Save", command=save_game, width=10).grid(row=0, column=1, padx=5, pady=2)
tk.Button(btn_frame, text="Load", command=load_game, width=10).grid(row=0, column=2, padx=5, pady=2)

tk.Button(btn_frame, text="Hint", command=show_hint, width=10).grid(row=1, column=0, padx=5, pady=2)
tk.Button(btn_frame, text="Dark Mode", command=toggle_dark_mode, width=10).grid(row=1, column=1, padx=5, pady=2)
tk.Button(btn_frame, text="Theme", command=change_theme, width=10).grid(row=1, column=2, padx=5, pady=2)

tk.Button(btn_frame, text="Mute", command=toggle_mute, width=10).grid(row=2, column=0, padx=5, pady=2)
tk.Button(btn_frame, text="Leaderboard", command=show_leaderboard, width=22).grid(row=2, column=1, columnspan=2, pady=2)

status_label = tk.Label(root, text="Welcome to the Number Guessing Game!", fg="blue")
status_label.pack(pady=10)

timer_label = tk.Label(root, text="Time Left: 30s", font=("Arial", 12))
timer_label.pack()

root.mainloop()
