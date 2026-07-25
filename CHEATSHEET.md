# 📟 Шпаргалка - все команды в одном месте

## ⚡ 5-минутный старт на VPS

```bash
# 1. Подключитесь
ssh root@your_vps_ip

# 2. Один скрипт все установит
bash <(curl -s https://raw.githubusercontent.com/yourusername/drunk-bot/main/deploy.sh)

# 3. Настройте .env
sudo nano /home/botuser/drunk-bot/.env
# Добавьте: TELEGRAM_BOT_TOKEN=ваш_токен

# 4. Готово!
sudo systemctl restart drunk-bot
sudo systemctl status drunk-bot
```

---

## 🎮 Управление ботом

### Основные команды
```bash
# Статус
sudo systemctl status drunk-bot

# Перезагрузить
sudo systemctl restart drunk-bot

# Остановить
sudo systemctl stop drunk-bot

# Запустить
sudo systemctl start drunk-bot

# Смотреть логи
sudo journalctl -u drunk-bot -f
```

### Логи
```bash
# Реальное время (Ctrl+C выход)
sudo journalctl -u drunk-bot -f

# Последние 50 строк
sudo journalctl -u drunk-bot -n 50

# За последний час
sudo journalctl -u drunk-bot --since "1 hour ago"

# Ошибки только
sudo journalctl -u drunk-bot | grep ERROR
```

---

## 🔄 Обновление кода

```bash
cd /home/botuser/drunk-bot
sudo -u botuser git pull
sudo -u botuser venv/bin/pip install -r requirements.txt
sudo systemctl restart drunk-bot
```

---

## 📊 Мониторинг

### Ресурсы
```bash
# Память
free -h

# Диск
df -h /home/botuser/

# Процесс
ps aux | grep python | grep main.py
```

### Статистика Docker (если используете)
```bash
docker-compose ps
docker stats
docker-compose logs -f
```

---

## 💾 Резервные копии

### Создать
```bash
mkdir -p /home/botuser/backups
cp /home/botuser/drunk-bot/sobriety.db /home/botuser/backups/sobriety.db.$(date +%Y%m%d_%H%M%S).bak
```

### Автоматическая (крон)
```bash
crontab -e
# Добавьте: 0 3 * * * cp /home/botuser/drunk-bot/sobriety.db /home/botuser/backups/sobriety.db.$(date +\%Y\%m\%d)
```

### Восстановить
```bash
cp /home/botuser/backups/sobriety.db.backup /home/botuser/drunk-bot/sobriety.db
sudo systemctl restart drunk-bot
```

---

## 🐛 Отладка

### Проверка файлов
```bash
# Права
ls -la /home/botuser/drunk-bot/

# .env
sudo cat /home/botuser/drunk-bot/.env

# БД
ls -lh /home/botuser/drunk-bot/sobriety.db
```

### Распространённые проблемы

**Проблема: Permission denied**
```bash
sudo chown -R botuser:botuser /home/botuser/drunk-bot
```

**Проблема: Модуль не найден**
```bash
cd /home/botuser/drunk-bot
source venv/bin/activate
pip install -r requirements.txt
```

**Проблема: Порт занят**
```bash
# Telegram бот не использует порты, это не применимо
```

**Проблема: БД повреждена**
```bash
cd /home/botuser/drunk-bot
rm sobriety.db
sudo systemctl restart drunk-bot  # создастся новая
```

---

## 🔐 Безопасность

### SSH ключи
```bash
# На локальном компьютере
ssh-keygen -t ed25519

# Скопируйте ключ
ssh-copy-id -i ~/.ssh/id_ed25519.pub root@your_vps_ip

# На сервере отключите пароли
sudo nano /etc/ssh/sshd_config
# PasswordAuthentication no
sudo systemctl restart sshd
```

### Файрвол
```bash
# UFW
sudo ufw allow 22/tcp
sudo ufw enable

# Открыть только SSH
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
sudo ufw enable
```

---

## 🐳 Docker команды

### Запуск
```bash
docker-compose up -d
```

### Логи
```bash
docker-compose logs -f
docker-compose logs -f --tail 100
```

### Управление
```bash
docker-compose ps
docker-compose restart
docker-compose stop
docker-compose start
```

### Обновление
```bash
git pull
docker-compose up -d --build
```

---

## 📈 Расширенные команды

### Найти все процессы Python
```bash
ps aux | grep python
```

### Убить процесс
```bash
kill -9 PID
# или
pkill -f "python main.py"
```

### Переместить БД на другой диск
```bash
mv /home/botuser/drunk-bot/sobriety.db /mnt/backup/
ln -s /mnt/backup/sobriety.db /home/botuser/drunk-bot/sobriety.db
sudo systemctl restart drunk-bot
```

### Создать горячую копию (без остановки)
```bash
# Требует sqlite3
sqlite3 /home/botuser/drunk-bot/sobriety.db ".backup '/home/botuser/backups/sobriety.hot.bak'"
```

---

## 🌐 Интернет/Сеть

### Проверить IP
```bash
curl ifconfig.me
hostname -I
```

### Проверить соединение с Telegram API
```bash
curl -I https://api.telegram.org
```

### Получить информацию о домене
```bash
nslookup your_domain.com
dig your_domain.com
```

---

## 📱 Тестирование бота

### Быстрый тест
```bash
# Просто откройте Telegram и найдите вашего бота
# Нажмите /start
# Если ответит - бот работает ✓
```

### Тест в группе
```bash
# 1. Создайте новую группу
# 2. Добавьте бота в группу
# 3. Нажмите /start
# 4. Проверьте кнопки
```

---

## 📞 Быстрая помощь

| Проблема | Решение |
|----------|---------|
| Бот не запускается | `sudo systemctl restart drunk-bot` и смотреть логи |
| Ошибка 'Permission denied' | `sudo chown -R botuser:botuser /home/botuser/drunk-bot` |
| 'TELEGRAM_BOT_TOKEN не установлен' | Проверьте `.env` файл |
| Бот медленно работает | Проверьте размер БД, очистите логи |
| Не видно логов | `sudo journalctl --vacuum=1G` для очистки |
| БД повреждена | `rm sobriety.db` и перезагрузить |

---

## 🎯 Оптимальная схема

```
┌─ VPS (Ubuntu 20.04)
│  ├─ Python 3.11
│  ├─ systemd сервис drunk-bot
│  ├─ SQLite БД (sobriety.db)
│  └─ Автоматический перезапуск
│
├─ Резервные копии (ежедневные)
│  └─ /home/botuser/backups/
│
└─ Монитор (journalctl)
   └─ sudo journalctl -u drunk-bot -f
```

---

## 📊 Примеры скриптов

### Скрипт мониторинга
```bash
#!/bin/bash
while true; do
  sudo systemctl status drunk-bot > /dev/null 2>&1
  if [ $? -ne 0 ]; then
    echo "$(date): Бот упал! Перезагружаю..." >> /var/log/bot-monitor.log
    sudo systemctl restart drunk-bot
  fi
  sleep 300  # Проверка каждые 5 минут
done
```

### Скрипт ежедневной резервной копии
```bash
#!/bin/bash
DATE=$(date +%Y%m%d)
BACKUP_DIR="/home/botuser/backups"
mkdir -p $BACKUP_DIR
cp /home/botuser/drunk-bot/sobriety.db $BACKUP_DIR/sobriety.db.$DATE
# Удалить старые (старше 30 дней)
find $BACKUP_DIR -name "*.db.*" -mtime +30 -delete
```

---

## 🎓 Полезные ссылки в проекте

- `README.md` - Основная документация
- `QUICK_START.md` - Быстрый старт за 5 минут
- `DEPLOYMENT.md` - Полный гайд systemd
- `DOCKER.md` - Docker развертывание
- `FAQ.md` - Часто задаваемые вопросы
- `DOCS.md` - Указатель всех документов

---

**Версия:** 1.0  
**Последнее обновление:** 2026-07-25

💡 **Совет:** Сохраните эту шпаргалку! Используйте `Ctrl+F` для поиска команды.
