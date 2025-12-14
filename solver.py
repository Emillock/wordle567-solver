import string
from typing import List, Dict, Tuple
from itertools import product
from utils import max_letter_counts
import csv

lowercase_letters = list(string.ascii_lowercase)
print(lowercase_letters)

file_path = 'nounlist.csv'
data_as_list = []

with open(file_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        data_as_list.append(row)

words = [item for sublist in data_as_list for item in sublist]

print(max_letter_counts(words, 5))

class Solver:
    def __init__(self, letters_number: int = 5):
        """
        Initializes the Solver instance.
        """
        self.letters_number = letters_number
        self.domains= [lowercase_letters.copy() for _ in range(letters_number)]
        self.guesses=[]
        # self.must_contain_counts={}
        self.max_letter_counts = max_letter_counts(words, letters_number)

    def update_csp_domains(self, feedback: List[str]) -> Tuple[List[List[str]], Dict[str, int]]:
        """
        Updates the CSP domains (allowed_letters) based on the generate_wordle_feedback output.

        Args:
            allowed_letters: The current list of 5 domains (one for each position).
            guess: The word that was just guessed.
            feedback: The list of 'GREEN', 'YELLOW', 'GRAY' results.
        """

        #Dictionary to track the minimum required count of each letter
        #This must be calculated fresh for each guess, based on the current feedback
        guess=self.guesses[-1]
        #1) First Pass: Calculate all required GREEN and YELLOW counts
        for i in range(self.letters_number):
            letter = guess[i]

            # #We only care about letters that are definitely in the word
            # if feedback[i] in ['GREEN', 'YELLOW']:
            #     #Sum up all GREEN/YELLOW instances of the letter in the guess
            #     yellow_sum=sum(1 for k in range(self.letters_number) if guess[k] == letter and feedback[k] == 'YELLOW')
            #     green_sum=sum(1 for k in range(self.letters_number) if guess[k] == letter and feedback[k] == 'GREEN')
            #     total_yellow_or_green = green_sum + (yellow_sum if not green_sum==0 else 1)

            #     #The 'must_contain' count is the max of the current count and this total
            #     self.must_contain_counts[letter] = max(self.must_contain_counts.get(letter, 0), total_yellow_or_green)


        #2) Second Pass: Apply Positional and Omission Constraints
        for i in range(self.letters_number):
            letter = guess[i]

            if feedback[i] == 'GREEN':
                #Positional Constraint: Fixed to this letter
                self.domains[i] = [letter]
                self.max_letter_counts[letter] = self.max_letter_counts[letter] - 1
            
                if self.max_letter_counts[letter] == 0:
                    #If not required, remove this letter from all domains
                    for j in range(self.letters_number):
                        if letter in self.domains[j] and j != i:
                            self.domains[j].remove(letter)

            elif feedback[i] == 'YELLOW':
                #Positional Exclusion: Remove the letter from the current position's domain
                if letter in self.domains[i]:
                    self.domains[i].remove(letter)

            elif feedback[i] == 'GRAY':
                for j in range(self.letters_number):
                    if letter in self.domains[j]:
                        self.domains[j].remove(letter)

    def guess(self):
        list_of_possibilities = list(filter(
            lambda w: len(w.strip()) == self.letters_number and
            (lambda word: all(c in self.domains[i]
            for i, c in enumerate(word.strip())))(w),
            words)
        )

        self.guesses.append(list_of_possibilities[0])
        return list_of_possibilities[0]
