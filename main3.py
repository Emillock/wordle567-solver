import numpy as np
from eda_analysis import (
    load_words, separate_by_length, calculate_position_frequencies,
    plot_position_heatmap, plot_top_letters_per_position,
    calculate_overall_frequency, plot_overall_frequency,
    save_frequency_matrix
)

def main():
    print("\nLoading word list")
    words = load_words()
    print(f"Total words: {len(words):,}")
    
    print("\nSeparating by length")
    words_5, words_6, words_7 = separate_by_length(words)
    print(f"5-letter words: {len(words_5):,}")
    print(f"6-letter words: {len(words_6):,}")
    print(f"7-letter words: {len(words_7):,}")
    
    print("\nCalculating position frequencies")
    freq_5 = calculate_position_frequencies(words_5, 5)
    freq_6 = calculate_position_frequencies(words_6, 6)
    freq_7 = calculate_position_frequencies(words_7, 7)
    
    print("\nCalculating overall letter frequencies")
    overall_freq = calculate_overall_frequency(words)
    
    print("\nGenerating visualizations")
    
    plot_position_heatmap(freq_5, 5)
    plot_position_heatmap(freq_6, 6)
    plot_position_heatmap(freq_7, 7)
    
    plot_top_letters_per_position(freq_5, 5)
    plot_top_letters_per_position(freq_6, 6)
    plot_top_letters_per_position(freq_7, 7)
    
    plot_overall_frequency(overall_freq)
    
    print("\nSaving frequency data")
    save_frequency_matrix(freq_5, 5)
    save_frequency_matrix(freq_6, 6)
    save_frequency_matrix(freq_7, 7)
    
    print("\nEDA Complete!")
    print("Visualizations saved to: eda_visualizations/")
    print("Frequency data saved to: eda_data/")

if __name__ == "__main__":
    main()