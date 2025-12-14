import random
from typing import List, Dict

#Game Setup
def start_new_game(word_list: List[str]) -> str:
    #This function randomly selects a word from the provided list to be the target word
    if not word_list:
        raise ValueError("Word list cannot be empty.")

    return random.choice(word_list) #Uses lowercase for consistency

#Feedback function
def generate_wordle_feedback(target_word: str, guess: str) -> List[str]:
    #Check if the chosen word and the guess matches the requirement
    target_word = target_word.lower()
    guess = guess.lower()

    if len(target_word) != 5 or len(guess) != 5:
        raise ValueError("Both target_word and guess must be 5 letters long.")

    feedback = [''] * 5
    #Use a mutable list for target letters to handle duplicates properly
    target_letters = list(target_word)

    #1) Find all GREEN matches first
    for i in range(5):
        if guess[i] == target_word[i]:
            feedback[i] = 'GREEN'
            #Mark this letter as "used" in the target list
            target_letters[i] = None

    #2) Find YELLOW and GRAY matches
    for i in range(5):
        #Skip letters that were already marked GREEN
        if feedback[i] == 'GREEN':
            continue

        letter = guess[i]

        if letter in target_letters:
            feedback[i] = 'YELLOW'
            #Mark the first occasion of this letter as "used" to prevent double-counting
            try:
                target_letters[target_letters.index(letter)] = None
            except ValueError:
                #Should not happen if 'letter in target_letters' is true
                pass
        else:
            feedback[i] = 'GRAY'

    return feedback