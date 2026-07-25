# 🛡️ Соbriety Counter Bot

Telegram бот для отслеживания дней без алкоголя.

## 📋 Функции

- **Начать аскезу** - зафиксировать дату и время начала отсчета
- **Счетчик дней** - отслеживание количества дней без алкоголя
- **Обнуление счетчика** - при нажатии кнопки "Выпить"
- **Статистика** - просмотр истории и прогресса
- **Мотивация** - поощрительные сообщения за прогресс

## 🚀 Быстрый старт

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/yourusername/drunk-bot.git
cd drunk-bot
```

### 2. Установите зависимости
```bash
pip install -r requirements.txt
```

### 3. Настройте .env файл
```bash
cp .env.example .env
```

Отредактируйте `.env` и добавьте ваш Telegram Bot Token:
```
TELEGRAM_BOT_TOKEN=ваш_токен_здесь
```

Как получить токен:
1. Напишите боту @BotFather в Telegram
2. Выполните команду `/newbot`
3. Следуйте инструкциям
4. Скопируйте выданный токен в `.env`

### 4. Запустите бота
```bash
python main.py
```

## 📱 Использование

### Кнопки интерфейса

- **🛡️ Взять аскезу** - начать отсчет дней без алкоголя
- **🍺 Выпить** - обнулить счетчик
- **📊 Мой прогресс** - узнать текущее количество дней
- **📈 Статистика** - подробная информация

### Команды

- `/start` - начать работу с ботом
- `/help` - справка
- `/stats` - быстрый просмотр статистики

## 🗄️ База данных

Бот использует SQLite для хранения данных:
- `users` - информация о пользователях и их аскезе
- `history` - история событий

## 📁 Структура проекта

```
drunk-bot/
├── main.py           # Основной файл бота
├── db.py             # Работа с базой данных
├── requirements.txt  # Зависимости
├── .env.example      # Пример конфигурации
├── .env              # Конфигурация (не загружайте в репо!)
├── sobriety.db       # База данных (не загружайте в репо!)
└── README.md         # Этот файл
```

## 🛠️ Технологии

- **Python 3.8+**
- **python-telegram-bot 20.7** - API для работы с Telegram
- **SQLite** - легкая база данных
- **python-dotenv** - управление переменными окружения

## 📊 Возможности расширения

Можно добавить:
- 📈 Графики прогресса
- 🏆 Достижения и награды
- 📧 Напоминания
- 👥 Групповые челленджи
- 💾 Экспорт статистики
- 🌐 Веб-интерфейс

## ⚙️ Развертывание на VPS

### 📖 Полные инструкции по развертыванию

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Полный гайд для systemd (рекомендуется) ⭐
- **[QUICK_START.md](QUICK_START.md)** - Быстрый старт за 5 минут
- **[DOCKER.md](DOCKER.md)** - Развертывание в Docker контейнере
- **[deploy.sh](deploy.sh)** - Автоматический скрипт установки
- **[manage-bot.sh](manage-bot.sh)** - Интерактивное управление ботом

### Рекомендуемый вариант: systemd на Ubuntu/Debian

```bash
# 1. Подключитесь к VPS
ssh root@your_server_ip

# 2. Запустите скрипт установки
curl -sSL https://raw.githubusercontent.com/yourusername/drunk-bot/main/deploy.sh | bash

# 3. Настройте .env
sudo nano /home/botuser/drunk-bot/.env

# 4. Перезагрузите бота
sudo systemctl restart drunk-bot

# 5. Проверьте статус
sudo systemctl status drunk-bot
```

### Быстрые команды управления

```bash
# Статус
sudo systemctl status drunk-bot

# Перезагрузить
sudo systemctl restart drunk-bot

# Логи
sudo journalctl -u drunk-bot -f

# Обновить код
cd /home/botuser/drunk-bot && sudo -u botuser git pull && sudo systemctl restart drunk-bot
```

### На облачных сервисах
- AWS Lambda
- Google Cloud Functions
- Heroku
- Replit
- Railway
- Render

## 📝 Лицензия

MIT License - свободное использование

## 🤝 Помощь и поддержка

Если у вас есть вопросы или идеи - пишите в Issues!

---

**Удачи в борьбе! 💪**
