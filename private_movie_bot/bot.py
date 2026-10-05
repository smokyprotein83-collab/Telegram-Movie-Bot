import os
import re
import asyncio
import shlex
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.constants import ParseMode

import tmdb_client
import telethon_client
import filename_parser

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
ALLOWED_USER_IDS = [
    uid.strip() for uid in os.getenv("ALLOWED_USER_IDS", "").split(",") if uid.strip()
]
SEARCH_CHANNELS = [
    ch.strip() for ch in os.getenv("SEARCH_CHANNELS", "").split(",") if ch.strip()
]


def is_allowed(user_id: int) -> bool:
    if not ALLOWED_USER_IDS:
        return True
    return str(user_id) in ALLOWED_USER_IDS


def get_message_link(entity, message_id: int) -> str:
    if hasattr(entity, "username") and entity.username:
        return f"https://t.me/{entity.username}/{message_id}"
    channel_id = str(entity.id)
    if channel_id.startswith("-100"):
        channel_id = channel_id[4:]
    return f"https://t.me/c/{channel_id}/{message_id}"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update.effective_user.id):
        await update.message.reply_text("You are not authorized to use this bot.")
        return

    help_text = (
        "Welcome to the Private Movie Search Bot!\n\n"
        "Commands:\n"
        "/start - Show this help message\n"
        "/find <title> [lang] [max_res] [max_quality]\n\n"
        "Examples:\n"
        "/find Inception malayalam 1080p web-dl\n"
        '/find "Baahubali 2" tamil 720p bluray\n\n'
        "Supported languages: malayalam, tamil, hindi, english\n"
        "Supported resolutions: 480p, 720p, 1080p, 2160p\n"
        "Supported qualities: CAM, TELESYNC, HDRIP, WEB-DL, BLU-RAY"
    )
    await update.message.reply_text(help_text)


async def find(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update.effective_user.id):
        await update.message.reply_text("You are not authorized to use this bot.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /find <title> [lang] [max_res] [max_quality]")
        return

    try:
        parts = shlex.split(" ".join(context.args))
    except ValueError:
        await update.message.reply_text("Invalid command format.")
        return

    title = parts[0]
    lang = parts[1] if len(parts) > 1 else None
    max_res = parts[2] if len(parts) > 2 else None
    max_quality = parts[3] if len(parts) > 3 else None

    valid_langs = ["malayalam", "tamil", "hindi", "english"]
    if lang and lang.lower() not in valid_langs:
        await update.message.reply_text(
            f"Unsupported language: {lang}. Use: malayalam, tamil, hindi, english"
        )
        return

    await update.message.reply_text(f"Searching for: {title}")

    try:
        results = tmdb_client.search_movies(title, language="en-US")
    except Exception as e:
        await update.message.reply_text(f"TMDB search failed: {e}")
        return

    if not results:
        await update.message.reply_text("No movies found on TMDB.")
        return

    top_movie = results[0]
    movie_id = top_movie["id"]

    try:
        details = tmdb_client.get_movie_details(movie_id, language="en-US")
    except Exception as e:
        await update.message.reply_text(f"Failed to fetch movie details: {e}")
        return

    release_date = details.get("release_date", "N/A")
    year = release_date.split("-")[0] if release_date else "N/A"
    overview = details.get("overview", "No overview available.")

    summary = f"🎬 *{top_movie['title']}* ({year})\n\n{overview[:300]}{'...' if len(overview) > 300 else ''}"
    await update.message.reply_text(summary, parse_mode=ParseMode.MARKDOWN)

    if not SEARCH_CHANNELS:
        await update.message.reply_text("No channels configured in SEARCH_CHANNELS.")
        return

    try:
        channel_results = await telethon_client.search_in_channels(title, SEARCH_CHANNELS, limit=20)
    except Exception as e:
        await update.message.reply_text(f"Channel search failed: {e}")
        return

    matches = []
    for entity, message in channel_results:
        text = message.text or message.caption or ""
        if filename_parser.matches_constraints(text, lang, max_quality, max_res):
            matches.append((entity, message))

    if not matches:
        await update.message.reply_text("No matching files found in the configured channels.")
        return

    await update.message.reply_text(f"Found {len(matches)} match(es). Showing up to 5:")
    for entity, message in matches[:5]:
        channel_name = getattr(entity, "title", str(entity))
        text = message.text or message.caption or "No text"
        link = get_message_link(entity, message.id)

        result_text = f"📁 {text[:100]}\n📍 Channel: {channel_name}\n🔗 {link}"
        await update.message.reply_text(result_text, disable_web_page_preview=True)


def main():
    if not BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN is not set in .env")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("find", find))

    try:
        telethon_client.init_telethon()
    except Exception as e:
        print(f"Warning: Telethon init failed: {e}")

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
