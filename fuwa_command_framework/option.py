from inspect import getattr_static
from typing import (
    Union,
    List,
    Optional
)

from .types import ApplicationCommandOptionType


class ApplicationCommandOption:
    def __init__(
        self,
        name: Union[str, List[str]],
        /,
        description: Optional[str] = None,
        required: bool = False,
        option_type: int = ApplicationCommandOptionType.STRING
    ):
        self.name = name

        self.required = required
        self.description = description
        self.option_type = option_type

        self.choices: List[str] = []

    def get_payload(self):
        option_payload = {
            "name": self.name,
            "description": self.description,
            "type": self.option_type,
            "required": self.required,
            "choices": self.choices
        }
        return option_payload

    def __repr__(self) -> str:
        r = "<ApplicationCommandOption name={!r} description={!r} type={!r}>"
        return r.format(
            self.name,
            self.description,
            self.option_type
        )


Option = ApplicationCommandOption # just for a shorter way of referencing the class

class FilledOptions(dict):
    def __getattribute__(self, __name: str):
        if __name == "_populate_maps":
            return getattr_static(self, "_populate_maps")
        
        try:
            v = super().__getitem__(__name)
        except KeyError:
            return None
        else:
            return v

    def _populate_maps(self, data):
        interaction_data = data["data"]
        options = interaction_data.get("options")

        if options:
            for opt in options:
                name = opt["name"]
                value = opt["value"]

                super().__setitem__(name, value)