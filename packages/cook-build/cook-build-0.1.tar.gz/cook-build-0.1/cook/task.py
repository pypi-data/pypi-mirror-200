from __future__ import annotations
from pathlib import Path
from typing import List, Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from .util import PathOrStr
    from .actions import Action


class Task:
    """
    Task to be executed.

    Args:
        name: Name of the task.
        dependencies: Files that the task depends on.
        targets: Files that the task will generate.
        action: Action to execute when the task is run.
        task_dependencies: Tasks that should be executed prior to this task.
    """
    def __init__(
            self,
            name: str,
            *,
            dependencies: Optional[List[PathOrStr]] = None,
            targets: Optional[List[PathOrStr]] = None,
            action: Optional[Action] = None,
            task_dependencies: Optional[List[Task]] = None,
            ) -> None:
        self.name = name
        self.dependencies = dependencies or []
        self.targets = [Path(path) for path in (targets or [])]
        self.action = action
        self.task_dependencies = task_dependencies or []

    async def execute(self) -> None:
        if self.action:
            await self.action.execute(self)

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return f"{self.name}({len(self.dependencies)} -> {len(self.targets)})"
