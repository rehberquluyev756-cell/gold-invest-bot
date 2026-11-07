
import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = os.getenv("CHANNEL_ID")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "GOLD INVESTISIYA botuna xoş gəlmisiniz!\n"
        "Kanala qoşulduqdan sonra yoxlama düyməsinə basın.",
        reply_markup={
            "inline_keyboard": [[
                {
                    "text": "Kanala qoşul",
                    "url": "https://t.me/+fTgfEan8ZwczNTcy"
                },
                {
                    "text": "Üzvlüyü yoxla",
                    "callback_data": "check"
                }
            ]]
        }
    )

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        member = await context.bot.get_chat_member(
            chat_id=CHANNEL,
            user_id=query.from_user.id
        )

        if member.status in ["member", "administrator", "creator"]:
            await query.message.reply_text(
                "Üzvlüyün təsdiqləndi! 3 AZN bonus üçün sorğun qəbul edildi."
            )
        else:
            await query.message.reply_text(
                "Əvvəlcə kanala qoşulmalısan."
            )
    except Exception:
        await query.message.reply_text(
            "Yoxlama alınmadı. Kanal ayarlarını yoxlayın."
        )

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(
    __import__("telegram").ext.CallbackQueryHandler(check, pattern="^check$")
)
app.run_polling()
