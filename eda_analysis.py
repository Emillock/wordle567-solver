import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def load_words(filepath='valid_words.txt'):
    """Load all valid words from the dataset"""
    with open(filepath, 'r') as file:
        words = [line.strip().lower() for line in file.readlines()]
    return words
def separate_by_length(words):
    """Separate words into 5, 6, and 7-letter categories"""
    words_5 = [w for w in words if len(w) == 5]
    words_6 = [w for w in words if len(w) == 6]
    words_7 = [w for w in words if len(w) == 7]
    return words_5, words_6, words_7

def calculate_position_frequencies(words, word_length):
    """Calculate letter frequency for each position"""
    freq_matrix = np.zeros((word_length, 26))
    
    for word in words:
        for pos, letter in enumerate(word):
            if letter.isalpha():
                letter_idx = ord(letter) - ord('a')
                freq_matrix[pos][letter_idx] += 1
    
    for pos in range(word_length):
        total = freq_matrix[pos].sum()
        if total > 0:
            freq_matrix[pos] = (freq_matrix[pos] / total) * 100
    
    return freq_matrix

def plot_position_heatmap(freq_matrix, word_length, output_dir='eda_visualizations'):
    """Create heatmap of letter frequencies by position"""
    os.makedirs(output_dir, exist_ok=True)
    
    letters = [chr(i) for i in range(ord('a'), ord('z')+1)]
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(freq_matrix.T, 
                xticklabels=[f'Pos {i+1}' for i in range(word_length)],
                yticklabels=letters,
                cmap='YlOrRd',
                annot=False,
                cbar_kws={'label': 'Frequency (%)'})
    
    plt.title(f'Letter Frequency Heatmap - {word_length}-Letter Words', 
              fontsize=16, fontweight='bold')
    plt.xlabel('Position in Word', fontsize=12)
    plt.ylabel('Letter', fontsize=12)
    plt.tight_layout()
    
    filename = f'{output_dir}/heatmap_{word_length}letter.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {filename}")

def plot_top_letters_per_position(freq_matrix, word_length, output_dir='eda_visualizations'):
    """Bar charts showing top 5 letters for each position"""
    os.makedirs(output_dir, exist_ok=True)
    
    letters = [chr(i) for i in range(ord('a'), ord('z')+1)]
    
    fig, axes = plt.subplots(1, word_length, figsize=(4*word_length, 5))
    if word_length == 1:
        axes = [axes]
    
    for pos in range(word_length):
        pos_freq = freq_matrix[pos]
        top_5 = np.argsort(pos_freq)[-5:][::-1]
        top_letters = [letters[i].upper() for i in top_5]
        top_values = [pos_freq[i] for i in top_5]
        
        axes[pos].barh(top_letters, top_values, color='teal')
        axes[pos].set_xlabel('Frequency (%)', fontsize=10)
        axes[pos].set_title(f'Position {pos+1}', fontsize=12, fontweight='bold')
        axes[pos].invert_yaxis()
        
        # Add percentage labels
        for i, (letter, val) in enumerate(zip(top_letters, top_values)):
            axes[pos].text(val, i, f' {val:.1f}%', va='center', fontsize=9)
    
    plt.suptitle(f'Top 5 Letters by Position - {word_length}-Letter Words', 
                 fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    filename = f'{output_dir}/top_letters_{word_length}letter.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {filename}")

def calculate_overall_frequency(words):
    """Calculate overall letter frequency"""
    from collections import Counter
    all_letters = ''.join(words)
    counter = Counter(all_letters)
    total = sum(counter.values())
    
    freq_dict = {letter: (count/total)*100 for letter, count in counter.items()}
    return freq_dict

def plot_overall_frequency(freq_dict, output_dir='eda_visualizations'):
    """Bar chart of overall letter frequencies"""
    os.makedirs(output_dir, exist_ok=True)
    
    letters = sorted(freq_dict.keys())
    frequencies = [freq_dict[l] for l in letters]
    
    plt.figure(figsize=(14, 6))
    bars = plt.bar(letters, frequencies, color='steelblue')
    plt.title('Overall Letter Frequency Across All Words', fontsize=16, fontweight='bold')
    plt.ylabel('Frequency (%)', fontsize=12)
    plt.xlabel('Letter', fontsize=12)
    plt.xticks(fontsize=10)
    
    # Highlight vowels
    vowels = set('aeiou')
    for i, letter in enumerate(letters):
        if letter in vowels:
            bars[i].set_color('coral')
    
    plt.legend(['Consonants', 'Vowels'], loc='upper right')
    plt.tight_layout()
    
    filename = f'{output_dir}/overall_frequency.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {filename}")

def save_frequency_matrix(freq_matrix, word_length, output_dir='eda_data'):
    """Save frequency matrix to CSV for Emil's solver"""
    os.makedirs(output_dir, exist_ok=True)
    
    letters = [chr(i) for i in range(ord('a'), ord('z')+1)]
    
    import pandas as pd
    df = pd.DataFrame(freq_matrix.T, 
                      index=letters,
                      columns=[f'Pos_{i+1}' for i in range(word_length)])
    
    filename = f'{output_dir}/freq_{word_length}letter.csv'
    df.to_csv(filename)
    print(f"✓ Saved frequency data: {filename}")