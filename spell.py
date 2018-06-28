import re
from collections import Counter

def words(text): return re.findall(r'\w+', text.lower())


def P(word, WORDS): 
    "Probability of `word`."
    N = sum(WORDS.values())
    return WORDS[word] / N

def correction(word,WORDS): 
    "Most probable spelling correction for word."
    return max(candidates(word,WORDS), P(word,WORDS))

def candidates(word,WORDS): 
    "Generate possible spelling corrections for word."
    # print known([word])
    # print known(edits1(word))
    # print known(edits2(word))
    # print [word]    
    return (known([word],WORDS) or known(edits1(word),WORDS) or known(edits2(word),WORDS) or set([word]))

def known(words,WORDS): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


def spellcorrection(file,word):
    WORDS = Counter(words(open(file).read()))
    return correction(word,WORDS)

