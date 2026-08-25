"""
Axiom

The authoritative world-intelligence layer of Aevum.

Axiom maintains canonical reality, enforces world rules,
resolves character intentions, and produces world events.
"""

from .events import create_world_event


__all__ = [
    "create_world_event",
]
