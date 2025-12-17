import argparse
import csv
import sys
import time
from collections import defaultdict
from statistics import mean

from wordle_game import generate_wordle_feedback
from solver import CSPSolver


def plot_distribution(distribution: dict, out_path: str = 'distribution.png', title: str = None):
    """Create and save a bar chart from the distribution mapping.

    distribution: mapping where keys are attempt counts (int or numeric strings) and/or 'fail'.
    out_path: path to save the PNG image.
    title: optional plot title.
    """
    try:
        import matplotlib.pyplot as plt
    except Exception:
        print('matplotlib is not available. Install it (pip install matplotlib) to enable plotting.')
        return

    # Separate numeric keys (1,2,3..) and non-numeric keys (like 'fail')
    numeric_items = {}
    other_items = {}
    for k, v in distribution.items():
        try:
            nk = int(k)
            numeric_items[nk] = v
        except Exception:
            other_items[str(k)] = v

    if not numeric_items and not other_items:
        print('No distribution data found to plot.')
        return

    xs_numeric = sorted(numeric_items.keys())
    xs_other = sorted(other_items.keys(), key=lambda x: (x != 'fail', x))

    # Build labels and values: numeric labels first, then non-numeric (fail) last
    labels = [str(x) for x in xs_numeric] + xs_other
    values = [numeric_items[x] for x in xs_numeric] + [other_items[x] for x in xs_other]

    x_positions = list(range(len(labels)))

    # Convert raw counts to percentages of the total answers
    total = sum(values)
    if total == 0:
        print('No distribution data found to plot.')
        return
    percents = [v / total * 100 for v in values]

    plt.figure(figsize=(max(6, len(labels) * 0.8), 5))
    # color fail bar differently if present
    colors = []
    for lab in labels:
        if lab == 'fail':
            colors.append('C3')
        else:
            colors.append('C0')

    plt.bar(x_positions, percents, color=colors)
    plt.xlabel('Guess count')
    plt.ylabel('Percentage of answers (%)')
    if title:
        plt.title(title)
    plt.xticks(x_positions, labels)
    # set y limit a little above the max percent for nicer layout
    plt.ylim(0, min(100, max(percents) * 1.1))
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    print(f"Saved distribution plot to {out_path}")


def load_answers(path: str) -> list:
    with open(path, 'r', encoding='utf-8') as f:
        return [w.strip() for w in f if w.strip()]


def simulate(answers: list, max_guesses: int = 6, limit: int = None):
    total = 0
    wins = 0
    guess_counts = []
    distribution = defaultdict(int)
    failed_words = []
    game_times = []

    total_start = time.perf_counter()
    for idx, target in enumerate(answers):
        if limit and idx >= limit:
            break
        total += 1
        # measure single-game time
        game_start = time.perf_counter()
        # instantiate solver fresh for each target

        solver = CSPSolver(letters_number=len(target))
        guess_func = None

        attempts = 0
        solved = False

        while attempts < max_guesses:
            attempts += 1
            guess = solver.solve_csp()
            if guess is None:
                # no candidate -> fail early
                break

            feedback = generate_wordle_feedback(target, guess)


            # solver will record guess when incorporate_feedback is called
            solver.incorporate_feedback(guess, feedback)

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

        # record elapsed time for this game
        game_elapsed = time.perf_counter() - game_start
        game_times.append(game_elapsed)

        # simple progress every 100 games
        if total % 100 == 0:
            print(f"Simulated {total} games... wins so far: {wins}")

    winrate = (wins / total) * 100 if total else 0
    avg_guesses = mean(guess_counts) if guess_counts else float('nan')
    total_elapsed = time.perf_counter() - total_start
    avg_time_per_game = mean(game_times) if game_times else float('nan')

    results = {
        'total': total,
        'wins': wins,
        'winrate_percent': winrate,
        'average_guesses_on_wins': avg_guesses,
        'total_time_seconds': total_elapsed,
        'average_time_per_game_seconds': avg_time_per_game,
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
    # timing info
    if 'total_time_seconds' in results:
        print(f"Total simulation time: {results['total_time_seconds']:.3f} s")
    if 'average_time_per_game_seconds' in results:
        print(f"Average time per game: {results['average_time_per_game_seconds']*1000:.3f} ms")
    print('\nDistribution:')
    for k in sorted(results['distribution'].keys(), key=lambda x: (x=='fail', x)):
        print(f"  {k}: {results['distribution'][k]}")
    print(f"\nFailed words ({len(results['failed_words'])}): {results['failed_words'][:20]}{'...' if len(results['failed_words'])>20 else ''}")


def main():
    parser = argparse.ArgumentParser(description='Simulate Wordle across all answers and compute metrics')
    parser.add_argument('--letters_number', type=int, default=7)
    parser.add_argument('--max-guesses', type=int, default=6)
    parser.add_argument('--limit', type=int, help='Limit number of answers to simulate (for quick tests)')
    parser.add_argument('--save-csv', type=str, help='Optional path to save per-word results CSV')
    parser.add_argument('--plot', type=str, help='Optional path to save distribution bar chart PNG', default="yes")

    args = parser.parse_args()
    letters_number = args.letters_number
    answers = load_answers(f'word_lists/wordle_answers_{letters_number}letter.txt')
    if not answers:
        print('No letters_number loaded.')
        sys.exit(1)

    results = simulate(answers, max_guesses=args.max_guesses, limit=args.limit)
    pretty_print(results)

    # Optionally create a bar chart of guess distribution (numeric guess counts only)
    if args.plot:
        title = f"Distribution ({letters_number}-letter)"
        plot_distribution(results.get('distribution', {}), out_path=args.plot, title=title)

    if args.save_csv:
        # Write basic summary for failed words
        with open(args.save_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['metric', 'value'])
            writer.writerow(['total', results['total']])
            writer.writerow(['wins', results['wins']])
            writer.writerow(['winrate_percent', f"{results['winrate_percent']:.4f}"])
            writer.writerow(['average_guesses_on_wins', results['average_guesses_on_wins']])
            # include timing info if present
            if 'total_time_seconds' in results:
                writer.writerow(['total_time_seconds', f"{results['total_time_seconds']:.6f}"])
            if 'average_time_per_game_seconds' in results:
                writer.writerow(['average_time_per_game_seconds', f"{results['average_time_per_game_seconds']:.6f}"])
            writer.writerow(['distribution', str(results['distribution'])])
            writer.writerow(['failed_words_count', len(results['failed_words'])])


if __name__ == '__main__':
    main()
