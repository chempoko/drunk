#!/bin/bash

# Скрипт для развертывания Telegram бота на VPS (Ubuntu/Debian)

set -e

echo "🚀 Начинаем установку Telegram бота на VPS..."

# 1. Обновляем пакеты
echo "📦 Обновляем пакеты..."
sudo apt update
sudo apt upgrade -y

# 2. Устанавливаем Python и зависимости
echo "🐍 Устанавливаем Python..."
sudo apt install -y python3 python3-pip python3-venv git

# 3. Создаем пользователя для бота (опционально)
echo "👤 Создаем пользователя для бота..."
if ! id -u botuser > /dev/null 2>&1; then
    sudo useradd -m -s /bin/bash botuser
    echo "✓ Пользователь botuser создан"
else
    echo "✓ Пользователь botuser уже существует"
fi

# 4. Клонируем репозиторий
PROJECT_DIR="/home/botuser/drunk-bot"
echo "📂 Клонируем проект в $PROJECT_DIR..."
sudo -u botuser git clone https://github.com/yourusername/drunk-bot.git $PROJECT_DIR 2>/dev/null || echo "⚠️ Замените URL на свой репозиторий"

# 5. Создаем виртуальное окружение
echo "📦 Создаем виртуальное окружение..."
cd $PROJECT_DIR
sudo -u botuser python3 -m venv venv

# 6. Устанавливаем зависимости
echo "📦 Устанавливаем зависимости..."
sudo -u botuser venv/bin/pip install --upgrade pip
sudo -u botuser venv/bin/pip install -r requirements.txt

# 7. Настраиваем .env
echo "🔑 Настраиваем переменные окружения..."
if [ ! -f .env ]; then
    sudo cp .env.example .env
    echo "⚠️ Отредактируйте $PROJECT_DIR/.env и добавьте TELEGRAM_BOT_TOKEN"
    echo "Команда: sudo nano $PROJECT_DIR/.env"
else
    echo "✓ Файл .env уже существует"
fi

# 8. Создаем systemd сервис
echo "⚙️ Создаем systemd сервис..."
sudo tee /etc/systemd/system/drunk-bot.service > /dev/null <<EOF
[Unit]
Description=Drunk Sobriety Counter Telegram Bot
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=botuser
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PROJECT_DIR/venv/bin/python main.py

# Автоматический перезапуск при падении
Restart=always
RestartSec=10

# Логирование
StandardOutput=journal
StandardError=journal
SyslogIdentifier=drunk-bot

# Ограничения ресурсов (опционально)
MemoryLimit=512M
CPUQuota=50%

[Install]
WantedBy=multi-user.target
EOF

# 9. Активируем сервис
echo "🔄 Активируем сервис..."
sudo systemctl daemon-reload
sudo systemctl enable drunk-bot
sudo systemctl start drunk-bot

# 10. Проверяем статус
echo ""
echo "✅ Установка завершена!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Отредактируйте .env и добавьте TELEGRAM_BOT_TOKEN:"
echo "   sudo nano $PROJECT_DIR/.env"
echo ""
echo "2. Перезагрузите сервис:"
echo "   sudo systemctl restart drunk-bot"
echo ""
echo "3. Проверьте статус:"
echo "   sudo systemctl status drunk-bot"
echo ""
echo "4. Смотрите логи:"
echo "   sudo journalctl -u drunk-bot -f"
