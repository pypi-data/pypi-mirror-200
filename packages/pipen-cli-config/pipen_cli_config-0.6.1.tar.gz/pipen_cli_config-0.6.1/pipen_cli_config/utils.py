"""Utilities for pipen_cli_config to work on pipelines"""
from __future__ import annotations


def from_pipen_cli_config() -> bool:
    """Check if the process is called from pipen_cli_config

    Returns:
        True if the process is called from pipen_cli_config
    """
    import sys
    return sys.argv[0] == "from-pipen-cli-config"
