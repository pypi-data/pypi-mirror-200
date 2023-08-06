import importlib as _importlib
import re as _re
from os import environ as _env
from os import path as _path
from os import scandir as _scandir
from sys import modules as _modules

from ..abc import Building as _Building
from ..tools.type import underscore_to_camelcase as _2camelcase

infobox = {}


def _import_terminals(start_dir, package_name):

    with _scandir(start_dir) as entries:
        for entry in entries:

            if entry.is_dir() and entry.name.startswith('_') and _path.isfile(_path.join(entry.path, '__init__.py')):

                subpackage_name = f"{package_name}.{entry.name}"
                subpackage_path = _path.join(entry.path, '__init__.py')
                spec = _importlib.util.spec_from_file_location(subpackage_name, subpackage_path)  # type: ignore
                subpackage = _importlib.util.module_from_spec(spec)  # type: ignore

                _modules[subpackage_name] = subpackage  # Add the subpackage to sys.modules
                # pylint: disable=line-too-long
                setattr(_modules[__name__], entry.name, subpackage)  # Add the subpackage to the omnicloud.airport.terminals namespace

                subpackage.__package__ = subpackage_name
                spec.loader.exec_module(subpackage)

                terminal = getattr(subpackage, 'Terminal')
                if not terminal or not issubclass(terminal, _Building):
                    raise RuntimeError(f"Terminal not found in {subpackage_name}.")

                terminal_name = _2camelcase(entry.name)

                setattr(_modules[__name__], terminal_name, terminal)
                infobox[terminal_name] = {'gates': {}}
                infobox[terminal_name]['description'] = str(terminal.__doc__) \
                    .strip() \
                    .split('\n', 1)[0][:125] \
                    .strip()


_import_terminals(_path.dirname(__file__), __name__)

if _env.get('OMNICLOUD_AIRPORT_DEVPATH', '') != '' and _path.isdir(_env['OMNICLOUD_AIRPORT_DEVPATH']):

    _workdir = _path.join(_env['OMNICLOUD_AIRPORT_DEVPATH'], 'omnicloud/airport/terminals')
    _import_terminals(_workdir, __name__)
