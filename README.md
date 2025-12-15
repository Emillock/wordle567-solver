## wordle567-solver

A 5-, 6-, and 7-letter Wordle solver & simulator project that contains:

- CSP-based solver implementation (`solver.py`).
- Wordle game mechanics and feedback generator in `wordle_game.py`.
- A simulator script `evaluation.py` that runs the solver against a list of answer words and reports metrics (win rate, guess distribution, failures).
- Word lists under `word_lists/` (valid words and sampled answer lists for 5, 6, and 7-letter simulations).

This repository is intended for running automated simulations of Wordle-like games, comparing solver strategies, and performing exploratory analysis (EDA) on results.

## Requirements

- Python 3.12 or newer (pyproject specifies >=3.12).
- The project lists a few Python dependencies in `pyproject.toml` (matplotlib, nltk, numpy, seaborn, spacy). These are optional unless you run the EDA scripts.

## Setup (Windows / cmd.exe)

This project can be set up using a UV environment (recommended for reproducible developer environments) or with a plain Python virtual environment + pip. UV (from Astral) provides environment management and dependency syncing; official installation instructions are available at:

https://docs.astral.sh/uv/getting-started/installation/

Using UV (recommended)

- Follow the official UV installation guide at the link above for your platform.
- After installing `uv`, consult the UV docs to create and sync an environment for this repository. The exact commands depend on your UV configuration and platform; please follow the official guide. Example (illustrative) workflow once `uv` is installed:

```bash
.venv\Scripts\activate
uv sync
```

## Files and run order

Suggested minimal run order to reproduce simulations and analyze results:

1) Run a single interactive simulation (quick test):

```
uv run main.py
```

`main.py` runs one game using the CSP solver against a randomly selected target from the 5-letter valid words list and prints per-guess feedback.

2) Run batch simulations across an answer list (recommended for metrics):

```
uv run simulate_all.py --answers word_lists\wordle_answers_5letter_new.txt --solver csp --max-guesses 6 --limit 317
```

Options:
- `--answers`: path to the answer list file (one word per line).
- `--max-guesses`: maximum allowed guesses per game (default 6).
- `--limit`: limit number of answers (useful for quick tests).
- `--save-csv`: optional path to write a small CSV summary.

Example to run the 6-letter sampled answers with the Dummy solver:

```
uv run simulate_all.py --answers word_lists\wordle_answers_6letter.txt --solver dummy --max-guesses 6
```

4) (Optional) Exploratory analysis

- Use `eda_analysis.py` to generate visualizations from simulation data. That script depends on matplotlib / seaborn. You may need to adapt it to load the CSV summary produced by `simulate_all.py`.


## Quick troubleshooting

- Python version errors: ensure `python --version` shows 3.12+.
- Missing packages: activate your venv and run the pip install command above.
- Permission errors on Windows: run `cmd.exe` as a normal user (no admin required) and ensure files are not locked by other programs.


