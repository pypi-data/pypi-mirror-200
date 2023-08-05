import inspect
from types import ModuleType
from argparse import ArgumentParser, Namespace
from typing import List, Type, TypeVar
from ramjam.cli import Command

CommandModulesType = TypeVar(name="CommandModulesType", bound="CommandModules")


def get_commands(module: ModuleType) -> List[Type[Command]]:
    commands = []
    for i, _class in inspect.getmembers(module, inspect.isclass):
        if _class != Command:
            if issubclass(_class, Command):
                commands.append(_class)
    return commands


def parse_args(*modules: ModuleType) -> Namespace:

    parser = ArgumentParser()
    sub_parser = parser.add_subparsers(dest="command")
    sub_parser.required = True

    for module in modules:
        for command in get_commands(module):
            p = sub_parser.add_parser(command.method(), help=command.help)
            for args, kwargs in command.args.items():
                p.add_argument(*args, **kwargs)
            p.set_defaults(command=command)
    return parser.parse_args()
