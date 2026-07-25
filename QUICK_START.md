# 🚀 Быстрый старт на VPS (5 минут)

## 1️⃣ Подключитесь к VPS

```bash
ssh root@your_server_ip
```

## 2️⃣ Выполните одну команду

```bash
curl -sSL https://raw.githubusercontent.com/yourusername/drunk-bot/main/deploy.sh | bash
```

**⚠️ Замените URL на свой репозиторий!**

## 3️⃣ Настройте .env

```bash
sudo nano /home/botuser/drunk-bot/.env
```

Добавьте:
```
TELEGRAM_BOT_TOKEN=ваш_токен
```

## 4️⃣ Перезагрузите бота

```bash
sudo systemctl restart drunk-bot
```

## 5️⃣ Проверьте что работает

```bash
sudo systemctl status drunk-bot
sudo journalctl -u drunk-bot -f
```

---

## 📋 Полезные команды

| Команда | Описание |
|---------|---------|
| `sudo systemctl status drunk-bot` | Статус бота |
| `sudo systemctl restart drunk-bot` | Перезагрузить |
| `sudo systemctl stop drunk-bot` | Остановить |
| `sudo systemctl start drunk-bot` | Запустить |
| `sudo journalctl -u drunk-bot -f` | Логи в реальном времени |
| `sudo journalctl -u drunk-bot -n 50` | Последние 50 строк логов |
| `ps aux \| grep python` | Проверить процесс |
| `sudo systemctl enable drunk-bot` | Включить автозагрузку |
| `sudo systemctl disable drunk-bot` | Отключить автозагрузку |

---

## 🔄 Обновление кода

```bash
cd /home/botuser/drunk-bot
sudo -u botuser git pull
sudo -u botuser venv/bin/pip install -r requirements.txt
sudo systemctl restart drunk-bot
```

---

## 📊 Проверка ресурсов

```bash
# Память
free -h

# Диск
df -h

# Процесс бота
ps aux | grep python | grep main.py
```

---

## 💾 Резервная копия БД

```bash
mkdir -p /home/botuser/backups
cp /home/botuser/drunk-bot/sobriety.db \
   /home/botuser/backups/sobriety.db.$(date +%Y%m%d_%H%M%S).bak
```

---

## ❌ Если что-то не работает

```bash
# 1. Смотрите логи
sudo journalctl -u drunk-bot -f

# 2. Проверьте .env
sudo cat /home/botuser/drunk-bot/.env

# 3. Проверьте права
ls -la /home/botuser/drunk-bot/

# 4. Перезагрузитесь
sudo systemctl restart drunk-bot
```

---

## 🎉 Готово!

Ваш бот работает 24/7! 🚀
