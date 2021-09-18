def word_capitalize(word: str) -> str:
    """Capitalize the first letter of every word within a sentence."""
    return ' '.join(map(str.capitalize, word.split()))
