import numpy as np
from eda_analysis import load_words, separate_by_length, calculate_position_frequencies

def main():
    print("\nLoading word list")
    words = load_words()
    print(f"Total words: {len(words):,}")
    
    print("\nSeparating by length")
    words_5, words_6, words_7 = separate_by_length(words)
    print(f"5-letter words: {len(words_5):,}")
    print(f"6-letter words: {len(words_6):,}")
    print(f"7-letter words: {len(words_7):,}")
    
    print("\nCalculating position frequencies for 5-letter words")
    freq_5 = calculate_position_frequencies(words_5, 5)
    
    # Show top 3 letters for position 1
    letters = [chr(i) for i in range(ord('a'), ord('z')+1)]
    pos_0_freq = freq_5[0]
    top_3_indices = np.argsort(pos_0_freq)[-3:][::-1]
    
    print("\nTop 3 letters at position 1:")
    for idx in top_3_indices:
        print(f"  {letters[idx]}: {pos_0_freq[idx]:.2f}%")

if __name__ == "__main__":
    main()