"""Utilities for pipen_cli_config to work on pipelines"""
from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Type

if TYPE_CHECKING:
    from pipen import Proc

MARK_CONTAINER = "__pipen_cli_config__"


def from_pipen_cli_config() -> bool:
    """Check if the process is called from pipen_cli_config

    Returns:
        True if the process is called from pipen_cli_config
    """
    import sys
    return sys.argv[0] == "from-pipen-cli-config"


def get_mark(proc: Type[Proc], key: str):
    """Get the marked attribute of the process

    Args:
        proc: The process
        key: The attribute name

    Returns:
        The attribute value
    """
    return getattr(proc, MARK_CONTAINER, {}).get(key)


def mark(**kwargs) -> Callable[[Type[Proc]], Type[Proc]]:
    """Mark the process with some attributes to be used by pipen_cli_config

    Args:
        kwargs: The attributes to be marked

    Marks:
        no_input: Do not ask for input for the process even it is a
            start process.
            The cases could be that the input has been provided somewhere else
            For example, options from a process group, or hard-coded in the
            pipeline
        hidden: Do not show the process in the UI

    Returns:
        A decorator for the process with the attributes marked
    """
    def decorator(proc: Type[Proc]):
        if not hasattr(proc, MARK_CONTAINER):
            setattr(proc, MARK_CONTAINER, {})
        config = getattr(proc, MARK_CONTAINER)
        config.update(kwargs)
        return proc

    return decorator
