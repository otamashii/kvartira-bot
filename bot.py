import os
from datetime import date, datetime, timedelta, time, timezone
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

UZ_TZ = timezone(timedelta(hours=5))

cleaning_start_date = date(2026, 3, 22)
cleaning_groups = [
    "Bobursan & Bobur",
    "Shahriyor & Javohir",
    "Akbarali & Suhrob",
    "Shoxrux & Asilbek",
]

shopping_start_date = date(2026, 3, 15)
shopping_groups = [
    "Shoxrux & Asilbek",
    "Akbarali & Suhrob",
    "Shahriyor & Bobursan",
]

def next_sunday(today: date) -> date:
    days_until_sunday = (6 - today.weekday()) % 7
    return today + timedelta(days=days_until_sunday)

def get_cleaning_group(target_date: date) -> str:
    weeks_passed = (target_date - cleaning_start_date).days // 7
    index = weeks_passed % len(cleaning_groups)
    return cleaning_groups[index]

def get_shopping_group(target_date: date) -> str:
    weeks_passed = (target_date - shopping_start_date).days // 7
    index = weeks_passed % len(shopping_groups)
    return shopping_groups[index]

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🤖 Kvartira Navbat Bot komandalar:\n\n"
        "/thisweek - Shu haftadagi navbatlar\n"
        "/tomorrow - Ertangi navbatlar\n"
        "/cleaning - Shu haftadagi tozalash navbati\n"
        "/shopping - Shu haftadagi bozorlik navbati\n"
        "/help - Komandalar ro'yxati"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def this_week(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = datetime.now(UZ_TZ).date()
    sunday = next_sunday(today)
    cleaning = get_cleaning_group(sunday)
    shopping = get_shopping_group(sunday)

    text = (
        f"📢 Shu hafta navbatlar:\n\n"
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

    text = (
        f"🧹 Shu haftadagi tozalash navbati:\n\n"
        f"{cleaning}\n\n"
        f"📅 Sana: {sunday.strftime('%d-%m-%Y')}"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def shopping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = datetime.now(UZ_TZ).date()
    sunday = next_sunday(today)
    shopping = get_shopping_group(sunday)

    text = (
        f"🛒 Shu haftadagi bozorlik navbati:\n\n"
        f"{shopping}\n\n"
        f"📅 Sana: {sunday.strftime('%d-%m-%Y')}"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def send_weekly_notice(context: ContextTypes.DEFAULT_TYPE):
    today = datetime.now(UZ_TZ).date()
    sunday = next_sunday(today)
    cleaning = get_cleaning_group(sunday)
    shopping = get_shopping_group(sunday)

    text = (
        f"📢 Bu hafta navbatlar:\n\n"
        f"🧹 Tozalash: {cleaning}\n"
        f"🛒 Bozorlik: {shopping}\n\n"
        f"📅 Sana: {sunday.strftime('%d-%m-%Y')}"
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
        f"🛒 Bozorlik: {shopping}\n\n"
        f"📅 Sana: {tomorrow.strftime('%d-%m-%Y')}"
    )
    await context.bot.send_message(chat_id=CHAT_ID, text=text)

def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN topilmadi")
    if not CHAT_ID:
        raise ValueError("CHAT_ID topilmadi")

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
    app.run_polling()

if __name__ == "__main__":
    main()