from __future__ import annotations

import inspect
from typing import (
    List,
    TYPE_CHECKING,
    Optional
)

from .types import ApplicationCommandType
from .option import ApplicationCommandOption
from .abc import ApplicationCommand


class SlashCommand(ApplicationCommand):
    def __init_subclass__(
        cls,
        *,
        name: str,
        description: str,
        guild_id: Optional[int] = None
    ):
        name = name.strip()
        description = description.strip()

        cls.name = name
        cls.description = description
        cls.guild_id = guild_id
        
        cls._type = ApplicationCommandType.CHAT_INPUT # 'slash' commands
        cls._options: List[ApplicationCommandOption] = []

    def get_payload(self):
        options = []

        for option in self._options:
            option_payload = option.get_payload()
            options.append(option_payload)

        payload = {
            "name": self.name,
            "description": self.description,
            "type": self._type,
            "options": options
        }

        return payload
    
    def _try_match_against_data(self, event_data: dict):
        interaction_data = event_data["data"]
        name = interaction_data["name"]

        if name == self.name:
            return True

class UserCommand(ApplicationCommand):
    
    def __init_subclass__(
        cls,
        *,
        name: str,
        guild_id: Optional[int] = None
    ):
        cls.name = name
        cls.guild_id = guild_id

        cls._type = ApplicationCommandType.USER # 'user' commands
        cls._options: List[ApplicationCommandOption] = []

    def _try_match_against_data(self, event_data: dict):
        interaction_data = event_data["data"]
        name = interaction_data["name"]

        if name == self.name:
            return True

    def get_payload(self):
        options = []

        for option in self._options:
            option_payload = option.get_payload()
            options.append(option_payload)

        payload = {
            "name": self.name,
            "type": self._type,
            "options": options
        }

        return payload

class MessageCommand(ApplicationCommand):

    def __init_subclass__(
        cls,
        *,
        name: str,
        guild_id: Optional[int] = None
    ):
        cls.name = name
        cls.guild_id = guild_id

        cls._type = ApplicationCommandType.MESSAGE
        cls._options: List[ApplicationCommandOption] = []

    def _try_match_against_data(self, event_data: dict):
        interaction_data = event_data["data"]
        name = interaction_data["name"]

        if name == self.name:
            return True

    def get_payload(self):
        options = []

        for option in self._options:
            option_payload = option.get_payload()
            options.append(option_payload)

        payload = {
            "name": self.name,
            "type": self._type,
            "options": options
        }

        return payload