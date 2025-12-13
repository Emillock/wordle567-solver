from solver import solve_wordle, lowercase_letters
from wordle_game import start_new_game, generate_wordle_feedback, load_valid_words
from typing import List, Dict, Tuple

# --- Core Constraint Update Logic ---

def update_csp_domains(allowed_letters: List[List[str]], guess: str, feedback: List[str]) -> Tuple[List[List[str]], Dict[str, int]]:
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

    return allowed_letters, must_contain_counts

#Main Simulation

def main():
    MAX_GUESSES = 6

    #1) Load the words using the function from wordle_game.py
    words = load_valid_words() #This is the list from valid_words.txt

    #Initialize the CSP domains to the full alphabet for all 5 positions
    allowed_letters = [list(lowercase_letters) for _ in range(5)]

    #Start the game
    target_word = start_new_game(words) #Use the large word list
    print(f"--- Wordle Solver Simulation ---")
    print(f"Target Word Selected: (Keep this hidden from the agent!)")

    #Initial guess
    current_guess = "sanes"
    print(f"Agent's Initial Guess: {current_guess.upper()}")

    for guess_num in range(1, MAX_GUESSES + 1):
        print(f"\n--- Guess {guess_num}: {current_guess.upper()} ---")

        # 1) Get Feedback from the Game
        feedback = generate_wordle_feedback(target_word, current_guess)
        print(f"Feedback: {feedback}")

        # 2) Check for Win Condition
        if all(f == 'GREEN' for f in feedback):
            print(f"\n Correct! The solver guessed '{current_guess.upper()}' in {guess_num} guesses.")
            return

        # 3) Update the CSP Domains based on Feedback
        #This function applies GREEN/YELLOW/GRAY rules to allowed_letters and finds required counts
        allowed_letters, must_contain_counts = update_csp_domains(allowed_letters, current_guess, feedback)

        #Print the current state of the domains (for debugging/visualisation)
        print("\nCSP Domains (Reduced Allowed Letters):")
        for i, domain in enumerate(allowed_letters):
            #Show the first few letters or the exact letter if domain is size 1
            display = domain if len(domain) <= 5 else f"{domain[:5]}... ({len(domain)} left)"
            print(f"Pos {i}: {display}")

        # 4) Run the Solver (Generate new possibilities)
        possible_words = solve_wordle(allowed_letters, words, must_contain_counts, 5)

        if not possible_words:
            print("\n Solver ran out of possible words. Check constraints/word list.")
            print(f"The target word was: {target_word.upper()}")
            return

        print(f"\n{len(possible_words)} possible words remaining. Top 5:")
        print(possible_words[:5])

        #5) Select Next Guess (this is where we use heuristics)
        #For now, we'll just pick the first word (simple but poor heuristic)
        current_guess = possible_words[0]

    print("\nGame Over: Maximum guesses reached.")
    print(f"The target word was: {target_word.upper()}")


if __name__ == "__main__":
    main()