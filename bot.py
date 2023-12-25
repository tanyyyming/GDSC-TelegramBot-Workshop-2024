import os
import requests

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")

UPLOAD_PHOTO = range(1)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and ask the user to upload a picture."""

    await update.message.reply_text(
        "Hi! Please send the picture you want me to write a caption for."
    )

    return UPLOAD_PHOTO


async def reply_with_caption(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Reply the user photo with a caption."""
    # Stores the photo in the context
    photo_file = await update.message.photo[-1].get_file()
    photo_path = photo_file.file_path
    await photo_file.download_to_drive("data/user_photo.jpg")

    # Sends the photo to the API and gets the caption
    url = "https://image-caption-generator2.p.rapidapi.com/v2/captions"
    querystring = {
        "imageUrl": photo_path,
        "useEmojis": "true",
        "useHashtags": "true",
        "limit": "1",
        "vibe": "cute",
    }
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "image-caption-generator2.p.rapidapi.com",
    }
    response = requests.get(url, headers=headers, params=querystring).json()
    caption = response["captions"][0]

    # Reply the user with the caption
    await update.message.reply_text(caption)

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""

    await update.message.reply_text("Bye! I hope we can talk again some day.")

    return ConversationHandler.END


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""

    await update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # add conversation handler with the states UPLOAD_PHOTO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            UPLOAD_PHOTO: [MessageHandler(filters.PHOTO, reply_with_caption)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
