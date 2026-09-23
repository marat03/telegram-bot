import os
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from telegram.error import TelegramError

# Читаем токен и прокси из переменных окружения
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
PROXY_URL = os.environ.get("PROXY_URL")


async def delete_posted(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message

    if not message or not message.text:
        return

    if "posted" not in message.text.lower():
        return

    target = message.reply_to_message
    if not target:
        print("Команда 'posted' не является ответом на сообщение.")
        return

    try:
        await target.delete()
        print(f"Удалено сообщение: {target.text or '[без текста]'}")
    except TelegramError as e:
        print(f"Не удалось удалить целевое сообщение: {e}")

    try:
        await message.delete()
    except TelegramError as e:
        print(f"Не удалось удалить сообщение 'posted': {e}")


def main():
    if not BOT_TOKEN:
        print("Ошибка: переменная TELEGRAM_BOT_TOKEN не задана!")
        return

    builder = Application.builder().token(BOT_TOKEN)

    # Если прокси задан, используем его
    if PROXY_URL:
        builder = builder.base_url(PROXY_URL)
        print(f"Используется прокси: {PROXY_URL}")

    app = builder.build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, delete_posted)
    )

    print("Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()