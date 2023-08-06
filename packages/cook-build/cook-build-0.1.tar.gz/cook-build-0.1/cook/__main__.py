import argparse
import importlib.util
import os
from pathlib import Path
import re
import sqlite3
import sys
from typing import Iterable, List, Optional
from .contexts import create_target_directories, normalize_action, normalize_dependencies
from .controller import Controller, QUERIES
from .manager import Manager
from .task import Task
from .util import FailedTaskError


def discover_tasks(manager: Manager, patterns: Iterable[re.Pattern]) -> List[Task]:
    """
    Discover tasks based on regular expressions.
    """
    if not patterns:
        return list(manager.tasks.values())
    return [task for name, task in manager.tasks.items() if
            any(pattern.match(name) for pattern in patterns)]


class Command:
    """
    Abstract base class for commands.
    """
    NAME: Optional[str] = None

    def __init__(self) -> None:
        pass

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        raise NotImplementedError

    def execute(self, controller: Controller, args: argparse.Namespace) -> None:
        raise NotImplementedError


class ExecArgs(argparse.Namespace):
    tasks: Iterable[re.Pattern]


class ExecCommand(Command):
    """
    Execute one or more tasks.
    """
    NAME = "exec"

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("tasks", nargs="+", type=re.compile,
                            help="task or tasks to execute as regular expressions")

    def execute(self, controller: Controller, args: ExecArgs) -> Optional[int]:
        tasks = discover_tasks(controller.manager, args.tasks)
        try:
            controller.execute_sync(*tasks)
        except FailedTaskError as ex:
            print(ex)
            return 1


class LsArgs(argparse.Namespace):
    tasks: Iterable[re.Pattern]


class LsCommand(Command):
    """
    List tasks.
    """
    NAME = "ls"

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("tasks", nargs="*", type=re.compile,
                            help="task or tasks to execute as regular expressions")

    def execute(self, controller: Controller, args: LsArgs) -> None:
        tasks = discover_tasks(controller.manager, args.tasks)
        if tasks:
            print("\n".join(map(str, tasks)))
        else:
            print(f"found no tasks matching pattern {args.tasks or '.*'}")


class InfoArgs(argparse.Namespace):
    pass


class InfoCommand(Command):
    """
    Display information about one or more tasks.
    """
    NAME = "info"

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("tasks", nargs="+", help="task or tasks to execute")

    def execute(self, controller: Controller, args: argparse.Namespace) -> None:
        print(self)


def __main__(cli_args: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser("cook")
    parser.add_argument("--recipe", help="file containing declarative recipe for tasks",
                        default="recipe.py", type=Path)
    parser.add_argument("--module", "-m", help="module containing declarative recipe for tasks")
    parser.add_argument("--db", help="database for keeping track of assets", default=".cook")
    subparsers = parser.add_subparsers()
    subparsers.required = True

    for command_cls in [ExecCommand, LsCommand, InfoCommand]:
        subparser = subparsers.add_parser(command_cls.NAME, help=command_cls.__doc__)
        command = command_cls()
        command.configure_parser(subparser)
        subparser.set_defaults(command=command)

    args = parser.parse_args(cli_args)

    with Manager() as manager:
        manager.contexts.extend([
            create_target_directories(),
            normalize_action(),
            normalize_dependencies(),
        ])
        if args.module:
            # Temporarily add the current working directory to the path.
            try:
                sys.path.append(os.getcwd())
                importlib.import_module(args.module)
            finally:
                sys.path.pop()
        elif args.recipe.is_file():
            # Parse the recipe.
            spec = importlib.util.spec_from_file_location("recipe", args.recipe)
            recipe = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(recipe)
        else:  # pragma: no cover
            raise ValueError("recipe file or module must be specified; default recipe.py not found")

    with sqlite3.connect(args.db) as connection:
        connection.execute(QUERIES["schema"])
        controller = Controller(manager, connection)
        command: Command = args.command
        exit_code = command.execute(controller, args)
        if exit_code:
            sys.exit(exit_code)


if __name__ == "__main__":
    __main__()
