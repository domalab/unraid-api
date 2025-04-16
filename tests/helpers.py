"""Helper functions for tests."""
import asyncio
from unittest.mock import AsyncMock, MagicMock


def async_return(value):
    """Create a coroutine that returns a value."""
    async def _async_return():
        return value
    return _async_return()


class AsyncMethodMock(MagicMock):
    """MagicMock that properly handles async methods."""
    async def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)


def patch_async_method(target, return_value=None):
    """Create a properly awaitable mock for an async method."""
    mock = AsyncMock()
    if return_value is not None:
        mock.return_value = return_value
    return mock


def create_awaitable_mock(return_value=None):
    """Create a mock that can be awaited and returns the specified value."""
    mock = AsyncMock()
    mock.__await__ = lambda: asyncio.sleep(0).__await__()
    if return_value is not None:
        mock.return_value = return_value
    return mock
