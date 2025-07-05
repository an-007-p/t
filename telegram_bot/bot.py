import sys
print("Python version:", sys.version)
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from datetime import time

CHAT_ID = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CHAT_ID
    CHAT_ID = update.effective_chat.id
    await update.message.reply_text("Включаю напоминния на 9:00 и 21:00")

async def send_morning_reminder(context):
    if CHAT_ID:
        await context.bot.send_message(chat_id=CHAT_ID, text="Доброе утро! ☀️ Как настроение?")
async def test_morning(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Тест: доброе утро!")

async def send_evening_reminder(context):
    if CHAT_ID:
        await context.bot.send_message(chat_id=CHAT_ID, text="Добрый вечер! 🌙 Как прошёл день?")

# Этапы
MORNING_1, MORNING_2, MORNING_3, MORNING_4, MORNING_5 = range(5)
EVENING_Q1, EVENING_Q2, EVENING_Q3, EVENING_Q4, EVENING_Q5, EVENING_Q6 = range(10, 16)

# Лог
logging.basicConfig(level=logging.INFO)

# START
async def start2 (update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я помогу тебе отслеживать день 🌞 /morning — утренний чек-ин, 🌙 /evening — вечернее завершение дня."
    )

# УТРО
async def morning_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("☀️ Утренняя запись\n\n1. Как я себя чувствую сейчас?")
    return MORNING_1

async def morning_q1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["morning_q1"] = update.message.text
    await update.message.reply_text("2. Что для меня сегодня главное?")
    return MORNING_2

async def morning_q2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["morning_q2"] = update.message.text
    await update.message.reply_text("3. Какие три вещи помогут мне держать фокус сегодня?")
    return MORNING_3

async def morning_q3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["morning_q3"] = update.message.text
    await update.message.reply_text("4. Что я хочу избежать сегодня?")
    return MORNING_4

async def morning_q4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["morning_q4"] = update.message.text
    await update.message.reply_text("5. Что я сделаю для себя сегодня?")
    return MORNING_5

async def morning_q5(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["morning_q5"] = update.message.text

    summary = (
        "🌅 *Твоя утренняя запись:*\n\n"
        f"1. 🧘 Как я себя чувствую: {context.user_data['morning_q1']}\n"
        f"2. 🎯 Главное сегодня: {context.user_data['morning_q2']}\n"
        f"3. 🎧 Что поможет держать фокус: {context.user_data['morning_q3']}\n"
        f"4. ❌ Чего хочу избежать: {context.user_data['morning_q4']}\n"
        f"5. 💝 Что сделаю для себя: {context.user_data['morning_q5']}"
    )

    await update.message.reply_text(summary, parse_mode="Markdown")
    return ConversationHandler.END

# ВЕЧЕР
async def evening(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧾 Сегодня ты сделала…")
    return EVENING_Q1

async def evening_q1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["evening_q1"] = update.message.text
    await update.message.reply_text("🫂 Как ты к себе сегодня отнеслась?")
    return EVENING_Q2

async def evening_q2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["evening_q2"] = update.message.text
    await update.message.reply_text("✨ Чем ты сегодня гордишься?")
    return EVENING_Q3

async def evening_q3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["evening_q3"] = update.message.text
    await update.message.reply_text("🙏 За что ты себе благодарна?")
    return EVENING_Q4

async def evening_q4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["evening_q4"] = update.message.text
    await update.message.reply_text("🧪 Что сработало, а что — нет?")
    return EVENING_Q5

async def evening_q5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["evening_q5"] = update.message.text
    await update.message.reply_text("💤 Что поможет тебе завтра?")
    return EVENING_Q6

async def evening_q6(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["evening_q6"] = update.message.text

    summary = (
        "🌙 *Вечерний отчёт:*\n\n"
        f"1. 🧾 Сегодня я сделала: {context.user_data['evening_q1']}\n"
        f"2. 🫂 Как я к себе отнеслась: {context.user_data['evening_q2']}\n"
f"3. ✨ Чем я горжусь: {context.user_data['evening_q3']}\n"
        f"4. 🙏 За что благодарна: {context.user_data['evening_q4']}\n"
        f"5. 🧪 Что сработало / не сработало: {context.user_data['evening_q5']}\n"
        f"6. 💤 Что поможет завтра: {context.user_data['evening_q6']}"
    )

    await update.message.reply_text(summary, parse_mode="Markdown")
    return ConversationHandler.END

# ОТМЕНА
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Запись отменена. Возвращайся когда будешь готова 🌿")
    return ConversationHandler.END

# ЗАПУСК
if __name__ == "__main__":
    TOKEN = "7830180476:AAFSiLdlVSv72ApNxzp8m7gJd09a7g3_jd4"
    app = ApplicationBuilder().token(TOKEN).build()

    morning_conv = ConversationHandler(
        entry_points=[CommandHandler("morning", morning_start)],
        states={
            MORNING_1: [MessageHandler(filters.TEXT & ~filters.COMMAND, morning_q1)],
            MORNING_2: [MessageHandler(filters.TEXT & ~filters.COMMAND, morning_q2)],
            MORNING_3: [MessageHandler(filters.TEXT & ~filters.COMMAND, morning_q3)],
            MORNING_4: [MessageHandler(filters.TEXT & ~filters.COMMAND, morning_q4)],
            MORNING_5: [MessageHandler(filters.TEXT & ~filters.COMMAND, morning_q5)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    evening_conv = ConversationHandler(
        entry_points=[CommandHandler("evening", evening)],
        states={
            EVENING_Q1: [MessageHandler(filters.TEXT & ~filters.COMMAND, evening_q1)],
            EVENING_Q2: [MessageHandler(filters.TEXT & ~filters.COMMAND, evening_q2)],
            EVENING_Q3: [MessageHandler(filters.TEXT & ~filters.COMMAND, evening_q3)],
            EVENING_Q4: [MessageHandler(filters.TEXT & ~filters.COMMAND, evening_q4)],
            EVENING_Q5: [MessageHandler(filters.TEXT & ~filters.COMMAND, evening_q5)],
            EVENING_Q6: [MessageHandler(filters.TEXT & ~filters.COMMAND, evening_q6)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("start2", start2))
    app.add_handler(CommandHandler("test_morning", test_morning))
    app.add_handler(morning_conv)
    app.add_handler(evening_conv)
    
    job_queue = app.job_queue
    job_queue.run_daily(send_morning_reminder, time(hour=9, minute=0))
    job_queue.run_daily(send_evening_reminder, time(hour=21, minute=0))

    print("Бот запущен...")
    app.run_polling()
