from dataclasses import dataclass

@dataclass
class NameCase:
    camel: str
    kebab: str
    pascal: str
    spaced: str
    snake: str
    upper: str

    def dict(self):
        return self.__dict__

def case_map(word: str) -> NameCase:
    words = []
    start = 0
    prev = None

    for i in range(len(word)):
        curr = word[i]
        prev = None
        next = None
        if i != 0:
            prev = word[i - 1]
        if i < len(word) - 1:
            next = word[i + 1]
        if prev is not None:
            if curr.isupper() and prev and prev.islower():
                words.append(word[start:i])
                start = i
            if curr.isdigit() and prev.isalpha():
                words.append(word[start:i])
                start = i
            if curr.isalpha() and prev.isdigit():
                words.append(word[start:i])
                start = i
            if next is not None:
                if curr.isupper() and next.islower():
                    words.append(word[start:i])
                    start = i
    words.append(word[start:])

    words = [s.lower() for w in words for substr in w.split('_') for s in substr.split('-') if s]

    return NameCase(
        camel=''.join([words[0]] + [w.capitalize() for w in words[1:]]),
        kebab='-'.join(words),
        pascal=''.join(w.capitalize() for w in words),
        spaced=' '.join(words),
        snake='_'.join(words),
        upper='_'.join(words).upper()
    )