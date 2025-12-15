import argparse
import csv
import sys
from collections import defaultdict
from statistics import mean

from wordle_game import generate_wordle_feedback
from solver import CSPSolver, DummySolver
from utils import load_valid_words


def load_answers(path: str) -> list:
    with open(path, 'r', encoding='utf-8') as f:
        return [w.strip() for w in f if w.strip()]


def simulate(answers: list, solver_name: str = 'csp', max_guesses: int = 6, limit: int = None):
    total = 0
    wins = 0
    guess_counts = []
    distribution = defaultdict(int)
    failed_words = []

    # pre-load valid words for DummySolver if needed
    if solver_name == 'dummy':
        words = load_valid_words(letters_number=5)

    for idx, target in enumerate(answers):
        if limit and idx >= limit:
            break
        total += 1

        # instantiate solver fresh for each target
        if solver_name == 'csp':
            solver = CSPSolver(letters_number=len(target))
            guess_func = None
        else:
            solver = DummySolver(words, letters_number=len(target))

        attempts = 0
        solved = False

        while attempts < max_guesses:
            attempts += 1
            if solver_name == 'csp':
                guess = solver.solve_csp()
                if guess is None:
                    # no candidate -> fail early
                    break
            else:
                guess = solver.guess()
                if guess is None:
                    break

            feedback = generate_wordle_feedback(target, guess)

            if solver_name == 'csp':
                # solver will record guess when incorporate_feedback is called
                solver.incorporate_feedback(guess, feedback)
            else:
                solver.update_csp_domains(feedback)

            if all(f == 'GREEN' for f in feedback):
                solved = True
                break

        if solved:
            wins += 1
            guess_counts.append(attempts)
            distribution[attempts] += 1
        else:
            failed_words.append(target)
            distribution['fail'] += 1

        # simple progress every 100 games
        if total % 100 == 0:
            print(f"Simulated {total} games... wins so far: {wins}")

    winrate = (wins / total) * 100 if total else 0
    avg_guesses = mean(guess_counts) if guess_counts else float('nan')

    results = {
        'total': total,
        'wins': wins,
        'winrate_percent': winrate,
        'average_guesses_on_wins': avg_guesses,
        'distribution': dict(distribution),
        'failed_words': failed_words,
    }

    return results


def pretty_print(results):
    print('\nSimulation results:')
    print(f"Total games: {results['total']}")
    print(f"Wins: {results['wins']} ({results['winrate_percent']:.2f}%)")
    if results['wins'] > 0:
        print(f"Average guesses (wins only): {results['average_guesses_on_wins']:.2f}")
    print('\nDistribution:')
    for k in sorted(results['distribution'].keys(), key=lambda x: (x=='fail', x)):
        print(f"  {k}: {results['distribution'][k]}")
    print(f"\nFailed words ({len(results['failed_words'])}): {results['failed_words'][:20]}{'...' if len(results['failed_words'])>20 else ''}")


def main():
    parser = argparse.ArgumentParser(description='Simulate Wordle across all answers and compute metrics')
    parser.add_argument('--letters_number', type=int, default=7)
    parser.add_argument('--solver', type=str, choices=['csp', 'dummy'], default='csp')
    parser.add_argument('--max-guesses', type=int, default=7)
    parser.add_argument('--limit', type=int, help='Limit number of answers to simulate (for quick tests)')
    parser.add_argument('--save-csv', type=str, help='Optional path to save per-word results CSV')

    args = parser.parse_args()
    letters_number = args.letters_number
    answers = load_answers(f'word_lists/wordle_answers_{letters_number}letter.txt')
    if not answers:
        print('No letters_number loaded.')
        sys.exit(1)

    results = simulate(answers, solver_name=args.solver, max_guesses=args.max_guesses, limit=args.limit)
    pretty_print(results)

    if args.save_csv:
        # Write basic summary for failed words
        with open(args.save_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['metric', 'value'])
            writer.writerow(['total', results['total']])
            writer.writerow(['wins', results['wins']])
            writer.writerow(['winrate_percent', f"{results['winrate_percent']:.4f}"])
            writer.writerow(['average_guesses_on_wins', results['average_guesses_on_wins']])
            writer.writerow(['distribution', str(results['distribution'])])
            writer.writerow(['failed_words_count', len(results['failed_words'])])


if __name__ == '__main__':
    main()
