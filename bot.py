import requests
import threading
import time
import asyncio
import signal
import sys
import streamlit as st
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)

# Load secrets safely
try:
    TELEGRAM_TOKEN = st.secrets["TELEGRAM_BOT_TOKEN"]
    SARVAM_API_KEY = st.secrets["SARVAM_API_KEY"]
except Exception:
    # fallback for standalone mode using env vars
    import os
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

SARVAM_URL = "https://api.sarvam.ai/v1/chat/completions"

bot_app = None
bot_thread = None
is_running = False


# ---------- Sarvam ----------
def ask_sarvam(message: str) -> str:

    headers = {
        "Authorization": f"Bearer {SARVAM_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "sarvam-m",
        "messages": [
            {"role": "user", "content": message}
        ],
    }

    try:
        response = requests.post(
            SARVAM_URL,
            headers=headers,
            json=payload,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        print("Sarvam error:", e)
        return "AI error."


# ---------- Telegram handler ----------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    await update.message.chat.send_action("typing")

    reply = ask_sarvam(text)

    await update.message.reply_text(reply)


# ---------- Core bot ----------
def create_app():

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    return app


# ---------- Thread mode ----------
def run_bot_thread():

    global bot_app, is_running

    bot_app = create_app()

    is_running = True

    print("Bot started (thread mode)")

    bot_app.run_polling(stop_signals=None)

    is_running = False


# ---------- Standalone mode ----------
def run_bot_standalone():

    global bot_app, is_running

    bot_app = create_app()

    is_running = True

    print("Bot started (standalone mode)")

    bot_app.run_polling()

    is_running = False


# ---------- Controls ----------
def start_bot():

    global bot_thread, is_running

    if is_running:
        print("Bot already running")
        return

    bot_thread = threading.Thread(
        target=run_bot_thread,
        daemon=True
    )

    bot_thread.start()


def stop_bot():

    global bot_app, is_running

    if bot_app and is_running:

        print("Stopping bot")

        bot_app.stop_running()

        is_running = False


def bot_status():
    return is_running


# ---------- Entry point ----------
if __name__ == "__main__":

    try:
        run_bot_standalone()

    except KeyboardInterrupt:

        print("\nBot stopped by user")

        sys.exit(0)