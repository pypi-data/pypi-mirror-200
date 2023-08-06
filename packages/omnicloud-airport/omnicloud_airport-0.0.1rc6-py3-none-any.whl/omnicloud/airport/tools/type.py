
__all__ = [
    'convert_to_bool',
    'underscore_to_camelcase'
]


def convert_to_bool(string):
    return bool(int(string)) if string.isdigit() else string.lower() in ['true', 'yes', 'on', '1']


def underscore_to_camelcase(text):
    words = text.split('_')
    # Capitalize the first letter of each word except the first word
    camelcase_words = [word.capitalize() if i != 0 else word for i, word in enumerate(words)]
    # Join the words into a single string
    camelcase_text = ''.join(camelcase_words)
    return camelcase_text
