import os
from datetime import date, datetime, timedelta, time, timezone
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

UZ_TZ = timezone(timedelta(hours=5))

# =========================
# TOZALASH JADVALI
# =========================
cleaning_schedule = {
    "2026-03-22": "Bobursan & Bobur",
    "2026-03-29": "Shahriyor & Javohir",

    "2026-04-05": "Akbarali & Suhrob",
    "2026-04-12": "Shoxrux & Asilbek",
    "2026-04-19": "Bobursan & Bobur",
    "2026-04-26": "Shahriyor & Javohir",

    "2026-05-03": "Akbarali & Suhrob",
    "2026-05-10": "Shoxrux & Asilbek",
    "2026-05-17": "Bobursan & Bobur",
    "2026-05-24": "Shahriyor & Javohir",
    "2026-05-31": "Akbarali & Suhrob",

    "2026-06-07": "Shoxrux & Asilbek",
    "2026-06-14": "Bobursan & Bobur",
    "2026-06-21": "Shahriyor & Javohir",
    "2026-06-28": "Akbarali & Suhrob",

    "2026-07-05": "Shoxrux & Asilbek",
    "2026-07-12": "Bobursan & Bobur",
    "2026-07-19": "Shahriyor & Javohir",
    "2026-07-26": "Akbarali & Suhrob",
}

# =========================
# BOZORLIK JADVALI
# =========================
shopping_schedule = {
    "2026-03-15": "Shoxrux & Asilbek",
    "2026-03-22": "Akbarali & Suhrob",
    "2026-03-29": "Shahriyor & Bobursan",

    "2026-04-05": "Shoxrux & Asilbek",
    "2026-04-12": "Akbarali & Suhrob",
    "2026-04-19": "Shahriyor & Bobursan",
    "2026-04-26": "Shoxrux & Asilbek",

    "2026-05-03": "Akbarali & Suhrob",
    "2026-05-10": "Shahriyor & Bobursan",
    "2026-05-17": "Shoxrux & Asilbek",
    "2026-05-24": "Akbarali & Suhrob",
    "2026-05-31": "Shahriyor & Bobursan",

    "2026-06-07": "Shoxrux & Asilbek",
    "2026-06-14": "Akbarali & Suhrob",
    "2026-06-21": "Shahriyor & Bobursan",
    "2026-06-28": "Shoxrux & Asilbek",

    "2026-07-05": "Akbarali & Suhrob",
    "2026-07-12": "Shahriyor & Bobursan",
    "2026-07-19": "Shoxrux & Asilbek",
    "2026-07-26": "Akbarali & Suhrob",
}

def next_sunday(today: date) -> date:
    days_until_sunday = (6 - today.weekday()) % 7
    return today + timedelta(days=days_until_sunday)

def get_cleaning_group(target_date: date) -> str:
    key = target_date.strftime("%Y-%m-%d")
    return cleaning_schedule.get(key, "Navbat yo‘q")

def get_shopping_group(target_date: date) -> str:
    key = target_date.strftime("%Y-%m-%d")
    return shopping_schedule.get(key, "Navbat yo‘q")

# =========================
# COMMANDS
# =========================
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🤖 Kvartira Navbat Bot komandalar:\n\n"
        "/thisweek - Shu haftadagi navbat\n"
        "/tomorrow - Ertangi navbat\n"
        "/cleaning - Tozalash navbati\n"
        "/shopping - Bozorlik navbati\n"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def this_week(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = datetime.now(UZ_TZ).date()
    sunday = next_sunday(today)

    cleaning = get_cleaning_group(sunday)
    shopping = get_shopping_group(sunday)

    text = (
        f"📢 Shu hafta navbat:\n\n"
        f"🧹 Tozalash: {cleaning}\n"
        f"🛒 Bozorlik: {shopping}\n\n"
        f"📅 Sana: {sunday.strftime('%d-%m-%Y')}"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def tomorrow_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = datetime.now(UZ_TZ).date()
    tomorrow = today + timedelta(days=1)

    cleaning = get_cleaning_group(tomorrow)
    shopping = get_shopping_group(tomorrow)

    text = (
        f"⏰ Ertangi navbat:\n\n"
        f"🧹 Tozalash: {cleaning}\n"
        f"🛒 Bozorlik: {shopping}\n\n"
        f"📅 Sana: {tomorrow.strftime('%d-%m-%Y')}"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def cleaning_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = datetime.now(UZ_TZ).date()
    sunday = next_sunday(today)
    cleaning = get_cleaning_group(sunday)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"🧹 Tozalash: {cleaning}")

async def shopping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = datetime.now(UZ_TZ).date()
    sunday = next_sunday(today)
    shopping = get_shopping_group(sunday)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"🛒 Bozorlik: {shopping}")

# =========================
# AUTO MESSAGES
# =========================
async def send_weekly_notice(context: ContextTypes.DEFAULT_TYPE):
    today = datetime.now(UZ_TZ).date()
    sunday = next_sunday(today)

    cleaning = get_cleaning_group(sunday)
    shopping = get_shopping_group(sunday)

    text = (
        f"📢 Bu hafta navbat:\n\n"
        f"🧹 Tozalash: {cleaning}\n"
        f"🛒 Bozorlik: {shopping}\n"
    )
    await context.bot.send_message(chat_id=CHAT_ID, text=text)

async def send_tomorrow_notice(context: ContextTypes.DEFAULT_TYPE):
    today = datetime.now(UZ_TZ).date()
    tomorrow = today + timedelta(days=1)

    cleaning = get_cleaning_group(tomorrow)
    shopping = get_shopping_group(tomorrow)

    text = (
        f"⏰ Eslatma:\n"
        f"Ertaga navbat kuni.\n\n"
        f"🧹 Tozalash: {cleaning}\n"
        f"🛒 Bozorlik: {shopping}"
    )
    await context.bot.send_message(chat_id=CHAT_ID, text=text)

# =========================
# MAIN
# =========================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("thisweek", this_week))
    app.add_handler(CommandHandler("tomorrow", tomorrow_command))
    app.add_handler(CommandHandler("cleaning", cleaning_command))
    app.add_handler(CommandHandler("shopping", shopping_command))

    app.job_queue.run_daily(
        send_weekly_notice,
        time=time(hour=9, minute=0, tzinfo=UZ_TZ),
        days=(0,)
    )

    app.job_queue.run_daily(
        send_tomorrow_notice,
        time=time(hour=20, minute=0, tzinfo=UZ_TZ),
        days=(5,)
    )

    print("Bot ishga tushdi...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()