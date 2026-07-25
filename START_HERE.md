# 🎉 ВСЁ ГОТОВО! Инструкция по развертыванию на VPS

Поздравляю! 🎊 Ваш проект полностью подготовлен к развертыванию на VPS.

---

## 🚀 САМЫЙ БЫСТРЫЙ СПОСОБ (5 минут)

### Шаг 1: Подключитесь к VPS через SSH

```bash
ssh root@your_vps_ip
```

Замените `your_vps_ip` на IP адрес вашего VPS.

### Шаг 2: Запустите автоматический скрипт

```bash
curl -sSL https://raw.githubusercontent.com/yourusername/drunk-bot/main/deploy.sh | bash
```

**⚠️ ВАЖНО:** Замените `yourusername` на ваше имя пользователя GitHub!

### Шаг 3: Добавьте Telegram Bot Token

```bash
sudo nano /home/botuser/drunk-bot/.env
```

Найдите строку:
```
TELEGRAM_BOT_TOKEN=вставьте_ваш_токен_здесь
```

Замените на реальный токен от @BotFather.

### Шаг 4: Перезагрузите бота

```bash
sudo systemctl restart drunk-bot
```

### Шаг 5: Проверьте что работает

```bash
sudo systemctl status drunk-bot
```

Должно показать: `active (running)` ✅

---

## 📖 ДОКУМЕНТАЦИЯ ПО РАЗВЕРТЫВАНИЮ

### Если вы хотите систему...

**systemd** (встроенная в Linux) - ⭐ РЕКОМЕНДУЕТСЯ
→ [DEPLOYMENT.md](DEPLOYMENT.md)

**Docker** (изолированная в контейнере)
→ [DOCKER.md](DOCKER.md)

**Быстрый старт за 5 минут**
→ [QUICK_START.md](QUICK_START.md)

**Все команды в одном месте**
→ [CHEATSHEET.md](CHEATSHEET.md)

**Частые вопросы и ответы**
→ [FAQ.md](FAQ.md)

---

## ⚙️ УПРАВЛЕНИЕ БОТОМ

### После установки используйте эти команды:

```bash
# Статус бота
sudo systemctl status drunk-bot

# Смотреть логи в реальном времени
sudo journalctl -u drunk-bot -f

# Перезагрузить бота
sudo systemctl restart drunk-bot

# Обновить код из Git
cd /home/botuser/drunk-bot
sudo -u botuser git pull
sudo systemctl restart drunk-bot
```

Подробнее → [CHEATSHEET.md](CHEATSHEET.md)

---

## 📦 СТРУКТУРА ФАЙЛОВ ПРОЕКТА

```
drunk-bot/
├── 🤖 ОСНОВНОЙ КОД
│   ├── main.py                    ← Основной бот
│   ├── db.py                      ← База данных
│   └── requirements.txt           ← Зависимости
│
├── 🔧 КОНФИГУРАЦИЯ
│   ├── .env                       ← Переменные окружения
│   ├── .env.example               ← Пример .env
│   └── .gitignore                 ← Git ignore
│
├── 🖥️ РАЗВЕРТЫВАНИЕ (systemd)
│   ├── deploy.sh                  ← Автоустановка (один скрипт!)
│   ├── manage-bot.sh              ← Интерактивное управление
│   ├── DEPLOYMENT.md              ← Полный гайд
│   └── QUICK_START.md             ← Быстрый старт
│
├── 🐳 РАЗВЕРТЫВАНИЕ (Docker)
│   ├── Dockerfile                 ← Docker образ
│   ├── docker-compose.yml         ← Docker Compose
│   └── DOCKER.md                  ← Гайд Docker
│
└── 📚 ДОКУМЕНТАЦИЯ
    ├── README.md                  ← Основная документация
    ├── DOCS.md                    ← Указатель всех документов
    ├── FAQ.md                     ← Частые вопросы
    ├── CHEATSHEET.md              ← Шпаргалка команд
    └── CHANGELOG.md               ← История изменений
```

---

## ✅ CHECKLIST ДО ЗАПУСКА

- [ ] У меня есть VPS с Ubuntu/Debian
- [ ] У меня есть SSH доступ
- [ ] Я получил Telegram Bot Token от @BotFather
- [ ] Я скопировал ссылку своего GitHub репозитория
- [ ] Я готов запустить скрипт

Если все ✅, то готовы к началу!

---

## 🎯 РЕКОМЕНДУЕМАЯ ПОСЛЕДОВАТЕЛЬНОСТЬ

### День 1: Настройка
```bash
# 1. Подключитесь к VPS
ssh root@your_vps_ip

# 2. Запустите скрипт (полная установка)
bash <(curl -s https://raw.githubusercontent.com/yourusername/drunk-bot/main/deploy.sh)

# 3. Отредактируйте .env
sudo nano /home/botuser/drunk-bot/.env

# 4. Перезагрузитесь
sudo systemctl restart drunk-bot

# 5. Проверьте статус
sudo systemctl status drunk-bot
```

### День 2: Тестирование
```bash
# 1. Откройте Telegram
# 2. Найдите вашего бота
# 3. Нажмите /start
# 4. Протестируйте все кнопки
```

### День 3+: Управление
```bash
# Используйте команды управления (см выше)
# Выполняйте регулярные обновления
# Следите за логами
```

---

## 🔐 ПЕРВОНАЧАЛЬНАЯ БЕЗОПАСНОСТЬ

После развертывания **обязательно**:

1. **Отключите пароль SSH** (используйте только ключи)
   ```bash
   sudo nano /etc/ssh/sshd_config
   # PasswordAuthentication no
   sudo systemctl restart sshd
   ```

2. **Включите файрвол**
   ```bash
   sudo ufw allow 22/tcp
   sudo ufw enable
   ```

3. **Создайте резервную копию**
   ```bash
   cp /home/botuser/drunk-bot/sobriety.db ~/backups/
   ```

---

## 📞 НУЖНА ПОМОЩЬ?

1. **Прочитайте FAQ.md** - там ответы на 95% вопросов
2. **Посмотрите логи** - `sudo journalctl -u drunk-bot -f`
3. **Используйте CHEATSHEET.md** - все команды в одном месте
4. **Создайте Issue на GitHub** с логами ошибки

---

## 🎉 ПОЗДРАВЛЯЕМ!

Теперь ваш бот:
- ✅ Работает 24/7 на VPS
- ✅ Автоматически перезагружается при падении
- ✅ Запускается при перезагрузке сервера
- ✅ Имеет полное логирование
- ✅ Легко управляется и обновляется

---

## 📊 СЛЕДУЮЩИЕ ШАГИ

1. **Пригласите друзей в чат** - бот будет собирать статистику по всем
2. **Мотивируйте друзей** - рейтинг лидеров вдохновляет!
3. **Отслеживайте прогресс** - используйте кнопку "Статистика"
4. **Проходите челленджи** - соревнуйтесь с друзьями!

---

## 📚 ПОЛЕЗНЫЕ ССЫЛКИ

| Потребность | Ссылка |
|------------|--------|
| Быстрый старт | [QUICK_START.md](QUICK_START.md) |
| Системный администратор | [DEPLOYMENT.md](DEPLOYMENT.md) |
| Используется Docker | [DOCKER.md](DOCKER.md) |
| Срочно нужна команда | [CHEATSHEET.md](CHEATSHEET.md) |
| Есть вопрос | [FAQ.md](FAQ.md) |

---

**Готово к запуску! 🚀**

Если у вас возникают вопросы - смотрите документацию, она очень подробная!

**Удачи! 💪**
