import random
from typing import List, Dict

#Game Setup

#Word List
def load_valid_words(path: str = 'valid_words.txt') -> List[str]:
    #Loads 5-letter words from the specified file path

    #In case of error, will use sample words
    sample_words = ["crane", "train", "power", "sheep", "light"]
    words = []

    try:
        with open(path, 'r') as file:
            #Store all words in lowercase and strip whitespace
            words = [line.strip().lower() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Error: {path} not found. Using a sample list for simulation.")
        words = sample_words

    #Filter the list to make sure only 5-letter words are used
    five_letter_words = [w for w in words if len(w) == 5]

    if not five_letter_words:
        print("Warning: No 5-letter words found. Using sample list.")
        return sample_words

    return five_letter_words

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