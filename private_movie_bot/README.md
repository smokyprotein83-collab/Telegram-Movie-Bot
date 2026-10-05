# Private Movie Search Bot

A private Telegram bot that searches for movies across configured channels using TMDB metadata and filename parsing.

## Features

- Search movies by title via TMDB
- Filter results by language, maximum resolution, and maximum quality
- Search configured Telegram channels for matching files
- Access control via allowed user IDs

## Prerequisites

- Python 3.10+
- A Telegram account
- TMDB API key (free at [themoviedb.org](https://www.themoviedb.org/))

## Getting Credentials

1. **Telegram Bot Token**
   - Open Telegram and message [@BotFather](https://t.me/BotFather)
   - Send `/newbot`, follow the prompts, and copy the token

2. **TMDB API Key**
   - Create an account at [themoviedb.org](https://www.themoviedb.org/)
   - Go to Settings -> API -> Create new key
   - Copy the API key (v3 auth)

3. **Telegram API ID and Hash**
   - Go to [my.telegram.org](https://my.telegram.org)
   - Log in with your phone number
   - Go to "API development tools"
   - Create an application and copy the `api_id` and `api_hash`

4. **Your Telegram User ID**
   - Message [@userinfobot](https://t.me/userinfobot)
   - It will reply with your numeric user ID

## Setup

1. Clone or copy this project folder.

2. Activate the virtual environment:
   ```bash
   private_movie_bot\venv\Scripts\activate
   ```

3. Fill in `.env` with your credentials:
   ```
   TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN_HERE
   TMDB_API_KEY=YOUR_TMDB_API_KEY_HERE
   TELEGRAM_API_ID=YOUR_TELEGRAM_API_ID_HERE
   TELEGRAM_API_HASH=YOUR_TELEGRAM_API_HASH_HERE
   ALLOWED_USER_IDS=YOUR_TELEGRAM_USER_ID_HERE
   SEARCH_CHANNELS=@channel1,@channel2
   ```

4. **Configure channels:**
   - Edit `.env` and replace `@channel1,@channel2` with your actual Telegram channel usernames.
   - Separate multiple channels with commas.

5. **Configure allowed users:**
   - Edit `.env` and replace `YOUR_TELEGRAM_USER_ID_HERE` with your numeric user ID.
   - To allow multiple users, separate IDs with commas: `123456,789012`
   - To allow everyone (not recommended), leave `ALLOWED_USER_IDS` empty.

## Running

```bash
private_movie_bot\venv\Scripts\activate
python bot.py
```

On the first run, Telethon may ask for your phone number and a login code in the console. Enter them when prompted. After that, a session file (`movie_bot_session.session`) will be created and you won't need to log in again.

## Usage

- `/start` - Show help and usage instructions
- `/find <title> [lang] [max_res] [max_quality]`

### Examples

```
/find Inception malayalam 1080p web-dl
/find "Baahubali 2" tamil 720p bluray
/find Avengers english 2160p blu-ray
/find Dangal hindi
```

## Supported Languages

- malayalam / ml
- tamil / ta
- hindi / hi
- english / en

## Supported Resolutions

- 480p
- 720p
- 1080p
- 2160p

## Supported Sources (quality filters)

- CAM
- TELESYNC
- HDRIP
- WEB-DL
- BLU-RAY

Higher quality values include lower ones. For example, `max_quality=web-dl` will match CAM, TELESYNC, HDRIP, and WEB-DL files.

## Notes

- The bot searches channel messages for the title and then filters by filename/caption constraints.
- Results are limited to 5 matches per command.
- Keep your `.env` file private and never commit it to version control.
