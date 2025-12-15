import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from collections import Counter

from utils import load_valid_answers

def load_words(filepath='valid_words.txt'):
    """Load all valid words from the dataset"""
    with open(filepath, 'r') as file:
        words = [line.strip().lower() for line in file.readlines()]
    return words
def separate_by_length():
    """Separate words into 5, 6, and 7-letter categories"""
    words_5 = load_valid_answers(5)
    words_6 = load_valid_answers(6)
    words_7 = load_valid_answers(7)
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


def alphabet_order_by_position(words=None, word_length=None, freq_matrix=None, uppercase=True):
    # Obtain freq_matrix if not provided
    if freq_matrix is None:
        if words is None or word_length is None:
            raise ValueError("Either provide freq_matrix or both words and word_length")
        freq_matrix = calculate_position_frequencies(words, word_length)

    # Ensure freq_matrix is numpy array
    freq_matrix = np.asarray(freq_matrix)

    if freq_matrix.ndim != 2 or freq_matrix.shape[1] != 26:
        raise ValueError("freq_matrix must be shape (positions, 26)")

    letters = [chr(i) for i in range(ord('a'), ord('z')+1)]
    ordered = []

    for pos in range(freq_matrix.shape[0]):
        # sort indices by frequency descending
        sorted_indices = np.argsort(freq_matrix[pos])[::-1]
        ordered_letters = [letters[i] for i in sorted_indices]
        if uppercase:
            ordered_letters = [l.upper() for l in ordered_letters]
        ordered.append(ordered_letters)

    # Print result nicely
    for pos, letters_list in enumerate(ordered):
        print(f"Position {pos+1}: {' '.join(letters_list)}")

    return ordered

def plot_sorted_barchart_all_positions(freq_matrix, word_length, output_dir='eda_visualizations'):
    """Sorted bar charts for each position - much clearer than heatmap!"""
    os.makedirs(output_dir, exist_ok=True)
    
    letters = [chr(i) for i in range(ord('a'), ord('z')+1)]
    
    # Create one chart per position
    for pos in range(word_length):
        fig, ax = plt.subplots(figsize=(14, 8))
        
        pos_freq = freq_matrix[pos]
        # Sort by frequency (descending)
        sorted_indices = np.argsort(pos_freq)[::-1]
        sorted_letters = [letters[i].upper() for i in sorted_indices]
        sorted_values = [pos_freq[i] for i in sorted_indices]
        
        # Color bars - highlight top 5
        colors = ['#e74c3c' if i < 5 else '#3498db' for i in range(26)]
        
        bars = ax.bar(sorted_letters, sorted_values, color=colors)
        ax.set_xlabel('Letter', fontsize=14, fontweight='bold')
        ax.set_ylabel('Frequency (%)', fontsize=14, fontweight='bold')
        ax.set_title(f'Letter Frequency at Position {pos+1} ({word_length}-Letter Words)', 
                     fontsize=16, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels on top of bars for top 10
        for i in range(min(10, len(bars))):
            height = bars[i].get_height()
            ax.text(bars[i].get_x() + bars[i].get_width()/2., height,
                   f'{sorted_values[i]:.1f}%',
                   ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        plt.tight_layout()
        filename = f'{output_dir}/barchart_pos{pos+1}_{word_length}letter.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved: {filename}")

def plot_all_positions_grid(freq_matrix, word_length, output_dir='eda_visualizations'):
    """Grid view of all positions - easier to compare"""
    os.makedirs(output_dir, exist_ok=True)
    
    letters = [chr(i) for i in range(ord('a'), ord('z')+1)]
    
    # Create subplots in a grid
    cols = min(3, word_length)
    rows = (word_length + cols - 1) // cols
    
    fig, axes = plt.subplots(rows, cols, figsize=(7*cols, 5*rows))
    if word_length == 1:
        axes = np.array([axes])
    axes = axes.flatten()
    
    for pos in range(word_length):
        ax = axes[pos]
        
        pos_freq = freq_matrix[pos]
        sorted_indices = np.argsort(pos_freq)[::-1]
        
        top_10_indices = sorted_indices[:10]
        top_letters = [letters[i].upper() for i in top_10_indices]
        top_values = [pos_freq[i] for i in top_10_indices]
        
        colors = ['#e74c3c' if i < 3 else '#3498db' for i in range(10)]
        bars = ax.bar(top_letters, top_values, color=colors)
        
        ax.set_xlabel('Letter', fontsize=11)
        ax.set_ylabel('Frequency (%)', fontsize=11)
        ax.set_title(f'Position {pos+1}', fontsize=13, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        # Add values on bars
        for i, (bar, val) in enumerate(zip(bars, top_values)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{val:.1f}%',
                   ha='center', va='bottom', fontsize=8)
    
    # Hide extra subplots
    for idx in range(word_length, len(axes)):
        axes[idx].set_visible(False)
    
    plt.suptitle(f'Top 10 Letters at Each Position - {word_length}-Letter Words', 
                 fontsize=18, fontweight='bold')
    plt.tight_layout()
    
    filename = f'{output_dir}/grid_view_{word_length}letter.png'
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
        
        # Add percentage labels with better spacing
        for i, (letter, val) in enumerate(zip(top_letters, top_values)):
            axes[pos].text(val + 0.5, i, f'{val:.1f}%', va='center', fontsize=9)
        
        # Add padding to x-axis so labels don't overlap
        max_val = max(top_values)
        axes[pos].set_xlim(0, max_val * 1.15)  # Add 15% padding
    
    plt.suptitle(f'Top 5 Letters by Position - {word_length}-Letter Words', 
                 fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    filename = f'{output_dir}/top_letters_{word_length}letter.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {filename}")

def calculate_overall_frequency(words):
    """Calculate overall letter frequency"""
    all_letters = ''.join(words)
    counter = Counter(all_letters)
    total = sum(counter.values())
    
    freq_dict = {letter: (count/total)*100 for letter, count in counter.items()}
    return freq_dict

def plot_overall_frequency(freq_dict, output_dir='eda_visualizations'):
    """Bar chart of overall letter frequencies - SORTED by frequency"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Sort by frequency (descending)
    sorted_items = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)
    letters = [item[0].upper() for item in sorted_items]
    frequencies = [item[1] for item in sorted_items]
    
    plt.figure(figsize=(14, 6))
    
    # Color bars - highlight vowels
    vowels = set('aeiou')
    colors = ['coral' if letter.lower() in vowels else 'steelblue' for letter in letters]
    
    bars = plt.bar(letters, frequencies, color=colors)
    plt.title('Overall Letter Frequency Across All Words (Sorted)', fontsize=16, fontweight='bold')
    plt.ylabel('Frequency (%)', fontsize=12)
    plt.xlabel('Letter', fontsize=12)
    plt.xticks(fontsize=10)
    plt.grid(axis='y', alpha=0.3)
    
    for i in range(min(10, len(bars))):
        height = bars[i].get_height()
        plt.text(bars[i].get_x() + bars[i].get_width()/2., height,
                f'{frequencies[i]:.1f}%',
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # Create custom legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='coral', label='Vowels'),
                      Patch(facecolor='steelblue', label='Consonants')]
    plt.legend(handles=legend_elements, loc='upper right')
    
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