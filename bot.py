import os
import asyncio
import logging
from telethon import TelegramClient, events

# Secure credentials using environment variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

SESSION_NAME = "channelmonbot"

# Source and target channels
SOURCE_CHANNELS = [
    "topdealsflop",
    "shopibot",
    "Canva_free_link"
]

# Target channel (your personal/channel to receive converted messages)
TARGET_CHANNEL = "lootalerts01"

# Converter bots in rotation
CONVERTER_BOTS = [
    "ekconverter9bot",
    "ekconverter10bot",
    "ekconverter11bot",
    "ekconverter12bot",
    "ekconverter13bot",
    "ekconverter14bot",
    "ekconverter15bot",
    "ekconverter16bot",
    "ekconverter17bot",
    "ekconverter18bot",
    "ekconverter19bot",
    "ekconverter20bot"
]

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# Track which bot to use
bot_index = 0

async def convert_text(original_text: str, bot_username: str) -> str:
    try:
        async with client.conversation(bot_username, timeout=60) as conv:
            await conv.send_message(original_text)
            response = await conv.get_response()
            return response.text
    except Exception as exc:
        logging.error(f"[{bot_username}] Conversion failed: {exc}")
        return original_text

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):
    global bot_index
    try:
        message = event.message
        logging.info(f"🟢 Message from source: {event.chat.username} | ID: {message.id}")

        original_text = getattr(message, 'text', None) or getattr(message, 'message', None) or ""


        # Rotate to the next converter bot
        converter_bot = CONVERTER_BOTS[bot_index % len(CONVERTER_BOTS)]
        bot_index += 1

        converted_text = await convert_text(original_text, converter_bot)

        if message.media:
            temp_file = await message.download_media()
            await client.send_file(
                TARGET_CHANNEL,
                temp_file,
                caption=converted_text or "",
                parse_mode="html"
            )
        else:
            await client.send_message(TARGET_CHANNEL, converted_text, parse_mode="html")

        logging.info(f"✅ Sent using {converter_bot}")

    except Exception as e:
        logging.exception(f"❌ Error processing message: {e}")

def main():
    print(">>> Bot is starting. Listening for messages and rotating converter bots...")
    client.start()
    client.run_until_disconnected()

if __name__ == "__main__":
    main()
