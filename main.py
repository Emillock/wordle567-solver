from typing import List, Optional

from solver import CSPSolver
from wordle_game import start_new_game, generate_wordle_feedback
from utils import load_valid_words

# here you can test the integration of the CSP solver with the Wordle game simulation
def main():
    MAX_GUESSES = 6
    LETTERS_NUMBER = 5

    # Load n-letter answer list
    words = load_valid_words(letters_number=LETTERS_NUMBER)
    if not words:
        print("No words available to run simulation. Ensure answers_5letter.txt exists.")
        return

    # Instantiate the CSP-based solver
    solver = CSPSolver(letters_number=LETTERS_NUMBER)

    # Start the game with a random target from the same word list
    target_word = start_new_game(words)
    print("--- Wordle Solver Simulation ---")
    print("(Target word selected — hidden from the solver)\n")

    for guess_num in range(1, MAX_GUESSES + 1):
        current_guess: Optional[str] = solver.solve_csp()
        if not current_guess:
            print("\nSolver could not find any valid candidate words. Check constraints or word list.")
            print(f"The target word was: {target_word.upper()}")
            return
        print(f"--- Guess {guess_num}: {current_guess.upper()} ---")
        # Ask solver for next guess
        # Get feedback from the game
        feedback = generate_wordle_feedback(target_word, current_guess)
        print(f"Feedback: {feedback}")

        # Check for win
        if all(f == 'GREEN' for f in feedback):
            print(f"\nCorrect! The solver guessed '{current_guess.upper()}' in {guess_num} guesses.")
            return

        # Feed back into the CSP solver so it updates domains and counts
        try:
            solver.incorporate_feedback(current_guess, feedback)
        except Exception as e:
            print(f"Error while incorporating feedback: {e}")
            return



        # Show some diagnostics
        candidates_count = len([w for w in solver.words if solver._word_matches_domains_and_counts(w)])
        print(f"Candidates remaining (approx): {candidates_count}")

    print("\nGame Over: Maximum guesses reached.")
    print(f"The target word was: {target_word.upper()}")


if __name__ == "__main__":
    main()