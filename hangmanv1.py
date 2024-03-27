import tkinter as tk
from tkinter import messagebox
import random

# Words for the game
word_list = ["aardvark", "baboon", "camel", "jazz", "grass", "follow", "castle", "cloud"]

# Global variables
chosen_word = ""
blank_list = []
update_display = 0
difficulty = ""
hint_used = False

def new_game():
    global chosen_word, blank_list, update_display, hint_used
    chosen_word = list(random.choice(word_list))
    blank_list = ["_"] * len(chosen_word)
    update_display = 0
    hint_used = False
    update_display_text()
    hint_button["state"] = tk.NORMAL
    hint_label.config(text="")

def update_display_text():
    hangman_display.config(text=HANGMANPICS[update_display])
    word_display.config(text=' '.join(blank_list))

def make_a_guess():
    global update_display
    guess = guess_entry.get().lower()
    if len(guess) != 1 or not guess.isalpha():
        messagebox.showwarning("Invalid Guess", "Please enter a single letter.")
        return
    correct_guess = False
    for i, letter in enumerate(chosen_word):
        if guess == letter:
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
    hidden_letters = [(i, letter) for i, letter in enumerate(blank_list) if letter == "_"]
    if hidden_letters:
        index, letter = random.choice(hidden_letters)
        blank_list[index] = chosen_word[index]
        hint_label.config(text=f"Hint: '{letter.upper()}' is in the word.")
        update_display_text()
    else:
        hint_label.config(text="No hidden letters to reveal.")

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

guess_entry = tk.Entry(root, width=5, font=("Courier", 12))
guess_entry.pack()

guess_button = tk.Button(root, text="Guess", command=make_a_guess)
guess_button.pack()

hint_button = tk.Button(root, text="Hint", command=use_hint)
hint_button.pack()

hint_label = tk.Label(root, text="", font=("Courier", 12))
hint_label.pack()

new_game_button = tk.Button(root, text="New Game", command=new_game)
new_game_button.pack()

exit_button = tk.Button(root, text="Exit", command=root.destroy)
exit_button.pack()

new_game()
root.mainloop()
