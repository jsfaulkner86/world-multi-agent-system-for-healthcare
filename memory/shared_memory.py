"""shared_memory.py — Shared in-memory context layer (Redis-ready)."""

from loguru import logger
from typing import Any, Optional


class SharedMemory:
    """
    In-memory key-value store for sharing context across agents.
    Designed to be swapped for Redis in production.
    """

    def __init__(self):
        self._store: dict[str, Any] = {}
        logger.debug("SharedMemory initialized (in-memory mode)")

    def store(self, key: str, value: Any) -> None:
        """Store a value by key."""
        self._store[key] = value
        logger.debug(f"SharedMemory: stored key='{key}'")

    def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve a value by key."""
        value = self._store.get(key)
        logger.debug(f"SharedMemory: retrieved key='{key}' -> {'found' if value else 'not found'}")
        return value

    def delete(self, key: str) -> None:
        """Delete a key from memory."""
        self._store.pop(key, None)
        logger.debug(f"SharedMemory: deleted key='{key}'")

    def clear(self) -> None:
        """Clear all stored memory."""
        self._store.clear()
        logger.debug("SharedMemory: cleared all keys")

    def keys(self) -> list:
        """List all stored keys."""
        return list(self._store.keys())
