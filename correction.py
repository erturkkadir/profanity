from collections import Counter
import re
import sys


def words(text):
    text = text.lower()
    return re.findall(r'\w+', text)


WORDS = Counter(words(open('txt.tr').read()))


def P(word, N=sum(WORDS.values())):
    """ Probability of Words """
    return WORDS[word] / N


def correction(word):
    """Most probable spelling correction if the word is """
    return max(candidates(word), key=P)


def candidates(word):
    "Generate possible spelling corrections for word"
    return known([word]) or known(edits1(word)) or known(edits2(word)) or [word]


def known(words):
    "The subset of words that appear in the dictionary pf WORDS"
    return set(w for w in words if w in WORDS)


def edits1(word):
    "all edits that are one edit away from word"
    letters = "abcçdefgğhıijklmnoöprsştuüvyz"
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


def edits2(word):
    """ll edits that are two edits away from word"""
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


def main():
    for arg in sys.argv[1:]:
        print(correction(arg))


if __name__ == "__main__":
    main()