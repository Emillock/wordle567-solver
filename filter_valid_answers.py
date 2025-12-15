import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet, words

# Download required data
try:
    nltk.data.find('corpora/wordnet')
    nltk.data.find('corpora/words')
except LookupError:
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    nltk.download('words')
    nltk.download('averaged_perceptron_tagger')

def load_words_file(filepath='valid_words.txt'):
    """Load all valid words"""
    with open(filepath, 'r') as file:
        word_list = [line.strip().lower() for line in file.readlines()]
    return word_list

def is_english_word(word):
    """Check if word exists in WordNet (real English word)"""
    # Must have at least one synset in WordNet
    return len(wordnet.synsets(word)) > 0

def is_regular_plural(word):
    """Check if word is a REGULAR plural"""
    lemmatizer = WordNetLemmatizer()
    lemma = lemmatizer.lemmatize(word, pos='n')
    
    if lemma != word:
        # Regular plural patterns
        if word == lemma + 's':
            return True
        if word == lemma + 'es':
            return True
        if lemma.endswith('y') and word == lemma[:-1] + 'ies':
            return True
    
    return False

def is_regular_past_tense(word):
    """Check if word is a REGULAR past tense"""
    lemmatizer = WordNetLemmatizer()
    lemma = lemmatizer.lemmatize(word, pos='v')
    
    if lemma != word and word.endswith('ed'):
        # Regular past tense patterns
        if word == lemma + 'ed':
            return True
        if lemma.endswith('e') and word == lemma + 'd':
            return True
        if len(lemma) >= 3 and word == lemma + lemma[-1] + 'ed':
            return True
        if lemma.endswith('y') and word == lemma[:-1] + 'ied':
            return True
    
    return False

def filter_by_wordle_rules(word_list, word_length):
    """Filter words by Wordle answer rules"""
    filtered = []
    
    print(f"\nProcessing {word_length}-letter words...")
    count = 0
    
    for word in word_list:
        if len(word) != word_length:
            continue
        
        count += 1
        if count % 1000 == 0:
            print(f"  Processed {count} words...")
        
        # RULE 1: Must be a real English word in WordNet
        if not is_english_word(word):
            continue
        
        # RULE 2: No regular plurals (-s, -es, -ies)
        if is_regular_plural(word):
            continue
        
        # RULE 3: No regular past tense (-ed)
        if is_regular_past_tense(word):
            continue
        
        filtered.append(word)
    
    return filtered

def main():
    print("="*60)
    print("FILTERING VALID WORDLE ANSWERS")
    print("="*60)
    
    # Load all words
    print("\nLoading valid_words.txt")
    word_list = load_words_file()
    print(f"Total words: {len(word_list):,}")
    
    # Filter for each length
    print("\nFiltering by Wordle rules")
    print("Rules: (1) Real English word (2) No regular plurals (3) No regular past tense")
    
    answers_5 = filter_by_wordle_rules(word_list, 5)
    print(f"✓ 5-letter valid answers: {len(answers_5):,}")
    
    answers_6 = filter_by_wordle_rules(word_list, 6)
    print(f"✓ 6-letter valid answers: {len(answers_6):,}")
    
    answers_7 = filter_by_wordle_rules(word_list, 7)
    print(f"✓ 7-letter valid answers: {len(answers_7):,}")
    
    # Save
    print("\n Saving filtered lists")
    
    with open('answers_5letter.txt', 'w') as f:
        for word in sorted(answers_5):
            f.write(word + '\n')
    print(f"✓ Saved {len(answers_5):,} words to answers_5letter.txt")
    
    with open('answers_6letter.txt', 'w') as f:
        for word in sorted(answers_6):
            f.write(word + '\n')
    print(f"✓ Saved {len(answers_6):,} words to answers_6letter.txt")
    
    with open('answers_7letter.txt', 'w') as f:
        for word in sorted(answers_7):
            f.write(word + '\n')
    print(f"✓ Saved {len(answers_7):,} words to answers_7letter.txt")
    
    # Show first 50 examples for verification
    print("\First 50 5-letter answers:")
    for i, word in enumerate(sorted(answers_5)[:50], 1):
        print(f"  {i:2}. {word}")


if __name__ == "__main__":
    main()