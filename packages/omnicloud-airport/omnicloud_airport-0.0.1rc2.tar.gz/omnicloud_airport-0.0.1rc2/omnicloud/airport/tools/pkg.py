import importlib as _importlib
import pkgutil as _pkgutil
from os import path as _path
from os import environ as _env
from warnings import warn as _warn


__all__ = [
    'import_all_modules',
    'abstract_checker',
    'import_subpackages_attributes'
]


def import_all_modules(package_name: str, package_path: str):

    for module_info in _pkgutil.iter_modules([package_path]):

        module_name = f"{package_name}.{module_info.name}"
        _importlib.import_module(module_name)
        module_path = _path.join(package_path, module_info.name)

        if _path.isdir(module_path):
            continue


def abstract_checker(cls, attr_name: str) -> None:
    attr = getattr(cls, attr_name)
    if hasattr(attr, '__isabstractmethod__') and attr.__isabstractmethod__:
        raise NotImplementedError(
            f'The attribute "{cls.__name__}.{attr_name}" is required. Please read documentation of ZZZ!!'
        )


def import_subpackages_attributes(package_name: str, inherited: type, prefix: str):
    """
    Find and import {prefix}<Name> attributes from subpackages starting with "_" in the current package.

    Returns:
        list: a list of tuples (terminal_name, terminal_object) for each {prefix}<Name> attribute found.

    Warnings:
        UserWarning: if there is not exactly one {prefix}<Name> attribute in any subpackage.
    """

    package = _importlib.import_module(package_name)
    terminals = []
    names_list = []

    def looking_for_subpackages(package_path, package_name):

        for _, name, is_pkg in _pkgutil.walk_packages(package_path, f"{package_name}."):

            if is_pkg and name.startswith(f"{package_name}._"):
                pkg = _importlib.import_module(name)

                terminal_names = [
                    attr_name[len(f'{prefix}'):]
                    for attr_name in dir(pkg)
                    if attr_name.startswith(f'{prefix}')
                ]

                if len(terminal_names) != 1:
                    _warn(f"Expected 1 {prefix}* attribute in {name}, found {len(terminal_names)}")
                    continue

                terminal_name = terminal_names[0]
                terminal = getattr(pkg, f'{prefix}{terminal_name}')

                if not issubclass(terminal, inherited):
                    raise TypeError(f"Expected {inherited.__name__} subclass in {name}.")

                terminals.append((terminal_name, terminal))
                names_list.append(terminal_name)

                if len(terminals) > len(set(names_list)):
                    raise RuntimeError(f"Duplicate terminal name {terminal_name} in {name}")

    looking_for_subpackages(package.__path__, package_name)
    if 'OMNICLOUD_AIRPORT_DEVPATH' in _env and _env['OMNICLOUD_AIRPORT_DEVPATH'] != '':
        looking_for_subpackages([_env['OMNICLOUD_AIRPORT_DEVPATH']], package_name)

    return terminals
