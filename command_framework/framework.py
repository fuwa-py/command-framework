from __future__ import annotations

import asyncio
from typing import (
    TYPE_CHECKING,
    List,
    Optional
)

import aiohttp
from fuwa.fhttp.client import Route
from fuwa.fhttp.client import HTTPClient
from fuwa.gateway.connection import GatewayConnection

from .option import FilledOptions
from .models import InteractionInfo
from .utils import print_exc_coro

if TYPE_CHECKING:
    from fuwa.gateway.intents import IntentsFlags
    from .abc import ApplicationCommand


class CommandFramework:
    def __init__(
        self,
        *,
        gateway: Optional[GatewayConnection] = None,
        http: Optional[HTTPClient] = None,
        bot_token: Optional[str] = None,
        intents: Optional[IntentsFlags] = None
    ):
        if (gateway is None or http is None) and (bot_token is None or intents is None):
            raise ValueError(
                "If you aren't giving the framework both gateway and http, you must provide a bot token and intents flags"
            )

        gateway = gateway or GatewayConnection(bot_token, intents)
        http = http or HTTPClient(bot_token)
        
        self.gateway = gateway
        self.http = http

        self.commands: List[ApplicationCommand] = []

        self.gateway.add_event_handler(
            "INTERACTION_CREATE",
            self._interaction_listener
        )

        self._stored_session: Optional[aiohttp.ClientSession] = None
        self._finished_reg: bool = False

        self.loop = asyncio.get_event_loop()
    
    def application_command(self):
        def decorator(cls):
            if isinstance(cls, type):
                cls = cls()
                cls.render_options()

            self.commands.append(cls)

        return decorator

    async def _interaction_listener(self, event_data: dict):
        # from pprint import pprint
        # pprint(event_data)
        for command in self.commands:
            if command._try_match_against_data(event_data):
                info = InteractionInfo(event_data)
                options = FilledOptions()
                options._populate_maps(options, event_data)

                self._schedule_command_callback(command, info, self.http, options)

    async def _run_command_callback(
        self,
        command: ApplicationCommand,
        *c_args,
        **c_kwargs
    ):
        callback = command.callback(*c_args, **c_kwargs)
        predicate = command.predicate(*c_args, **c_kwargs)

        async def _run_coro():
            predicate_result = await predicate
            # if our predicate result is True, run our callback function

            if predicate_result is True:
                await callback

        await print_exc_coro(_run_coro()) # handles
        # running our predicate and callback in a try-except block
        # while printing any errors that occur
            
    def _schedule_command_callback(
        self,
        command: ApplicationCommand,
        *c_args,
        **c_kwargs
    ):
        wrapped = self._run_command_callback(command, *c_args, **c_kwargs)
        asyncio.create_task(wrapped, name="luna:command_framework:command-task")

    async def setup(self):
        shared_session = aiohttp.ClientSession()
        self._stored_session = shared_session

        self.gateway.share_session(shared_session)
        self.http.share_session(shared_session)

        await self.http.init()

        gateway_route = Route("GET",  "/gateway/bot")
        data = await self.http.request(gateway_route)

        gateway_url = data["url"]
        version = 9

        try:
            await self.register_commands()
        except Exception as e:
            print(e.data)
            exit(1)

        await self.gateway.open_connection(
            gateway_url,
            version=version
        )

    async def register_commands(self):
        guild_commands = {} # guild_id: List[payloads]
        global_commands = []

        for command in self.commands:
            guild_id = command.guild_id

            if guild_id is None:
                # global command
                payload = command.get_payload()
                global_commands.append(payload)
            else:
                current_guild_commands = guild_commands.get(guild_id, [])
                payload = command.get_payload()
                current_guild_commands.append(payload)

                guild_commands[guild_id] = current_guild_commands

        # First we register global commands
        await self.http.bulk_upsert_application_commands(global_commands)

        # Next register guild specific commands, with a 0.1 second delay
        # between each guild_id, to avoid ratelimits
        for guild_id, payload in guild_commands.items():
            await self.http.bulk_upsert_application_commands(payload, guild_id=guild_id)
            await asyncio.sleep(0.1)

    def run(self):
        self.loop.run_until_complete(self.setup())
        self.loop.run_forever()
