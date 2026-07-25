#!/bin/bash

# Полезные скрипты для управления ботом на VPS

echo "🤖 Бот-помощник для управления Telegram ботом"
echo ""
echo "Выберите команду:"
echo "1) Статус бота"
echo "2) Смотреть логи (реальное время)"
echo "3) Смотреть последние 100 строк логов"
echo "4) Перезагрузить бота"
echo "5) Остановить бота"
echo "6) Запустить бота"
echo "7) Обновить код из репозитория"
echo "8) Создать резервную копию БД"
echo "9) Проверить ресурсы"
echo "10) Выход"
echo ""
read -p "Введите номер (1-10): " choice

case $choice in
    1)
        echo ""
        echo "📊 Статус бота:"
        sudo systemctl status drunk-bot
        ;;
    2)
        echo ""
        echo "📝 Логи (Ctrl+C для выхода):"
        sudo journalctl -u drunk-bot -f
        ;;
    3)
        echo ""
        echo "📋 Последние 100 строк логов:"
        sudo journalctl -u drunk-bot -n 100 --no-pager
        ;;
    4)
        echo ""
        echo "♻️  Перезагружаю бота..."
        sudo systemctl restart drunk-bot
        sleep 2
        sudo systemctl status drunk-bot
        ;;
    5)
        echo ""
        echo "⛔ Останавливаю бота..."
        sudo systemctl stop drunk-bot
        sleep 2
        sudo systemctl status drunk-bot
        ;;
    6)
        echo ""
        echo "▶️  Запускаю бота..."
        sudo systemctl start drunk-bot
        sleep 2
        sudo systemctl status drunk-bot
        ;;
    7)
        echo ""
        echo "🔄 Обновляю код..."
        cd /home/botuser/drunk-bot
        sudo -u botuser git pull
        sudo -u botuser venv/bin/pip install -r requirements.txt
        echo ""
        echo "✓ Код обновлен. Перезагружаю бота..."
        sudo systemctl restart drunk-bot
        sleep 2
        sudo systemctl status drunk-bot
        ;;
    8)
        echo ""
        echo "💾 Создаю резервную копию БД..."
        BACKUP_DIR="/home/botuser/backups"
        mkdir -p $BACKUP_DIR
        BACKUP_FILE="$BACKUP_DIR/sobriety.db.$(date +%Y%m%d_%H%M%S).bak"
        sudo cp /home/botuser/drunk-bot/sobriety.db $BACKUP_FILE
        sudo chown botuser:botuser $BACKUP_FILE
        echo "✓ БД сохранена: $BACKUP_FILE"
        ls -lh $BACKUP_DIR | tail -5
        ;;
    9)
        echo ""
        echo "🖥️  Использование ресурсов:"
        echo ""
        echo "Память:"
        free -h
        echo ""
        echo "Диск:"
        df -h /home/botuser/
        echo ""
        echo "Процесс бота:"
        ps aux | grep "[p]ython main.py" || echo "Бот не запущен"
        ;;
    10)
        echo "До встречи! 👋"
        exit 0
        ;;
    *)
        echo "❌ Неправильный выбор"
        exit 1
        ;;
esac
