import asyncio
from subprocess import SubprocessError
from typing import Awaitable, Callable, TYPE_CHECKING


if TYPE_CHECKING:
    from .task import Task


class Action:
    async def execute(self, task: "Task") -> None:
        raise NotImplementedError


class FunctionAction(Action):
    def __init__(self, func: Callable, *args, **kwargs) -> None:
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    async def execute(self, task: "Task") -> None:
        result = self.func(task, *self.args, **self.kwargs)
        if isinstance(result, Awaitable):
            await result


class SubprocessAction(Action):
    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs

    async def execute(self, task: "Task") -> None:
        process = await asyncio.create_subprocess_exec(*self.args, **self.kwargs)
        status = await process.wait()
        if status:
            raise SubprocessError(f"executing {self.args} returned status code {status}")


class ShellAction(Action):
    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs

    async def execute(self, task: "Task") -> None:
        process = await asyncio.create_subprocess_shell(*self.args, **self.kwargs)
        status = await process.wait()
        if status:
            raise SubprocessError(f"executing {self.args} returned status code {status}")


class CompositeAction(Action):
    def __init__(self, *actions: Action) -> None:
        self.actions = actions

    async def execute(self, task: "Task") -> None:
        for action in self.actions:
            await action.execute(task)
