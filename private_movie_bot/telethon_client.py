import os
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

load_dotenv()


def _get_api_id() -> int:
    val = os.getenv("TELEGRAM_API_ID", "0")
    try:
        return int(val)
    except ValueError:
        return 0


API_ID = _get_api_id()
API_HASH = os.getenv("TELEGRAM_API_HASH", "")
SESSION_NAME = "movie_bot_session"
client: TelegramClient | None = None


def init_telethon():
    """Start the Telethon client. Call this before using search_in_channels."""
    global client
    if client is None:
        if not API_ID or not API_HASH:
            raise RuntimeError(
                "TELEGRAM_API_ID and TELEGRAM_API_HASH must be set in .env"
            )
        client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    if not client.is_connected():
        client.start()
        print("Telethon client started.")


async def search_in_channels(query: str, channels: list[str], limit: int = 20):
    """
    Search each channel for messages containing the query.
    Returns a list of (entity, message) pairs.
    """
    if client is None:
        raise RuntimeError("Telethon client not initialized. Call init_telethon() first.")
    
    results = []
    for channel in channels:
        try:
            entity = await client.get_entity(channel)
            async for message in client.iter_messages(entity, search=query, limit=limit):
                if message.text or message.caption:
                    results.append((entity, message))
        except Exception as e:
            print(f"Error searching {channel}: {e}")
    return results
