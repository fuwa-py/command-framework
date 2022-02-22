from __future__ import annotations

import inspect
from typing import TYPE_CHECKING

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

        for _, value in inspect.getmembers(self):
            if isinstance(value, ApplicationCommandOption):
                self._options.append(value)

    def get_payload(self):
        raise NotImplementedError