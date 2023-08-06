import importlib as _importlib
from os import environ as _env
from os import path as _path
from os import scandir as _scandir
from sys import modules as _modules


__all__ = [
    'abstract_checker',
    'import_gates'
]


def abstract_checker(cls, attr_name: str) -> None:
    attr = getattr(cls, attr_name)
    if hasattr(attr, '__isabstractmethod__') and attr.__isabstractmethod__:
        raise NotImplementedError(
            f'The attribute "{cls.__name__}.{attr_name}" is required. Please read documentation of ...!!'
        )


def import_gates(file, name, parent: bool = True):

    start_dir = _path.dirname(file) if parent else file

    with _scandir(start_dir) as folder_cont:
        for entry in folder_cont:

            if entry.is_dir() and entry.name.startswith('_') and _path.isfile(_path.join(entry.path, '__init__.py')):

                subpackage_name = f"{name}.{entry.name}"
                subpackage_path = _path.join(entry.path, '__init__.py')
                spec = _importlib.util.spec_from_file_location(subpackage_name, subpackage_path)  # type: ignore
                subpackage = _importlib.util.module_from_spec(spec)  # type: ignore

                _modules[subpackage_name] = subpackage  # Add the subpackage to sys.modules
                setattr(_modules[name], entry.name, subpackage)  # Add the subpackage to the main module's namespace

                subpackage.__package__ = subpackage_name
                spec.loader.exec_module(subpackage)

    if _env.get('OMNICLOUD_AIRPORT_DEVPATH', '') != '' \
            and _path.isdir(_env['OMNICLOUD_AIRPORT_DEVPATH']) \
            and parent \
            and not _env['OMNICLOUD_AIRPORT_DEVPATH'] in file:

        workdir = _path.join(
            _env['OMNICLOUD_AIRPORT_DEVPATH'],
            'omnicloud/airport/terminals',
            start_dir.rsplit('/', 1)[-1]
        )
        if _path.isdir(workdir):
            with _scandir(workdir) as entries:
                for entry in entries:
                    if entry.is_dir() and entry.name.startswith('_') \
                            and _path.isfile(_path.join(entry.path, '__init__.py')):
                        import_gates(workdir, name, False)
