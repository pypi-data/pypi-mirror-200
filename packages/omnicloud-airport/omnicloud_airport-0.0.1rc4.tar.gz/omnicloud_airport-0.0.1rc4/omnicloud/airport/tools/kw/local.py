from ...tools.dict import enrich as _enrich
from ...tools.dict import item_converter as _converter

__all__ = [
    'kw4open'
]


def kw4open(options: dict, mode: str, name4log: str | None = None) -> dict:

    if not name4log:
        name4log = kw4open.__name__

    open_params = ['buffering', 'errors', 'newline', 'closefd', 'opener', 'encoding']

    kwargs = {}  # it is important because the open() function doesn't contains **kwargs

    # set default values; low priority
    kwargs = _enrich(kwargs, options, "encoding", "utf-8")

    for k in open_params:
        kwargs = _enrich(kwargs, options, k)

    kwargs = _enrich(kwargs, options, "mode", mode)  # function parameter has higher priority

    kwargs = _converter(kwargs, "buffering", int, name4log)
    kwargs = _converter(kwargs, "closefd", bool, name4log)

    return kwargs
