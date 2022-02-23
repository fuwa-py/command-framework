from __future__ import annotations

import inspect
from typing import (
    TYPE_CHECKING,
    get_type_hints,
    Literal
)

from .option import ApplicationCommandOption

if TYPE_CHECKING:
    from fuwa.fhttp.client import HTTPClient
    
    from .models import InteractionInfo
    from .option import FilledOptions


class ApplicationCommand:    
    async def predicate(
        self,
        interaction_info: InteractionInfo,
        http: HTTPClient,
        options: FilledOptions
    ):
        return True
    
    async def callback(
        self,
        interaction_info: InteractionInfo,
        http: HTTPClient,
        options: FilledOptions
    ):
        raise NotImplementedError

    def _try_match_against_data(self, event_data: dict):
        raise NotImplementedError

    def render_options(self):
        # This method is called when loading commands
        # This means the _options value isn't filled till runtime

        option_annotations = get_type_hints(self.__class__)

        for attr_name, value in inspect.getmembers(self):
            if isinstance(value, ApplicationCommandOption):
                
                # check if an annotation exists for this option
                # if it exists, only process it if its a Literal annotation

                if attr_name in option_annotations:
                    # Okay, we know its annotated, is it Literal?
                    annotation = option_annotations[attr_name]
                    origin = getattr(annotation, "__origin__", None)

                    if origin is Literal:
                        choices = annotation.__args__
                        for choice in choices:
                            choice_payload = {
                                "name": choice,
                                "value": choice
                            }
                            value.choices.append(choice_payload)

                self._options.append(value)

    def get_payload(self):
        raise NotImplementedError