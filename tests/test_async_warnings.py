"""Tests to fix the async warnings."""
import asyncio
import pytest


@pytest.mark.asyncio
async def test_asyncio_warnings():
    """Test to fix the asyncio warnings."""
    # This test doesn't do anything, but it ensures that the asyncio event loop
    # is properly set up and torn down, which fixes the warnings.
    await asyncio.sleep(0)
