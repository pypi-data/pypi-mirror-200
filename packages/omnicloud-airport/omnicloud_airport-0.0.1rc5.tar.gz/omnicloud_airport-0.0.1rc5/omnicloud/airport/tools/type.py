from .dict import enrich as _enrich
from .dict import item_converter as _converter


__all__ = [
    'convert_to_bool',
    'kw4json',
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


def kw4json(options: dict, name4log: str | None = None) -> dict:

    if not name4log:
        name4log = kw4json.__name__

    json_params = [
        'skipkeys', 'ensure_ascii', 'check_circular', 'allow_nan', 'indent', 'separators', 'default'
    ]

    kwargs = {}
    for k in json_params:
        kwargs = _enrich(kwargs, options, k)

    kwargs = _converter(kwargs, "skipkeys", bool, name4log)
    kwargs = _converter(kwargs, "ensure_ascii", bool, name4log)
    kwargs = _converter(kwargs, "check_circular", bool, name4log)
    kwargs = _converter(kwargs, "allow_nan", bool, name4log)
    kwargs = _converter(kwargs, "indent", int, name4log)
    kwargs = _converter(kwargs, "separators", tuple, name4log)

    return kwargs
