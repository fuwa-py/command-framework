import traceback


async def print_exc_coro(coro):
    try:
        await coro
    except Exception:
        traceback.print_exc()
