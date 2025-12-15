import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import spacy

nlp = spacy.load("en_core_web_sm")

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')
    nltk.download('omw-1.4')

def is_proper_noun_spacy(word, sentence=None):
    """
    Uses spaCy token.pos_ == 'PROPN' or token.tag_ in ('NNP','NNPS').
    If sentence provided, finds the matching token; otherwise tags the word alone.
    """
    text = sentence if sentence else word
    doc = nlp(text)
    for token in doc:
        if token.text == word or token.text.lower() == word.lower():
            if token.pos_ == "PROPN" or token.tag_ in ("NNP", "NNPS"):
                return True
            if token.ent_type_:
                return True
            return False
    doc2 = nlp(word)
    t = doc2[0]
    return t.pos_ == "PROPN" or t.tag_ in ("NNP", "NNPS") or bool(t.ent_type_)

def load_words_file(filepath='valid_words.txt'):
    """Load all valid words"""
    with open(filepath, 'r') as file:
        word_list = [line.strip().lower() for line in file.readlines()]
    return word_list

def is_english_word(word):
    """Check if word exists in WordNet (real English word)"""
    return len(wordnet.synsets(word)) > 0

def is_regular_plural(word):
    """Check if word is a REGULAR plural"""
    lemmatizer = WordNetLemmatizer()
    lemma = lemmatizer.lemmatize(word, pos='n')
    
    if lemma != word:
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
    
    print(f"\nProcessing {word_length}-letter words")
    count = 0
    
    for word in word_list:
        if len(word) != word_length:
            continue
        
        count += 1
        if count % 1000 == 0:
            print(f"  Processed {count} words")
        
        if not is_english_word(word):
            continue
        
        if is_proper_noun_spacy(word):
            continue
        
        if is_regular_plural(word):
            continue
        
        if is_regular_past_tense(word):
            continue
        
        filtered.append(word)
    
    return filtered

def main():
    print("\nLoading valid_words.txt")
    word_list = load_words_file()
    print(f"Total words: {len(word_list):,}")
    
    print("Rules: (1) Real English word (2) No proper nouns (3) No regular plurals (4) No regular past tense")
    
    answers_5 = filter_by_wordle_rules(word_list, 5)
    print(f"✓ 5-letter valid answers: {len(answers_5):,}")
    
    answers_6 = filter_by_wordle_rules(word_list, 6)
    print(f"✓ 6-letter valid answers: {len(answers_6):,}")
    
    answers_7 = filter_by_wordle_rules(word_list, 7)
    print(f"✓ 7-letter valid answers: {len(answers_7):,}")
    
    print("\nSaving filtered lists")
    
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
    
    print("\nFirst 50 5-letter answers:")
    for i, word in enumerate(sorted(answers_5)[:50], 1):
        print(f"  {i:2}. {word}")

if __name__ == "__main__":
    main()