from typing import List, Dict, Tuple, Optional
from collections import Counter, defaultdict
import copy


def compute_max_letter_counts(words: List[str], letters_number: int) -> Dict[str, int]:
    """Compute the maximum number of occurrences of each letter across the word list."""
    max_counts = defaultdict(int)
    for w in words:
        w = w.strip()
        if len(w) != letters_number:
            continue
        counts = Counter(w)
        for letter, c in counts.items():
            max_counts[letter] = max(max_counts[letter], c)
    return dict(max_counts)


def positional_frequencies(words: List[str], letters_number: int) -> List[Dict[str, int]]:
    """Return frequency counts of letters per position.
    Used to order domain values by positional frequency (LCV / heuristic).
    """
    freqs = [defaultdict(int) for _ in range(letters_number)]
    for w in words:
        w = w.strip()
        if len(w) != letters_number:
            continue
        for i, c in enumerate(w):
            freqs[i][c] += 1
    return freqs


class CSPSolver:
    def __init__(self, words: List[str], letters_number: int = 5):
        self.letters_number = letters_number
        self.words = [w.strip() for w in words if len(w.strip()) == letters_number]

        # Initial domain: all lowercase letters that appear in word list for that position
        freqs = positional_frequencies(self.words, letters_number)
        self.domains: List[List[str]] = []
        for i in range(letters_number):
            # sort letters by positional frequency desc so LCV/MRV heuristics have ordered values
            ordered = sorted(freqs[i].keys(), key=lambda c: -freqs[i][c])
            self.domains.append(list(ordered))

        # Global letter count bounds
        self.global_max_counts = compute_max_letter_counts(self.words, letters_number)
        # Start with very permissive min_counts = 0 for all letters
        self.min_counts: Dict[str, int] = defaultdict(int)
        # And start max_counts equal to global_max_counts for known letters; unknown letters get 0
        self.max_counts: Dict[str, int] = defaultdict(int, self.global_max_counts)

        # Keep guesses history
        self.guesses: List[str] = []

    def _update_counts_from_feedback(self, guess: str, feedback: List[str]) -> None:
        """Compute min and max letter counts from a single guess+feedback and merge with global bounds.

        Wordle rules handled (per-guess):
        - min_count for a letter = number of GREEN+YELLOW in this guess
        - If letter also has GRAY occurrences in same guess:
            * if min_count == 0 -> letter absent -> max_count_for_this_guess = 0
            * else -> extra guessed occurrences were gray -> max_count_for_this_guess = min_count
        - else (no gray) -> max_count_for_this_guess unchanged (we keep global max)

        Then we merge by:
        self.min_counts[letter] = max(self.min_counts[letter], min_count_for_guess)
        self.max_counts[letter] = min(self.max_counts.get(letter, self.global_max_counts.get(letter, 0)),
                                     max_count_for_guess)
        """
        letter_positions = defaultdict(lambda: {'G': 0, 'Y': 0, 'X': 0})
        # Map feedback to letters
        for i, ch in enumerate(guess):
            f = feedback[i]
            key = 'G' if f == 'GREEN' else ('Y' if f == 'YELLOW' else 'X')
            letter_positions[ch][key] += 1

        for ch, d in letter_positions.items():
            min_req = d['G'] + d['Y']
            if d['X'] > 0 and min_req == 0:
                # All occurrences gray -> letter absent
                max_for_guess = 0
            elif d['X'] > 0 and min_req > 0:
                # Some occurrences gray, some green/yellow -> exact min_req occurrences
                max_for_guess = min_req
            else:
                # No gray occurrences -> keep the previously known global max
                max_for_guess = self.global_max_counts.get(ch, 0)

            # Merge into global min/max
            self.min_counts[ch] = max(self.min_counts.get(ch, 0), min_req)
            # If we had a previous max bound, take the min (tighten)
            prev_max = self.max_counts.get(ch, self.global_max_counts.get(ch, 0))
            self.max_counts[ch] = min(prev_max, max_for_guess)

    def _apply_feedback_to_domains(self, guess: str, feedback: List[str]) -> None:
        """Forward checking.
        Apply positional pruning to domains using per-position feedback (GREEN/YELLOW/GRAY).

        - GREEN: set domain at position to that letter (singleton)
        - YELLOW: remove letter from that position's domain
        - GRAY: remove letter from all domains unless min_counts for that letter > 0 (i.e., we've
                already deduced the letter must appear elsewhere)
        After that, if any letter has max_count == 0, remove it from all domains.
        """
        for i, ch in enumerate(guess):
            fb = feedback[i]
            if fb == 'GREEN':
                # fix the letter at this position
                self.domains[i] = [ch]
            elif fb == 'YELLOW':
                # letter cannot be at this position
                if ch in self.domains[i]:
                    self.domains[i].remove(ch)
            else:  # GRAY
                # If we know the letter must appear some times (min_counts > 0), then we cannot
                # remove it everywhere; gray just indicates "not here" for this instance.
                # But to be conservative, remove from this position.
                if ch in self.domains[i]:
                    self.domains[i].remove(ch)

        # Remove letters with max_count == 0 from all domains (Global Cardinality Constraint)
        for ch, m in list(self.max_counts.items()):
            if m == 0:
                for i in range(self.letters_number):
                    if ch in self.domains[i]:
                        self.domains[i].remove(ch)

    def incorporate_feedback(self, guess: str, feedback: List[str]) -> None:
        """Public method to update CSP after a guess and its feedback.

        This performs:
         1. compute min/max letter counts implied by the feedback
         2. apply positional pruning
         3. perform a light consistency check
        """
        assert len(guess) == self.letters_number
        assert len(feedback) == self.letters_number
        self.guesses.append(guess)

        # 1) Update min/max counts from this guess
        self._update_counts_from_feedback(guess, feedback)

        # 2) Apply positional pruning
        self._apply_feedback_to_domains(guess, feedback)

        # 3) Lightweight arc-consistency style checks:
        #    - For every letter, check that the number of positions that could still hold it >= min_count
        for ch, min_req in self.min_counts.items():
            possible_positions = sum(1 for i in range(self.letters_number) if ch in self.domains[i])
            if possible_positions < min_req:
                raise ValueError(f"Inconsistency: letter '{ch}' requires {min_req} positions but only {possible_positions} available")

    def _word_matches_domains_and_counts(self, w: str) -> bool:
        # positional domains
        for i, c in enumerate(w):
            if c not in self.domains[i]:
                return False
        # min counts
        cnt = Counter(w)
        for ch, min_req in self.min_counts.items():
            if cnt.get(ch, 0) < min_req:
                return False
        # max counts
        for ch, max_req in self.max_counts.items():
            if cnt.get(ch, 0) > max_req:
                return False
        return True

    def candidate_words(self) -> List[str]:
        return [w for w in self.words if self._word_matches_domains_and_counts(w)]

    def solve_csp(self) -> Optional[str]:
        """Greedy selection based on heuristics.
        Run search to find a word consistent with current domains and global min/max counts.

        Returns a word (string) or None if inconsistent / no solution.
        """
        # Quick candidate filter first to speed things up
        candidates = self.candidate_words()
        print(f"Candidate words count: {len(candidates)}")
        if candidates:
            # prefer candidates that match domains and counts (and exist in dictionary)
            # score by sum of positional frequencies (higher is better)
            freqs = positional_frequencies(self.words, self.letters_number)
            def score_word(w: str) -> int: # heuristic scoring function
                return sum(freqs[i].get(w[i], 0) for i in range(self.letters_number))
            candidates.sort(key=score_word, reverse=True)
            return candidates[0]

class DummySolver:
    """A very simple baseline solver for comparison.


    Behavior:
    - Keeps the original word list order (no frequency-based ordering).
    - Does NOT perform domain filtering or ordering; domains remain the full alphabet.
    - On guess(), returns the first word from the original list that hasn't been guessed yet.
    """
    def __init__(self, words: List[str], letters_number: int = 5):
        self.letters_number = letters_number
        self.words = [w.strip() for w in words if len(w.strip()) == letters_number]
        # Domains are kept trivial and unordered (full alphabet, fixed order)
        import string
        self.domains = [list(string.ascii_lowercase) for _ in range(letters_number)]
        self.guesses: List[str] = []
        self.feedback_history: List[Tuple[str, List[str]]] = []


    def update_csp_domains(self, feedback: List[str]) -> None:
        """Accepts feedback but intentionally does not modify domains.


        This keeps the solver *dumb* so it can be compared fairly to the CSP solver.
        """
        if not self.guesses:
            return
        guess = self.guesses[-1]
        self.feedback_history.append((guess, feedback))
        # No domain pruning performed.


    def guess(self) -> Optional[str]:
        """Return the first word from the original list that hasn't been guessed yet."""
        for w in self.words:
            if w not in self.guesses:
                self.guesses.append(w)
                return w
        return None