from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    List
)

from .framework import CommandFramework

if TYPE_CHECKING:
    from .abc import ApplicationCommand


class Wheel:

    application_command = CommandFramework.application_command

    def __init__(self):
        self.commands: List[ApplicationCommand] = []