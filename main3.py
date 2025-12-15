import numpy as np
from eda_analysis import *

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
    
    print("Creating individual position bar charts...")
    plot_sorted_barchart_all_positions(freq_5, 5)
    plot_sorted_barchart_all_positions(freq_6, 6)
    plot_sorted_barchart_all_positions(freq_7, 7)
    
    print("Creating grid views...")
    plot_all_positions_grid(freq_5, 5)
    plot_all_positions_grid(freq_6, 6)
    plot_all_positions_grid(freq_7, 7)
    
    print("Creating top 5 comparison charts...")
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