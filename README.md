# Fuwa Command Framework

The command framework for the fuwa eco-system. This supports all 3 types of API commands, `Slash Commands`, `Message Commands`, `User Commands`.
Currently, the framework is in its development stages, however, I try to release "stable" changes to the repo, so you can still use it by installing it via `git`.


## Examples

```py
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from fuwa.gateway.intents import IntentsFlags
from fuwa.commands.framework import CommandFramework
from fuwa.commands.command import SlashCommand, UserCommand, MessageCommand
from fuwa.commands.option import Option
from fuwa.commands.types import ApplicationCommandOptionType as OptType
from fuwa.commands.types import InteractionCallbackType

if TYPE_CHECKING:
    from fuwa.fhttp.client import HTTPClient
    from fuwa.commands.option import FilledOptions
    from fuwa.commands.models import InteractionInfo


logging.basicConfig(level=logging.DEBUG)

intents = IntentsFlags(
    guilds=True,
    guild_messages=True
)

framework = CommandFramework(
    bot_token="bot token",
    intents=intents
)

@framework.application_command()
class MyCommand(SlashCommand, name="poggers", description="hello pog", guild_id=00000000):
    option_1 = Option("hello_world", description="hello world", option_type=OptType.BOOLEAN)

    async def predicate(
        self,
        info: InteractionInfo,
        http: HTTPClient,
        options: FilledOptions
    ):
        # you can do some additional checks, and return whether
        # to process this command interaction or not.

        # You MUST return a truthy/falsey value (boolean)
        return True # return True to allow for the command callback
        # to be run

    async def callback(
        self,
        info: InteractionInfo,
        http: HTTPClient,
        options: FilledOptions
    ):
        await http.create_interaction_response(
            InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE,
            info.id,
            info.token,
            data={"content": f"hello_word option value: {options.hello_world}"}
        )

framework.run() # using this method allows you to have peace of mind that the event loop is handled safely
```

~~You may be asking, why does the command framework not use the `fuwa.xyz` namespace. This is due to some quirks while development where some shadowing issues would occur. This may stay like this in the future, or it may be changed.~~
