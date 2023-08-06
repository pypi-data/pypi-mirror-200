import pytest
from bot_engine_client import BotEngineClient
from bot_engine_client.models import Bot


@pytest.fixture
def bot_engine_client():
    return BotEngineClient()


@pytest.mark.asyncio
async def test_ping_async(bot_engine_client: BotEngineClient):
    result = await bot_engine_client.ping_async()
    assert isinstance(result, int)

@pytest.mark.asyncio
async def test_get_bots_async(bot_engine_client: BotEngineClient):
    bots = await bot_engine_client.get_bots_async()
    assert isinstance(bots, list)
    assert all(isinstance(bot, Bot) for bot in bots)