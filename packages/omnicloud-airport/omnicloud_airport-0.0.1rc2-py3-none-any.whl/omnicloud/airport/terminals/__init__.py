from ..abc import Building as _Building
from ..tools.pkg import import_subpackages_attributes as _import_terminals


# Import all terminals with aliases without the _Terminal prefix
for _terminal_name, _terminal_obj in _import_terminals(__name__, _Building, '_Terminal'):

    globals()[_terminal_name] = _terminal_obj
