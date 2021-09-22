from time import time

HALF_HOUR: int = 1800
SALARIED_ROLE_ID: int = 888527962935296091
PDG_ROLE_ID: int = 888527789794422784


def word_capitalize(word: str) -> str:
    """Capitalize the first letter of every word within a sentence."""
    return ' '.join(map(str.capitalize, word.split()))


def get_int(string):
    return int(''.join(ch for ch in string if ch.isdigit()))


def get_last_half_hour():
    current_sec = time()
    return int(current_sec - (current_sec % HALF_HOUR))
