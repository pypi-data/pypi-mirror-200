import json
from os import path, makedirs
from ....tools.files import kw4open
from ....tools.json import kw4json

from .. import Terminal

__all__ = ['LocalJSON']


class LocalJSON(Terminal.Gate):

    @classmethod
    def arriving(cls, place: str, **options):

        open_kwargs = kw4open(options, "r", name4log=cls.__name__)
        json_kwargs = kw4json(options, name4log=cls.__name__)

        with open(place, **open_kwargs) as json_file:  # pylint: disable=unspecified-encoding
            return json.load(json_file, **json_kwargs)

    @classmethod
    def departure(cls, parcel, place: str, **options):

        open_kwargs = kw4open(options, "w", name4log=cls.__name__)
        json_kwargs = kw4json(options, name4log=cls.__name__)

        if not path.exists(path.dirname(place)):
            makedirs(path.dirname(place))

        with open(place, **open_kwargs) as json_file:  # pylint: disable=unspecified-encoding
            json.dump(parcel, json_file, **json_kwargs)
