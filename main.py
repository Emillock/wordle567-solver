from solver import *


def main():
    allowed_letters = [lowercase_letters, lowercase_letters,
                       lowercase_letters, lowercase_letters, lowercase_letters]
    # allowed_letters = [["h"], ["y"],
    #                    lowercase_letters, lowercase_letters, lowercase_letters]
    print(solve_wordle(allowed_letters, 5))


if __name__ == "__main__":
    main()
