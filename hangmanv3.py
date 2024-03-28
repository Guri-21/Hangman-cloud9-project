import tkinter as tk
from tkinter import messagebox
import random
import time

# Word themes for different Theme levels
word_themes = {
    "fruits": ["apple", "banana", "orange", "grape", "kiwi", "pear", "melon", "peach"],
    "animals": ["elephant", "giraffe", "zebra", "lion", "tiger", "monkey", "hippopotamus", "kangaroo"],
    "countries": ["australia", "brazil", "canada", "germany", "japan", "mexico", "russia", "india"]
}

# Global variables
chosen_word = ""
blank_list = []
update_display = 0
hint_used = False
Theme = "animals"  # Default Theme
points = 0
start_time = None
total_games = 0
total_points = 0
total_time = 0

# Hangman images
HANGMANPICS = [
'''
  +---+
  |   |
      |
      |
      |
      |
=========''',
'''
  +---+
  |   |
  O   |
      |
      |
      |
=========''',
'''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''',
'''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''',
'''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''',
'''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''',
'''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
========='''
]

def new_game():
    global chosen_word, blank_list, update_display, hint_used, points, start_time
    chosen_word = list(random.choice(word_themes[Theme]))
    blank_list = ["_"] * len(chosen_word)
    update_display = 0
    hint_used = False
    points = 0
    start_time = time.time()
    update_display_text()
    hint_button["state"] = tk.NORMAL
    hint_label.config(text="")
    Theme_label.config(text=f"Theme: {Theme.capitalize()}")

def update_display_text():
    hangman_display.config(text=HANGMANPICS[update_display])
    word_display.config(text=' '.join(blank_list))
    points_label.config(text=f"Points: {points}")

def make_a_guess(letter):
    global update_display, points
    guess = letter.lower()
    correct_guess = False
    for i, char in enumerate(chosen_word):
        if guess == char:
            blank_list[i] = guess
            correct_guess = True
    if not correct_guess:
        update_display += 1
    else:
        points += 10
    update_display_text()
    if not "_" in blank_list:
        win_animation()
        return
    if update_display == 6:
        lose_animation()
        return

def use_hint():
    global hint_used, points
    if hint_used:
        messagebox.showinfo("Hint", "You've already used the hint for this game.")
        return
    hint_used = True
    hidden_letters = [(i, char) for i, char in enumerate(blank_list) if char == "_"]
    if hidden_letters:
        index, char = random.choice(hidden_letters)
        blank_list[index] = chosen_word[index]
        hint_label.config(text=f"Hint: '{char.upper()}' is in the word.")
        update_display_text()
    else:
        hint_label.config(text="No hidden letters to reveal.")
    points -= 5  # Penalty for using hint
    update_display_text()

def set_Theme(diff):
    global Theme
    Theme = diff
    new_game()

def create_keyboard():
    letters = "abcdefghijklmnopqrstuvwxyz"
    for i, letter in enumerate(letters):
        btn = tk.Button(virtual_keyboard, text=letter.upper(), width=3, height=2,
                        command=lambda l=letter: make_a_guess(l))
        btn.grid(row=i // 7, column=i % 7)

def win_animation():
    global points, total_games, total_points, total_time
    elapsed_time = int(time.time() - start_time)
    points += max(100 - elapsed_time, 0)
    total_points += points
    total_time += elapsed_time
    total_games += 1
    messagebox.showinfo("Congratulations!", f"You guessed the word! You win!\nTime taken: {elapsed_time} seconds\nPoints earned: {points}")
    canvas.create_text(200, 50, text="You Win!", font=("Helvetica", 48), fill="green")
    canvas.update()
    canvas.after(2000, canvas.delete("all"))
    new_game()

def lose_animation():
    global total_games
    total_games += 1
    messagebox.showinfo("Game Over", f"The word was '{''.join(chosen_word)}'. Better luck next time.")
    canvas.create_text(200, 50, text="Game Over", font=("Helvetica", 48), fill="red")
    canvas.update()
    canvas.after(2000, canvas.delete("all"))
    new_game()

def show_stats():
    if total_games == 0:
        avg_points = 0
        avg_time = 0
    else:
        avg_points = total_points / total_games
        avg_time = total_time / total_games
    messagebox.showinfo("Player Statistics", f"Total Games: {total_games}\nTotal Points: {total_points}\nAverage Points per Game: {avg_points}\nAverage Time per Game: {avg_time:.2f} seconds")

# Main GUI setup
root = tk.Tk()
root.title("Hangman Game")

hangman_display = tk.Label(root, text="", font=("Courier", 12))
hangman_display.pack()

word_display = tk.Label(root, text="", font=("Courier", 16))
word_display.pack()

Theme_label = tk.Label(root, text="", font=("Courier", 12))
Theme_label.pack()

hint_label = tk.Label(root, text="", font=("Courier", 12))
hint_label.pack()

points_label = tk.Label(root, text="", font=("Courier", 12))
points_label.pack()

hint_button = tk.Button(root, text="Hint", command=use_hint)
hint_button.pack()

virtual_keyboard = tk.Frame(root)
virtual_keyboard.pack()

Theme_frame = tk.Frame(root)
Theme_frame.pack()

for diff in ["fruits", "animals", "countries"]:
    btn = tk.Button(Theme_frame, text=diff.capitalize(), command=lambda d=diff: set_Theme(d))
    btn.pack(side=tk.LEFT)

canvas = tk.Canvas(root, width=400, height=100)
canvas.pack()

stats_button = tk.Button(root, text="Player Stats", command=show_stats)
stats_button.pack()

new_game()
create_keyboard()
root.mainloop()
