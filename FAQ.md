# ❓ FAQ - Часто задаваемые вопросы

## 🚀 Развертывание

### Q: Какой способ развертывания выбрать?
**A:** 
- **systemd** (рекомендуется) - простой, надежный, встроен в Linux
- **Docker** - если нужна изоляция и масштабируемость
- **supervisor** - если systemd недоступен

### Q: Сколько времени займет развертывание?
**A:** 
- Автоматический скрипт: **5-10 минут**
- Ручное развертывание: **15-20 минут**
- Docker: **5 минут** (если Docker уже установлен)

### Q: Какие требования к VPS?
**A:**
- ОС: Ubuntu 20.04+ или Debian 10+
- ОЗУ: минимум 256MB (рекомендуется 512MB+)
- Диск: минимум 100MB свободного места
- CPU: 1 ядро достаточно

### Q: Подойдет ли бесплатный уровень хостинга?
**A:** Да, подойдет:
- Oracle Cloud (бесплатный уровень)
- AWS (первый год бесплатно)
- Azure (кредиты для стартапов)
- Heroku (с ограничениями)

---

## 🔧 Управление ботом

### Q: Как я буду знать что бот работает?
**A:**
```bash
sudo systemctl status drunk-bot
# Должно быть: active (running)

# Или смотрите логи
sudo journalctl -u drunk-bot -f
```

### Q: Как обновить код?
**A:**
```bash
cd /home/botuser/drunk-bot
sudo -u botuser git pull
sudo systemctl restart drunk-bot
```

### Q: Как посмотреть логи ошибок?
**A:**
```bash
sudo journalctl -u drunk-bot --since "1 hour ago"
sudo journalctl -u drunk-bot -n 100  # последние 100 строк
sudo journalctl -u drunk-bot | grep ERROR
```

### Q: Бот упал/не отвечает. Что делать?
**A:**
1. Проверьте статус: `sudo systemctl status drunk-bot`
2. Смотрите логи: `sudo journalctl -u drunk-bot -f`
3. Перезагрузитесь: `sudo systemctl restart drunk-bot`
4. Проверьте .env: `sudo cat /home/botuser/drunk-bot/.env`

### Q: Как остановить бота?
**A:**
```bash
sudo systemctl stop drunk-bot
```

### Q: Как отключить автозагрузку?
**A:**
```bash
sudo systemctl disable drunk-bot
```

---

## 🗄️ База данных

### Q: Где хранятся данные пользователей?
**A:** В файле `sobriety.db` в папке проекта. SQLite база данных.

### Q: Как создать резервную копию?
**A:**
```bash
cp /home/botuser/drunk-bot/sobriety.db /home/botuser/backups/sobriety.db.backup
```

### Q: Как восстановить из резервной копии?
**A:**
```bash
# Сделайте текущую резервную копию
cp /home/botuser/drunk-bot/sobriety.db /home/botuser/drunk-bot/sobriety.db.old

# Скопируйте резервную копию обратно
cp /home/botuser/backups/sobriety.db.backup /home/botuser/drunk-bot/sobriety.db

# Перезагрузитесь
sudo systemctl restart drunk-bot
```

### Q: Как автоматизировать резервные копии?
**A:**
```bash
# Добавьте крон-задачу
crontab -e

# Добавьте строку (ежедневно в 3:00):
0 3 * * * cp /home/botuser/drunk-bot/sobriety.db /home/botuser/backups/sobriety.db.$(date +\%Y\%m\%d)
```

### Q: База данных повреждена. Что делать?
**A:**
```bash
# Удалите повреждённую БД
rm /home/botuser/drunk-bot/sobriety.db

# Перезагрузитесь (создастся новая)
sudo systemctl restart drunk-bot
```

---

## 🔒 Безопасность

### Q: Где хранится мой токен Telegram?
**A:** В файле `.env` в корне проекта. Он в `.gitignore` и не загружается в репозиторий.

### Q: Как защитить .env файл?
**A:**
```bash
sudo chmod 600 /home/botuser/drunk-bot/.env
sudo chown botuser:botuser /home/botuser/drunk-bot/.env
```

### Q: Нужен ли SSL сертификат?
**A:** Нет, не нужен. Бот подключается к Telegram API через HTTPS.

### Q: Как использовать SSH ключи вместо пароля?
**A:**
```bash
# На локальном компьютере
ssh-keygen -t ed25519

# Скопируйте ключ на сервер
ssh-copy-id -i ~/.ssh/id_ed25519.pub root@your_server_ip

# Отключите пароли в /etc/ssh/sshd_config
# PasswordAuthentication no
```

---

## 📊 Мониторинг и производительность

### Q: Сколько памяти использует бот?
**A:**
```bash
ps aux | grep "[p]ython main.py"
# Обычно 30-50 MB
```

### Q: Как проверить использование ресурсов?
**A:**
```bash
free -h           # Память
df -h             # Диск
top -b -n 1 | grep python  # CPU
```

### Q: Бот тормозит. Как оптимизировать?
**A:**
1. Проверьте размер БД: `ls -lh sobriety.db`
2. Если > 1GB, архивируйте старые данные
3. Очистите логи: `journalctl --vacuum=100M`

### Q: Можно ли запустить несколько ботов?
**A:** Да, создайте разные сервисы:
```bash
# /etc/systemd/system/drunk-bot-1.service
# /etc/systemd/system/drunk-bot-2.service
```

---

## 🐛 Отладка

### Q: "Permission denied" ошибка
**A:**
```bash
sudo chown -R botuser:botuser /home/botuser/drunk-bot
sudo chmod -R 755 /home/botuser/drunk-bot
```

### Q: "TELEGRAM_BOT_TOKEN не установлен"
**A:**
```bash
# Проверьте .env
sudo cat /home/botuser/drunk-bot/.env

# Убедитесь что токен установлен:
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
```

### Q: БД заблокирована
**A:**
```bash
# Перезагрузитесь
sudo systemctl restart drunk-bot

# Или удалите lock файл
rm /home/botuser/drunk-bot/sobriety.db-wal
rm /home/botuser/drunk-bot/sobriety.db-shm
```

### Q: Бот не видит группу/чат
**A:**
1. Убедитесь что бот добавлен в группу
2. Бот должен быть администратором (опционально)
3. Проверьте что в группе не отключены боты

---

## 💰 Стоимость

### Q: Бесплатно ли запускать бота?
**A:** 
- Telegram Bot API - **БЕСПЛАТНО**
- VPS - **от $2.5/месяц** (например, DigitalOcean)
- Доменное имя - **от $1/год** (опционально)

Итого: **~$3/месяц** минимум

### Q: Какие хосты рекомендуются?
**A:**
- **DigitalOcean** - $4/месяц ($6 за месяц с лучшей скоростью)
- **Linode** - $5/месяц
- **Vultr** - $2.5/месяц
- **Hetzner** - €3/месяц
- **AWS EC2** - первый год бесплатно

---

## 📞 Другое

### Q: Как узнать свой IP адрес VPS?
**A:**
```bash
curl ifconfig.me
# или
hostname -I
```

### Q: Как переустановить Python?
**A:**
```bash
sudo apt install --reinstall python3 python3-pip python3-venv
cd /home/botuser/drunk-bot
rm -rf venv
python3 -m venv venv
venv/bin/pip install -r requirements.txt
sudo systemctl restart drunk-bot
```

### Q: Можно ли использовать бота лично (не в группе)?
**A:** Да, полностью работает в личных чатах! Каждый пользователь имеет свой счётчик.

### Q: Как отправить логи для отладки?
**A:**
```bash
sudo journalctl -u drunk-bot -n 200 > logs.txt
# Отправьте файл logs.txt
```

---

## 🎯 Помощь

Если ответа на ваш вопрос нет - создайте Issue на GitHub!

```bash
# Полезные диагностические команды
sudo systemctl status drunk-bot
sudo journalctl -u drunk-bot -f
ps aux | grep python
free -h
df -h
```

**Удачи! 🚀**
