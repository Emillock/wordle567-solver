import nltk
from nltk.corpus import wordnet

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')
    nltk.download('omw-1.4')

def load_words(filepath='valid_words.txt'):
    """Load all valid words"""
    with open(filepath, 'r') as file:
        words = [line.strip().lower() for line in file.readlines()]
    return words

def is_noun(word):
    """Check if word is a noun using WordNet"""
    synsets = wordnet.synsets(word)
    for synset in synsets:
        if synset.pos() == 'n':  # 'n' = noun
            return True
    return False

def is_proper_noun(word):
    """Check if word is a proper noun (capitalized name/place)"""
    # Most proper nouns will have their first synset as a proper noun
    synsets = wordnet.synsets(word)
    for synset in synsets:
        # Check if definition contains indicators of proper nouns
        definition = synset.definition().lower()
        if any(indicator in definition for indicator in ['capital of', 'city in', 'country in', 'person', 'biblical']):
            return True
    return False

def is_plural(word):
    """Check if word is likely plural"""
    if not word.endswith('s'):
        return False
    
    # Check if singular form exists
    singular = word[:-1]
    if is_noun(singular):
        return True
    
    # Handle words ending in 'es' (boxes -> box)
    if word.endswith('es') and len(word) > 3:
        singular = word[:-2]
        if is_noun(singular):
            return True
    
    if word.endswith('i'):  # like "abaci" -> "abacus"
        return True
    
    return False

def filter_5letter_nouns(words):
    """Filter for 5-letter singular common nouns"""
    five_letter = [w for w in words if len(w) == 5]
    
    nouns = []
    proper_nouns = []
    
    for word in five_letter:
        # Skip if first letter is uppercase (proper noun)
        if word[0].isupper():
            continue
            
        if is_noun(word) and not is_plural(word) and not is_proper_noun(word):
            nouns.append(word)
        elif is_noun(word) and is_proper_noun(word):
            proper_nouns.append(word)
    
    return nouns, proper_nouns

def main():
    print("Loading words...")
    words = load_words()
    print(f"Total words: {len(words):,}")
    
    print("\nFiltering 5-letter singular nouns...")
    nouns_5, proper_nouns = filter_5letter_nouns(words)
    print(f"5-letter common nouns (non-plural): {len(nouns_5):,}")
    print(f"5-letter proper nouns excluded: {len(proper_nouns):,}")
    
    # Save common nouns to file
    output_file = 'nouns_5letter.txt'
    with open(output_file, 'w') as f:
        for noun in sorted(nouns_5):
            f.write(noun + '\n')
    
    print(f"\nSaved to: {output_file}")
    
    # Show first 30 examples
    print("\nFirst 30 examples:")
    for noun in sorted(nouns_5)[:30]:
        print(f"  {noun}")
    
    # Manual verification sample
    print("\n\n=== VERIFICATION SAMPLE ===")
    print("Random 10 words to manually check:")
    import random
    sample = random.sample(sorted(nouns_5), min(10, len(nouns_5)))
    for word in sample:
        synsets = wordnet.synsets(word)
        if synsets:
            print(f"\n{word}:")
            print(f"  Definition: {synsets[0].definition()}")
        else:
            print(f"\n{word}: (no definition found)")

if __name__ == "__main__":
    main()