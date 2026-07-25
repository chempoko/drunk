# 🚀 Развертывание на VPS (Ubuntu/Debian + systemd)

Полная инструкция по запуску бота 24/7 на вашем VPS.

## 📋 Требования

- VPS с Ubuntu 20.04+ или Debian 10+
- SSH доступ к серверу
- Telegram Bot Token от @BotFather
- ~100MB свободного места

## 🔧 Вариант 1: Автоматическое развертывание (рекомендуется)

### Шаг 1: Подключитесь к VPS

```bash
ssh root@your_server_ip
```

### Шаг 2: Скачайте и запустите скрипт установки

```bash
curl -O https://raw.githubusercontent.com/yourusername/drunk-bot/main/deploy.sh
chmod +x deploy.sh
./deploy.sh
```

**ИЛИ** выполните команды вручную ниже (Вариант 2).

---

## 🔧 Вариант 2: Ручное развертывание (пошаговое)

### Шаг 1: Обновите пакеты

```bash
sudo apt update
sudo apt upgrade -y
```

### Шаг 2: Установите Python и зависимости

```bash
sudo apt install -y python3 python3-pip python3-venv git
```

### Шаг 3: Создайте пользователя для бота

```bash
sudo useradd -m -s /bin/bash botuser
```

### Шаг 4: Клонируйте репозиторий

```bash
sudo -u botuser git clone https://github.com/yourusername/drunk-bot.git /home/botuser/drunk-bot
cd /home/botuser/drunk-bot
```

**⚠️ Замените URL на ссылку вашего репозитория!**

### Шаг 5: Создайте виртуальное окружение

```bash
sudo -u botuser python3 -m venv venv
sudo -u botuser venv/bin/pip install --upgrade pip
sudo -u botuser venv/bin/pip install -r requirements.txt
```

### Шаг 6: Настройте переменные окружения

```bash
sudo cp .env.example .env
sudo nano .env
```

В файле добавьте ваш токен:
```
TELEGRAM_BOT_TOKEN=ваш_токен_от_BotFather
```

Сохраните: `Ctrl+X`, затем `Y`, затем `Enter`

### Шаг 7: Создайте systemd сервис

```bash
sudo nano /etc/systemd/system/drunk-bot.service
```

Скопируйте содержимое:

```ini
[Unit]
Description=Drunk Sobriety Counter Telegram Bot
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=botuser
WorkingDirectory=/home/botuser/drunk-bot
Environment="PATH=/home/botuser/drunk-bot/venv/bin"
ExecStart=/home/botuser/drunk-bot/venv/bin/python main.py

# Автоматический перезапуск при падении
Restart=always
RestartSec=10

# Логирование
StandardOutput=journal
StandardError=journal
SyslogIdentifier=drunk-bot

# Ограничения ресурсов
MemoryLimit=512M
CPUQuota=50%

[Install]
WantedBy=multi-user.target
```

Сохраните: `Ctrl+X`, затем `Y`, затем `Enter`

### Шаг 8: Активируйте сервис

```bash
sudo systemctl daemon-reload
sudo systemctl enable drunk-bot
sudo systemctl start drunk-bot
```

### Шаг 9: Проверьте статус

```bash
sudo systemctl status drunk-bot
```

Должно показать: `active (running)` ✅

---

## 📊 Управление ботом

### Смотреть статус
```bash
sudo systemctl status drunk-bot
```

### Смотреть логи в реальном времени
```bash
sudo journalctl -u drunk-bot -f
```

### Просмотреть последние 100 строк логов
```bash
sudo journalctl -u drunk-bot -n 100
```

### Перезагрузить бота
```bash
sudo systemctl restart drunk-bot
```

### Остановить бота
```bash
sudo systemctl stop drunk-bot
```

### Запустить бота
```bash
sudo systemctl start drunk-bot
```

### Отключить автозагрузку
```bash
sudo systemctl disable drunk-bot
```

---

## 🔍 Диагностика проблем

### Проблема: Бот не запускается

```bash
# Проверьте логи
sudo journalctl -u drunk-bot -n 50 --no-pager

# Проверьте права доступа
ls -la /home/botuser/drunk-bot/
sudo chown -R botuser:botuser /home/botuser/drunk-bot

# Проверьте .env файл
sudo cat /home/botuser/drunk-bot/.env
```

### Проблема: "Permission denied"

```bash
# Исправьте права
sudo chown -R botuser:botuser /home/botuser/drunk-bot
sudo chmod 755 /home/botuser/drunk-bot
```

### Проблема: Бот падает и перезагружается

```bash
# Смотрите логи ошибок
sudo journalctl -u drunk-bot -n 200 | grep -i error
```

---

## 🔄 Обновление кода

```bash
cd /home/botuser/drunk-bot

# Скачайте новую версию
sudo -u botuser git pull

# Переустановите зависимости (если они изменились)
sudo -u botuser venv/bin/pip install -r requirements.txt

# Перезагрузите сервис
sudo systemctl restart drunk-bot
```

---

## 🛡️ Безопасность

### 1. Используйте файрвол

```bash
sudo ufw allow 22/tcp    # SSH
sudo ufw enable
```

### 2. Защитите .env файл

```bash
sudo chmod 600 /home/botuser/drunk-bot/.env
sudo chown botuser:botuser /home/botuser/drunk-bot/.env
```

### 3. Используйте SSH ключи вместо пароля

```bash
# На вашем компьютере
ssh-keygen -t ed25519

# Скопируйте публичный ключ на сервер
ssh-copy-id -i ~/.ssh/id_ed25519.pub root@your_server_ip
```

### 4. Отключите вход по паролю

```bash
sudo nano /etc/ssh/sshd_config

# Найдите и измените на:
PasswordAuthentication no
PubkeyAuthentication yes

# Перезагрузите SSH
sudo systemctl restart sshd
```

---

## 📈 Мониторинг

### Установите инструмент для мониторинга (опционально)

```bash
# Простой мониторинг
sudo apt install -y htop
htop

# Проверьте использование памяти ботом
ps aux | grep "python main.py"
```

### Автоматические уведомления при падении

Если вы хотите получать уведомления при перезагрузке бота:

```bash
# Отредактируйте systemd сервис и добавьте:
OnFailure=send-email@%n.service
```

---

## 🌐 Работа с доменом (опционально)

Если нужен веб-интерфейс администратора:

```bash
# Установите nginx
sudo apt install -y nginx

# Настройте reverse proxy на порт бота
sudo nano /etc/nginx/sites-available/default
```

---

## 💾 Резервная копия БД

```bash
# Создайте папку для резервных копий
mkdir -p /home/botuser/backups

# Скопируйте БД
cp /home/botuser/drunk-bot/sobriety.db /home/botuser/backups/sobriety.db.$(date +%Y%m%d_%H%M%S)

# Создайте крон-задачу для автоматических бэкапов
crontab -e

# Добавьте строку (ежедневно в 3:00 утра):
0 3 * * * cp /home/botuser/drunk-bot/sobriety.db /home/botuser/backups/sobriety.db.$(date +\%Y\%m\%d)
```

---

## ✅ Проверка что всё работает

```bash
# 1. Статус сервиса
sudo systemctl status drunk-bot

# 2. Открыт ли процесс Python
ps aux | grep python | grep main.py

# 3. Использование памяти
free -h

# 4. Логи последних 10 минут
sudo journalctl -u drunk-bot --since "10 min ago"

# 5. Тест бота - напишите ему в Telegram
# Бот должен ответить
```

---

## 📞 Поддержка

Если что-то не работает:

1. Проверьте логи: `sudo journalctl -u drunk-bot -f`
2. Проверьте права доступа: `ls -la /home/botuser/drunk-bot/`
3. Проверьте .env: `sudo cat /home/botuser/drunk-bot/.env`
4. Перезагрузитесь: `sudo systemctl restart drunk-bot`

---

## 🎉 Готово!

Ваш бот теперь работает 24/7! 🚀

- ✅ Автоматически перезагружается при падении
- ✅ Стартует при перезагрузке сервера
- ✅ Логируется в systemd журнал
- ✅ Можно управлять через systemctl
