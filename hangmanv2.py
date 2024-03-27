import tkinter as tk
from tkinter import messagebox
import random

# Words for the game
word_list = ["aardvark", "baboon", "camel", "jazz", "grass", "follow", "castle", "cloud"]

# Global variables
chosen_word = ""
blank_list = []
update_display = 0
hint_used = False
difficulty = "medium"  # Default difficulty

def new_game():
    global chosen_word, blank_list, update_display, hint_used
    chosen_word = list(random.choice(word_list))
    blank_list = ["_"] * len(chosen_word)
    update_display = 0
    hint_used = False
    update_display_text()
    hint_button["state"] = tk.NORMAL
    hint_label.config(text="")
    difficulty_label.config(text=f"Difficulty: {difficulty.capitalize()}")

def update_display_text():
    hangman_display.config(text=HANGMANPICS[update_display])
    word_display.config(text=' '.join(blank_list))

def make_a_guess(letter):
    global update_display
    guess = letter.lower()
    correct_guess = False
    for i, char in enumerate(chosen_word):
        if guess == char:
            blank_list[i] = guess
            correct_guess = True
    if not correct_guess:
        update_display += 1
    update_display_text()
    if not "_" in blank_list:
        messagebox.showinfo("Congratulations!", "You guessed the word! You win!")
        new_game()
    elif update_display == 6:
        messagebox.showinfo("Game Over", f"The word was '{''.join(chosen_word)}'. Better luck next time.")
        new_game()

def use_hint():
    global hint_used
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

def set_difficulty(diff):
    global difficulty
    difficulty = diff
    new_game()

def create_keyboard():
    letters = "abcdefghijklmnopqrstuvwxyz"
    for i, letter in enumerate(letters):
        btn = tk.Button(virtual_keyboard, text=letter.upper(), width=3, height=2,
                        command=lambda l=letter: make_a_guess(l))
        btn.grid(row=i // 7, column=i % 7)

# Hangman ASCII art
HANGMANPICS = ['''
  +---+
  |   |
      |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']

# Main GUI setup
root = tk.Tk()
root.title("Hangman Game")

hangman_display = tk.Label(root, text="", font=("Courier", 12))
hangman_display.pack()

word_display = tk.Label(root, text="", font=("Courier", 16))
word_display.pack()

difficulty_label = tk.Label(root, text="", font=("Courier", 12))
difficulty_label.pack()

hint_label = tk.Label(root, text="", font=("Courier", 12))
hint_label.pack()

hint_button = tk.Button(root, text="Hint", command=use_hint)
hint_button.pack()

virtual_keyboard = tk.Frame(root)
virtual_keyboard.pack()

difficulty_frame = tk.Frame(root)
difficulty_frame.pack()

for diff in ["easy", "medium", "hard"]:
    btn = tk.Button(difficulty_frame, text=diff.capitalize(), command=lambda d=diff: set_difficulty(d))
    btn.pack(side=tk.LEFT)

new_game()
create_keyboard()
root.mainloop()
