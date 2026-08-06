import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
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


# ─── Клавиатуры ────────────────────────────────────────────────

def get_main_keyboard():
    """Reply-клавиатура для личных чатов"""
    keyboard = [
        ["📊 Мой прогресс"],
        ["🛡️ Взять аскезу", "🍺 Выпить"],
        ["📈 Статистика"],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_group_reply_keyboard():
    """Reply-клавиатура для панели ввода в групповых чатах"""
    keyboard = [
        ["🛡️ Взять аскезу", "🍺 Выпить"],
        ["📊 Мой прогресс", "📈 Статистика"],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_inline_keyboard():
    """Inline-клавиатура для групповых чатов"""
    keyboard = [
        [
            InlineKeyboardButton("🛡️ Взять аскезу", callback_data="abstinence"),
            InlineKeyboardButton("🍺 Выпить", callback_data="drink"),
        ],
        [
            InlineKeyboardButton("📊 Мой прогресс", callback_data="progress"),
            InlineKeyboardButton("📈 Статистика", callback_data="stats"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def is_group_chat(update: Update) -> bool:
    """Проверить, является ли чат групповым"""
    chat_type = update.effective_chat.type if update.effective_chat else None
    return chat_type in ("group", "supergroup")


# ─── Команды ────────────────────────────────────────────────────

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

    if is_group_chat(update):
        await update.message.reply_text(
            welcome_text,
            parse_mode="HTML",
            reply_markup=get_inline_keyboard(),
        )
        # Также отправляем reply-клавиатуру на панель ввода
        await update.message.reply_text(
            "👇 Кнопки на панели ввода:",
            reply_markup=get_group_reply_keyboard(),
        )
    else:
        await update.message.reply_text(
            welcome_text,
            parse_mode="HTML",
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

    if is_group_chat(update):
        await update.message.reply_text(help_text, parse_mode="HTML", reply_markup=get_inline_keyboard())
        await update.message.reply_text(
            "👇 Кнопки на панели ввода:",
            reply_markup=get_group_reply_keyboard(),
        )
    else:
        await update.message.reply_text(help_text, parse_mode="HTML", reply_markup=get_main_keyboard())


# ─── Обработчики действий ──────────────────────────────────────

def _get_reply_markup(update: Update):
    """Выбрать reply-клавиатуру в зависимости от типа чата"""
    if is_group_chat(update):
        return get_group_reply_keyboard()
    return get_main_keyboard()


async def handle_abstinence(update: Update, context: ContextTypes.DEFAULT_TYPE, is_callback: bool = False) -> None:
    """Обработка 'Взять аскезу'"""
    user = update.effective_user

    if is_abstinence_active(user.id):
        text = (
            "⚠️ <b>У тебя уже есть активная аскеза!</b>\n\n"
            "Нажми 'Выпить' чтобы закончить текущую, а потом сможешь начать новую."
        )
    else:
        create_or_update_user(user.id, user.username, user.first_name)
        set_abstinence_start(user.id)
        text = (
            f"🛡️ <b>Аскеза начата!</b>\n\n"
            f"Дата и время: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n"
            f"Отсчет начался. Ты можешь это! 💪"
        )

    if is_callback:
        query = update.callback_query
        await query.message.reply_text(text, parse_mode="HTML", reply_markup=get_inline_keyboard())
    else:
        await update.message.reply_text(text, parse_mode="HTML", reply_markup=_get_reply_markup(update))


async def handle_drinking(update: Update, context: ContextTypes.DEFAULT_TYPE, is_callback: bool = False) -> None:
    """Обработка 'Выпить'"""
    user = update.effective_user

    if not is_abstinence_active(user.id):
        text = "⚠️ У тебя еще нет активной аскезы. Нажми 'Взять аскезу' чтобы начать."
    else:
        days_passed = get_days_of_abstinence(user.id)
        record_drinking(user.id)
        text = (
            f"😔 <b>Счетчик обнулен</b>\n\n"
            f"Ты продержался: <b>{days_passed}</b> дней\n\n"
            f"Не унывай! Это опыт. Начни заново 💪"
        )

    if is_callback:
        query = update.callback_query
        await query.message.reply_text(text, parse_mode="HTML", reply_markup=get_inline_keyboard())
    else:
        await update.message.reply_text(text, parse_mode="HTML", reply_markup=_get_reply_markup(update))


async def handle_progress(update: Update, context: ContextTypes.DEFAULT_TYPE, is_callback: bool = False) -> None:
    """Обработка 'Мой прогресс'"""
    user = update.effective_user

    if not is_abstinence_active(user.id):
        text = (
            "⏳ <b>Аскеза не начата</b>\n\n"
            "Нажми на кнопку <b>Взять аскезу</b> чтобы начать отсчет."
        )
    else:
        days = get_days_of_abstinence(user.id)
        emoji = "🔥" if days >= 7 else "📈"
        text = (
            f"{emoji} <b>Твой прогресс:</b>\n\n"
            f"<b>{days}</b> дней без алкоголя\n\n"
        )
        if days >= 30:
            text += "🎉 Отличный результат! Продолжай в том же духе!\n"
        elif days >= 14:
            text += "😮 Воу-воу! Кто ты воин!?\n"
        elif days >= 7:
            text += "💪 Неплохо! Неделя позади!\n"
        elif days >= 1:
            text += "🌱 Хороший старт! Каждый день - это победа!\n"
        else:
            text += "🆕 Ты только что начал! Держи курс!\n"

    if is_callback:
        query = update.callback_query
        await query.message.reply_text(text, parse_mode="HTML", reply_markup=get_inline_keyboard())
    else:
        await update.message.reply_text(text, parse_mode="HTML", reply_markup=_get_reply_markup(update))


async def handle_statistics(update: Update, context: ContextTypes.DEFAULT_TYPE, is_callback: bool = False) -> None:
    """Обработка 'Статистика'"""
    user = update.effective_user
    group_stats = get_group_stats()

    if not group_stats:
        text = (
            "📊 В чате пока нет активных аскез.\n\n"
            "Нажми 'Взять аскезу' чтобы начать! 🛡️"
        )
    else:
        text = "📊 <b>Статистика чата:</b>\n\n"
        text += "🏆 <b>Лидеры по дням:</b>\n"
        for idx, stats in enumerate(group_stats, 1):
            medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else "📌"
            text += f"\n{medal} <b>{stats['first_name']}</b>: {stats['days']} дней"
        text += f"\n\n👥 <b>Всего участников:</b> {len(group_stats)}"

        user_position = None
        for idx, stats in enumerate(group_stats, 1):
            if stats['user_id'] == user.id:
                user_position = idx
                break
        if user_position:
            text += f"\n\n👤 <b>Твоя позиция:</b> #{user_position}"

    if is_callback:
        query = update.callback_query
        await query.message.reply_text(text, parse_mode="HTML", reply_markup=get_inline_keyboard())
    else:
        await update.message.reply_text(text, parse_mode="HTML", reply_markup=_get_reply_markup(update))


# ─── CallbackQueryHandler (inline-кнопки) ──────────────────────

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка нажатий на inline-кнопки"""
    query = update.callback_query
    data = query.data

    logger.info(f"📩 Получен callback: data={data}, user={query.from_user.id}, chat={query.message.chat.id if query.message else 'N/A'}")

    # Обязательно отвечаем на callback, чтобы Telegram знал, что мы обработали нажатие
    # Показываем всплывающее уведомление пользователю
    await query.answer(text=f"Обрабатываю: {data}...", show_alert=False)

    if data == "abstinence":
        await handle_abstinence(update, context, is_callback=True)
    elif data == "drink":
        await handle_drinking(update, context, is_callback=True)
    elif data == "progress":
        await handle_progress(update, context, is_callback=True)
    elif data == "stats":
        await handle_statistics(update, context, is_callback=True)
    else:
        logger.warning(f"⚠️ Неизвестный callback data: {data}")
        await query.answer(text="Неизвестная команда", show_alert=True)


# ─── MessageHandler (текстовые сообщения) ──────────────────────

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка текстовых сообщений (личные чаты и reply-кнопки в группах)"""
    text = update.message.text

    if text == "🛡️ Взять аскезу":
        await handle_abstinence(update, context)
    elif text == "🍺 Выпить":
        await handle_drinking(update, context)
    elif text == "📊 Мой прогресс":
        await handle_progress(update, context)
    elif text == "📈 Статистика":
        await handle_statistics(update, context)
    elif is_group_chat(update):
        # В групповых чатах игнорируем произвольный текст, но не кнопки
        return
    else:
        await update.message.reply_text(
            "Я тебя не понимаю 🤔\n\nИспользуй кнопки меню ниже.",
            reply_markup=_get_reply_markup(update),
        )


# ─── Главная функция ────────────────────────────────────────────

def main():
    """Главная функция"""
    application = Application.builder().token(BOT_TOKEN).build()

    # CommandHandler имеет приоритет по умолчанию (group=0)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", handle_statistics))
    
    # CallbackQueryHandler должен быть выше MessageHandler в порядке обработки
    # group=1 означает более высокий приоритет, чем у MessageHandler (group=2)
    application.add_handler(CallbackQueryHandler(button_callback), group=1)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text), group=2)

    logger.info("Бот запущен...")
    # Явно указываем allowed_updates, чтобы получать callback_query
    application.run_polling(allowed_updates=["message", "callback_query", "chat_member"])


if __name__ == "__main__":
    main()
