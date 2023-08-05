import json as _json
from ...tools.dict import enrich_dict, type_converter

from .terminal import _TerminalDict

__all__ = ['LocalJSON']


def _get_open_kwargs(options: dict, mode: str) -> dict:

    open_params = ['buffering', "errors", "newline", "closefd", "opener"]

    open_kwargs = {}  # it is important because the open() function doesn't contains **kwargs
    open_kwargs = enrich_dict(open_kwargs, options, "mode", mode)
    open_kwargs = enrich_dict(open_kwargs, options, "encoding", "utf-8")
    for k in open_params:
        open_kwargs = enrich_dict(open_kwargs, options, k)

    open_kwargs = type_converter(open_kwargs, "buffering", int, "open_kwargs")
    open_kwargs = type_converter(open_kwargs, "closefd", bool, "open_kwargs")

    return open_kwargs


def _get_json_kwargs(options: dict) -> dict:
    json_params = [
        'skipkeys', 'ensure_ascii', 'check_circular', 'allow_nan', 'indent', 'separators', 'default'
    ]
    json_kwargs = {}
    for k in json_params:
        json_kwargs = enrich_dict(json_kwargs, options, k)

    json_kwargs = type_converter(json_kwargs, "skipkeys", bool, "json_kwargs")
    json_kwargs = type_converter(json_kwargs, "ensure_ascii", bool, "json_kwargs")
    json_kwargs = type_converter(json_kwargs, "check_circular", bool, "json_kwargs")
    json_kwargs = type_converter(json_kwargs, "allow_nan", bool, "json_kwargs")
    json_kwargs = type_converter(json_kwargs, "indent", int, "json_kwargs")
    json_kwargs = type_converter(json_kwargs, "separators", tuple, "json_kwargs")

    return json_kwargs


class LocalJSON(_TerminalDict.Gate):

    @classmethod
    def arriving(cls, place: str, **options):

        open_kwargs = _get_open_kwargs(options, "r")
        json_kwargs = _get_json_kwargs(options)

        with open(place, **open_kwargs) as json_file:  # pylint: disable=unspecified-encoding
            return _json.load(json_file, **json_kwargs)

    @classmethod
    def departure(cls, parcel, place: str, **options):

        open_kwargs = _get_open_kwargs(options, "w")
        json_kwargs = _get_json_kwargs(options)

        with open(place, **open_kwargs) as json_file:  # pylint: disable=unspecified-encoding
            _json.dump(parcel, json_file, **json_kwargs)
