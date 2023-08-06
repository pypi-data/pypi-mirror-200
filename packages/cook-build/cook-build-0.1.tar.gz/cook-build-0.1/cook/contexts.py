from __future__ import annotations
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple, TYPE_CHECKING
from . import actions
from . import manager as manager_
from . import task as task_


if TYPE_CHECKING:
    from .manager import Manager
    from .task import Task


class Context:
    """
    Context that is applied to tasks when they are created.

    Args:
        manager: Manager to which the context is added.
    """
    def __init__(self, manager: Optional["Manager"] = None) -> None:
        self.manager = manager or manager_.Manager.get_instance()

    def __enter__(self) -> Context:
        self.manager.contexts.append(self)
        return self

    def __exit__(self, *_) -> None:
        if not self.manager.contexts:
            raise RuntimeError("exiting failed: no active contexts")
        if self.manager.contexts[-1] is not self:
            raise RuntimeError("exiting failed: unexpected context")
        self.manager.contexts.pop()

    def apply(self, task: "Task") -> "Task":
        """
        Apply the context to a task.

        Args:
            task: Task to modify.
        """
        raise NotImplementedError


class FunctionContext(Context):
    """
    Context wrapping a function.
    """
    def __init__(self, func: Callable, args: Optional[Tuple] = None, kwargs: Optional[Dict] = None,
                 manager: Optional["Manager"] = None) -> None:
        super().__init__(manager)
        self.func = func
        self.args = args or ()
        self.kwargs = kwargs or {}

    def apply(self, task: "Task") -> "Task":
        return self.func(task, *self.args, **self.kwargs)


class create_target_directories(Context):
    """
    Create parent directories for all targets.
    """
    def apply(self, task: "Task") -> Task:
        for target in task.targets:
            Path(target).parent.mkdir(parents=True, exist_ok=True)
        return task


class normalize_action(Context):
    """
    Normalize actions of tasks.

    - If the action is a callable, it will be wrapped in a :class:`actions.FunctionAction`.
    - If the action is a string, it will be executed on the shell.
    - If the action is a list of actions, a composite action will be created.
    - If the action is any other list, it will be executed as a subprocess after converting elements
      to strings.
    """
    def apply(self, task: "Task") -> "Task":
        if isinstance(task.action, Callable):
            task.action = actions.FunctionAction(task.action)
        elif isinstance(task.action, str):
            task.action = actions.ShellAction(task.action)
        elif isinstance(task.action, List):
            if all(isinstance(x, actions.Action) for x in task.action):
                task.action = actions.CompositeAction(*task.action)
            else:
                task.action = actions.SubprocessAction(*list(map(str, task.action)))
        return task


class normalize_dependencies(Context):
    def apply(self, task: "Task") -> "Task":
        # Move task and group dependencies to the task_dependencies if they appear in regular
        # dependencies.
        dependencies = []
        task_dependencies = task.task_dependencies
        for dependency in task.dependencies:
            if isinstance(dependency, (task_.Task, group)):
                task_dependencies.append(dependency)
            else:
                dependencies.append(dependency)
        task.dependencies = [Path(x) for x in dependencies]

        # Unpack group dependencies and look up tasks by name.
        task_dependencies = []
        for other in task.task_dependencies:
            if isinstance(other, group):
                other = other.task
            elif isinstance(other, str):
                other = self.manager.tasks[other]
            task_dependencies.append(other)
        task.task_dependencies = task_dependencies

        return task


class group(Context):
    """
    Context for grouping tasks.
    """
    def __init__(self, name: str, manager: Optional["Manager"] = None) -> None:
        super().__init__(manager)
        self.name = name
        self.task = self.manager.create_task(self.name)

    def apply(self, task: "Task") -> "Task":
        self.task.task_dependencies.append(task)
        return task
