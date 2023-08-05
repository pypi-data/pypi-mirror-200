
from ...abc import Gate as _Gate
from ...tools.pkg import import_subpackages_attributes as _import_gates
from .local import LocalJSON

from .terminal import _TerminalDict


# Import all terminals with aliases without the _Terminal prefix
for _gate_name, _gate_obj in _import_gates(__name__, _Gate, '_Gate'):

    globals()[_gate_name] = _gate_obj
