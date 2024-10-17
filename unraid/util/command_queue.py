import asyncio
from typing import Callable, Any, Awaitable

class CommandQueue:
    """
    A queue for managing concurrent command execution.

    This class limits the number of concurrent tasks and provides methods for
    executing tasks and running multiple tasks concurrently.
    """

    def __init__(self, max_concurrent: int = 6):
        """
        Initialize the CommandQueue.

        Args:
            max_concurrent: The maximum number of tasks that can run concurrently.
        """
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.tasks = set()

    async def do_task(self, task: Callable[..., Awaitable[Any]], *args, **kwargs) -> Any:
        """
        Execute a task while respecting the concurrency limit.

        Args:
            task: The async function to execute.
            *args: Positional arguments for the task.
            **kwargs: Keyword arguments for the task.

        Returns:
            The result of the task execution.
        """
        async with self.semaphore:
            return await task(*args, **kwargs)

    async def run(self, *tasks: Callable[..., Awaitable[Any]]) -> list[Any]:
        """
        Run multiple tasks concurrently, respecting the concurrency limit.

        Args:
            *tasks: The async functions to execute.

        Returns:
            A list of results from all task executions.
        """
        async def wrapped_task(task):
            try:
                return await self.do_task(task)
            finally:
                self.tasks.remove(task)

        self.tasks.update(tasks)
        return await asyncio.gather(*(wrapped_task(task) for task in tasks))