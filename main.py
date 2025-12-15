from solver import CSPSolver, load_valid_words

if __name__ == '__main__':
    # tiny example word list (replace with real wordlist)
    WORDS = load_valid_words('valid_words.txt', letters_number=5)
    
    csp = CSPSolver(WORDS, letters_number=5)

    # Example: suppose we guessed 'crate' and feedback was [GRAY, YELLOW, GRAY, GREEN, GRAY]
    # meaning: c=X, r=Y, a=X, t=G, e=X
    guess = 'crate'
    feedback = ['GRAY', 'YELLOW', 'GRAY', 'GREEN', 'GRAY']
    csp.incorporate_feedback(guess, feedback)

    print('Domains after feedback:')
    for i, d in enumerate(csp.domains):
        print(i, d)

    print('min_counts:', dict(csp.min_counts))
    print('max_counts:', dict(csp.max_counts))

    next_guess = csp.solve_csp()
    print('Next guess suggestion:', next_guess)