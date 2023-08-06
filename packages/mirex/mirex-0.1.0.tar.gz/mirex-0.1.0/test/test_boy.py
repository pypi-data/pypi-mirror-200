import asyncio
import os

import disnake
from disnake.ext import commands
from redis import asyncio as aioredis

from mirex import Mirex


async def main():
    bot = commands.InteractionBot(intents=disnake.Intents.all())

    redis = aioredis.from_url("redis://127.0.0.1:6379")
    mirex = Mirex(
        namespace=disnake,
        redis_instance=redis,
        connection_state=bot._connection,
    )
    mirex.inject_hooks()
    asyncio.create_task(mirex.consume_queue())
    asyncio.create_task(mirex.consume_eviction())

    @bot.event
    async def on_ready():
        g = await bot.fetch_guild(808030843078836254)
        mirex.add_to_cache(g)
        guild: disnake.Guild = await mirex.aget_guild(808030843078836254)
        assert guild == g
        print("Done")

    await bot.start(os.environ["TOKEN"])


asyncio.run(main())
