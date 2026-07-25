import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from db import (
    init_db,
    create_or_update_user,
    set_abstinence_start,
    record_drinking,
    get_days_of_abstinence,
    get_user_stats,
    is_abstinence_active,
    get_group_stats,
)

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не установлен в .env файле")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

init_db()


def get_main_keyboard():
    """Получить основную клавиатуру"""
    keyboard = [
        ["📊 Мой прогресс"],
        ["🛡️ Взять аскезу", "🍺 Выпить"],
        ["📈 Статистика"],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка команды /start"""
    user = update.effective_user
    create_or_update_user(user.id, user.username, user.first_name)
    
    welcome_text = (
        f"🌟 Привет, {user.first_name}!\n\n"
        "Я бот для отслеживания дней без алкоголя.\n\n"
        "Мои функции:\n"
        "🛡️ <b>Взять аскезу</b> - начать отсчет дней\n"
        "🍺 <b>Выпить</b> - обнулить счетчик\n"
        "📊 <b>Мой прогресс</b> - посмотреть текущий счетчик\n"
        "📈 <b>Статистика</b> - подробная информация\n\n"
        "Начни с кнопки <b>Взять аскезу</b>!"
    )
    
    await update.message.reply_text(
        welcome_text,
        parse_mode="HTML",
        reply_markup=get_main_keyboard(),
    )


async def handle_abstinence(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка кнопки 'Взять аскезу'"""
    user = update.effective_user
    
    # Проверяем есть ли уже активная аскеза
    if is_abstinence_active(user.id):
        await update.message.reply_text(
            "⚠️ <b>У тебя уже есть активная аскеза!</b>\n\n"
            "Нажми 'Выпить' чтобы закончить текущую, а потом сможешь начать новую.",
            parse_mode="HTML",
            reply_markup=get_main_keyboard(),
        )
        return
    
    create_or_update_user(user.id, user.username, user.first_name)
    set_abstinence_start(user.id)
    
    text = (
        f"🛡️ <b>Аскеза начата!</b>\n\n"
        f"Дата и время: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n"
        f"Отсчет начался. Ты можешь это! 💪"
    )
    
    await update.message.reply_text(text, parse_mode="HTML", reply_markup=get_main_keyboard())


async def handle_drinking(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка кнопки 'Выпить'"""
    user = update.effective_user
    
    # Проверяем есть ли активная аскеза
    if not is_abstinence_active(user.id):
        await update.message.reply_text(
            "⚠️ У тебя еще нет активной аскезы. Нажми 'Взять аскезу' чтобы начать.",
            reply_markup=get_main_keyboard(),
        )
        return
    
    # Получаем количество дней перед обнулением
    days_passed = get_days_of_abstinence(user.id)
    
    # Фиксируем что пользователь выпил
    record_drinking(user.id)
    
    text = (
        f"😔 <b>Счетчик обнулен</b>\n\n"
        f"Ты продержался: <b>{days_passed}</b> дней\n\n"
        f"Не унывай! Это опыт. Начни заново 💪"
    )
    
    await update.message.reply_text(text, parse_mode="HTML", reply_markup=get_main_keyboard())


async def handle_progress(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка кнопки 'Мой прогресс'"""
    user = update.effective_user
    
    # Проверяем есть ли активная аскеза
    if not is_abstinence_active(user.id):
        text = (
            "⏳ <b>Аскеза не начата</b>\n\n"
            "Нажми на кнопку <b>Взять аскезу</b> чтобы начать отсчет."
        )
        await update.message.reply_text(text, parse_mode="HTML", reply_markup=get_main_keyboard())
        return
    
    days = get_days_of_abstinence(user.id)
    
    emoji = "🔥" if days >= 7 else "📈"
    text = (
        f"{emoji} <b>Твой прогресс:</b>\n\n"
        f"<b>{days}</b> дней без алкоголя\n\n"
    )
    
    if days >= 30:
        text += "🎉 Отличный результат! Продолжай в том же духе!\n"
    elif days >= 7:
        text += "💪 Неплохо! Еще немного и неделя будет позади!\n"
    elif days >= 1:
        text += "🌱 Хороший старт! Каждый день - это победа!\n"
    else:
        text += "🆕 Ты только что начал! Держи курс!\n"
    
    await update.message.reply_text(text, parse_mode="HTML", reply_markup=get_main_keyboard())


async def handle_statistics(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка кнопки 'Статистика' - показывает групповую статистику"""
    user = update.effective_user
    
    # Получаем групповую статистику (всех активных пользователей)
    group_stats = get_group_stats()
    
    if not group_stats:
        await update.message.reply_text(
            "📊 В чате пока нет активных аскез.\n\n"
            "Нажми 'Взять аскезу' чтобы начать! 🛡️",
            reply_markup=get_main_keyboard(),
        )
        return
    
    text = "📊 <b>Статистика чата:</b>\n\n"
    text += "🏆 <b>Лидеры по дням:</b>\n"
    
    for idx, stats in enumerate(group_stats, 1):
        medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else "📌"
        text += f"\n{medal} <b>{stats['first_name']}</b>: {stats['days']} дней"
    
    text += f"\n\n👥 <b>Всего участников:</b> {len(group_stats)}"
    
    # Если текущий пользователь в списке - показываем его позицию
    user_position = None
    for idx, stats in enumerate(group_stats, 1):
        if stats['user_id'] == user.id:
            user_position = idx
            break
    
    if user_position:
        text += f"\n\n👤 <b>Твоя позиция:</b> #{user_position}"
    
    await update.message.reply_text(text, parse_mode="HTML", reply_markup=get_main_keyboard())


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка текстовых сообщений"""
    text = update.message.text
    
    if text == "🛡️ Взять аскезу":
        await handle_abstinence(update, context)
    elif text == "🍺 Выпить":
        await handle_drinking(update, context)
    elif text == "📊 Мой прогресс":
        await handle_progress(update, context)
    elif text == "📈 Статистика":
        await handle_statistics(update, context)
    else:
        await update.message.reply_text(
            "Я тебя не понимаю 🤔\n\nИспользуй кнопки меню ниже.",
            reply_markup=get_main_keyboard(),
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /help"""
    help_text = (
        "🤖 <b>Доступные команды:</b>\n\n"
        "/start - Начать работу с ботом\n"
        "/help - Эта справка\n"
        "/stats - Быстрый просмотр статистики\n\n"
        "<b>Кнопки:</b>\n"
        "🛡️ Взять аскезу - начать отсчет\n"
        "🍺 Выпить - обнулить счетчик\n"
        "📊 Мой прогресс - посмотреть дни\n"
        "📈 Статистика - полная информация"
    )
    
    await update.message.reply_text(help_text, parse_mode="HTML", reply_markup=get_main_keyboard())


def main():
    """Главная функция"""
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", handle_statistics))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    logger.info("Бот запущен...")
    application.run_polling()


if __name__ == "__main__":
    main()
