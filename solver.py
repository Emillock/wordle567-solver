import string
from typing import List, Dict
from itertools import product
lowercase_letters = list(string.ascii_lowercase)
print(lowercase_letters)
words_list_path = 'valid_words.txt'
with open(words_list_path, 'r') as file:
    words = [line.strip() for line in file.readlines()]

class Solver:
    def __init__(self, letters_number: int = 5):
        """
        Initializes the Solver instance.
        """
        self.letters_number = letters_number
        self.domains= [lowercase_letters.copy() for _ in range(letters_number)]
        self.must_contain_counts={}

    def update_csp_domains(self, allowed_letters: List[List[str]], guess: str, feedback: List[str]) -> Tuple[List[List[str]], Dict[str, int]]:
        """
        Updates the CSP domains (allowed_letters) based on the generate_wordle_feedback output.

        Args:
            allowed_letters: The current list of 5 domains (one for each position).
            guess: The word that was just guessed.
            feedback: The list of 'GREEN', 'YELLOW', 'GRAY' results.
        """

        #Dictionary to track the minimum required count of each letter
        #This must be calculated fresh for each guess, based on the current feedback
        must_contain_counts = {}

        #1) First Pass: Calculate all required GREEN and YELLOW counts
        for i in range(5):
            letter = guess[i]

            #We only care about letters that are definitely in the word
            if feedback[i] in ['GREEN', 'YELLOW']:
                #Sum up all GREEN/YELLOW instances of the letter in the guess
                total_yellow_or_green = sum(1 for k in range(5) if guess[k] == letter and feedback[k] in ['GREEN', 'YELLOW'])

                #The 'must_contain' count is the max of the current count and this total
                must_contain_counts[letter] = max(must_contain_counts.get(letter, 0), total_yellow_or_green)


        #2) Second Pass: Apply Positional and Omission Constraints
        for i in range(5):
            letter = guess[i]

            if feedback[i] == 'GREEN':
                #Positional Constraint: Fixed to this letter
                allowed_letters[i] = [letter]

            elif feedback[i] == 'YELLOW':
                #Positional Exclusion: Remove the letter from the current position's domain
                if letter in allowed_letters[i]:
                    allowed_letters[i].remove(letter)

            elif feedback[i] == 'GRAY':
                #Omission Rule: A letter is GRAY and must be omitted if, and only if, its required count is zero

                #This check uses .get(letter, 0) to safely check if the letter is in the dictionary.
                is_required_elsewhere = must_contain_counts.get(letter, 0) > 0

                if not is_required_elsewhere:
                    #If not required, remove this letter from all 5 domains
                    for j in range(5):
                        if letter in allowed_letters[j]:
                            allowed_letters[j].remove(letter)

        self.allowed_letters=allowed_letters
        self.must_contain_counts=must_contain_counts

    def solve_wordle(allowed_letters: List[List[str]], letters_number: int = 5):
        """Solve Wordle by generating all possible combinations of allowed letters.
        Args:
            allowed_letters (List[List[str]]): A list of lists, where each inner list contains
                                                the allowed letters for that position.
            letters_number (int): The number of letters in the Wordle word. Default is 5."""

        return list(filter(
            lambda w: len(w.strip()) == letters_number and
            (lambda word: all(c in allowed_letters[i]
            for i, c in enumerate(word.strip())))(w),
            words)
        )
