import os
import threading
from flask import Flask
import telebot
from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo
)

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEB_APP_URL = os.getenv("WEB_APP_URL")

bot = telebot.TeleBot(TOKEN) if TOKEN else None


@app.route("/")
def home():
    return "Facebook Helper Telegram Bot is running!"


@app.route("/health")
def health():
    return {"status": "ok"}


def create_keyboard():
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    if WEB_APP_URL:
        button = KeyboardButton(
            text="Open Facebook Mini App",
            web_app=WebAppInfo(url=WEB_APP_URL)
        )
        keyboard.add(button)

    return keyboard


if bot:

    @bot.message_handler(commands=["start"])
    def start(message):
        bot.send_message(
            message.chat.id,
            "Welcome! Your Facebook Helper Bot is ready. "
            "Use the button below to open the mini app.",
            reply_markup=create_keyboard()
        )

    @bot.message_handler(commands=["help"])
    def help_command(message):
        bot.send_message(
            message.chat.id,
            "Available commands:\n"
            "/start - Start the bot\n"
            "/help - Show help\n"
            "/open - Open the mini app"
        )

    @bot.message_handler(commands=["open", "facebook"])
    def open_app(message):
        if WEB_APP_URL:
            bot.send_message(
                message.chat.id,
                "Tap below to open your mini app:",
                reply_markup=create_keyboard()
            )
        else:
            bot.send_message(
                message.chat.id,
                "The mini app has not been configured yet."
            )


def run_bot():
    if bot:
        bot.infinity_polling(
            skip_pending=True,
            timeout=20,
            long_polling_timeout=20
        )


if __name__ == "__main__":
    if bot:
        threading.Thread(
            target=run_bot,
            daemon=True
        ).start()
    else:
        print("Telegram bot token is not configured yet.")

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )
