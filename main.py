import sys
import unicodedata
from collections import Counter, defaultdict

def _raise_if_unicode(s):
    # double check words are normalized
    try:
        return ''.join(
            c for c in unicodedata.normalize('NFD', s)
            if unicodedata.category(c) != 'Mn'
        )
    except Exception as e:
        print e
        return s

# STEP 1: DATA SOURCE
#   - download data from www.pallier.org/ressources/dicofr/liste.de.mots.francais.frgut.txt
#   - clean data (use _raise_if_unicode to double check that it's clean)
#   - drop words with 8+ letters
#   - save in own files

if False:
    words_files = []
    with open('data/words/all.txt', 'r') as all_file:
        for i in range(2, 8):
            f = open('data/words/%s.txt' % i, 'w')
            words_files.append(f)
        while True:
            word = all_file.readline()[:-1]
            if not word:
                break
            if len(word) > 7 or len(word) < 2:
                continue
            words_files[len(word) - 1].write('%s\n' % word)
            print word
        for i in range(2, 8):
            words_files[i].close()

# STEP 2: GET POSSIBLE WORDS
if len(sys.argv) < 6:
    print 'Need to run `python main.py "ABCDEFGH" "1 1 1 2 4 10 1 2" "IJ" "1 1" "x2 _ _ _ _ _ +10"`'
    exit(1)
regular_letters = [l for l in sys.argv[1]]
regular_letters_values = sys.argv[2].split(' ')
golden_letters = [l for l in sys.argv[3]]
golden_letters_values = sys.argv[4].split(' ')
available_letters = Counter(regular_letters + golden_letters)
playground = sys.argv[5].split(' ')
debug = len(sys.argv) == 7


def is_word_possible(word, available_letters):
    word_letters = Counter(word)
    for (l, occ) in word_letters.most_common():
        if available_letters[l] < occ:
            return False
    return True


possible_words = []

for i in range(7, 1, -1):
    with open('data/words/%s.txt' % i, 'r') as f:
        for word in f:
            word = word[:-1]
            if debug:
                print 'considering', word
            if(is_word_possible(word, available_letters)):
                possible_words.append(word)

if debug:
    print 'LETTERS', available_letters.most_common()
    print 'WORDS', possible_words


def word_score(
        word, playground,
        regular_letters, regular_letters_values,
        golden_letters, golden_letters_values
    ):
    """
        current rule: use all golden letters
    """
    for l in golden_letters:
        if l not in word:
            return -1

    score = 0
    for pos, l in enumerate(word):
        mult = 1
        plus = 0
        if playground[pos].startswith('x'):
            mult = int(playground[pos][1:])
        if playground[pos].startswith('+'):
            plus = int(playground[pos][1:])

        try:
            letter_value = regular_letters_values[regular_letters.index(l)]
        except ValueError:
            letter_value = golden_letters_values[golden_letters.index(l)]
        score += mult * int(letter_value) + plus
    return score


# STEP 3: FIND BEST WORDS
possible_values = defaultdict(list)
for word in possible_words:
    score = word_score(
        word, playground,
        regular_letters, regular_letters_values,
        golden_letters, golden_letters_values
    )
    possible_values[score].append(word)

keys = sorted(possible_values.keys())[::-1]
for key in keys[:3]:
    print key, possible_values[key]
