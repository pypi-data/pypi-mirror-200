#  pylint: disable=missing-module-docstring

from .type import convert_to_bool as _convert_to_bool

__all__ = ['enrich', 'item_converter']


def enrich(target: dict, src: dict, key: str, default=None) -> dict:
    '''Enriches a target dictionary with a source dictionary.

    Args:
        target (dict): The target dictionary to be enriched.
        src (dict): The source dictionary to enrich from.
        key (str): The key to be used for enrichment.
        default (optional): The default value if the key is not present in the source dictionary.

    Returns:
        dict: The enriched target dictionary.
    '''

    if key in src:
        target[key] = src[key]

    elif default is not None:
        target[key] = default

    return target


def item_converter(src: dict, key: str, data_type: type, obj: str) -> dict:
    '''Converts the value of a given key in a dictionary to a given type.

    Args:
        src (dict): The source dictionary.
        key (str): The key whose value should be converted.
        data_type (type): The type to which the value should be converted.
        obj (str): The name of the object containing the dictionary.

    Returns:
        dict: The source dictionary with the converted types of values.
    '''

    if key in src:

        try:
            src[key] = _convert_to_bool(src[key]) if data_type == bool else data_type(src[key])

        except Exception as ex:
            raise ValueError(
                # pylint: disable=line-too-long
                f'The value "{src[key]}" of the "{key}" parameter in the "{obj}" object is not a valid {data_type.__name__}'
            ) from ex

    return src
