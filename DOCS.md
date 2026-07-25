# 📚 Полная документация

Все файлы документации для запуска и управления ботом.

## 🚀 Начало работы

| Файл                                 | Описание                    |
| ------------------------------------ | --------------------------- |
| **[QUICK_START.md](QUICK_START.md)** | ⚡ Быстрый старт за 5 минут |
| **[README.md](README.md)**           | 📖 Основная документация   |
| **[FAQ.md](FAQ.md)**                 | ❓ Часто задаваемые вопросы |

## 🖥️ Развертывание на VPS

### systemd (рекомендуется)
| Файл                               | Описание                                 |
| ---------------------------------- | ---------------------------------------- |
| **[DEPLOYMENT.md](DEPLOYMENT.md)** | 📚 Полный гайд развертывания на systemd |
| **[deploy.sh](deploy.sh)**         | 🤖 Автоматический скрипт установки      |
| **[manage-bot.sh](manage-bot.sh)** | ⚙️ Интерактивное управление ботом      |

### Docker (альтернатива)
| Файл                                         | Описание                        |
| -------------------------------------------- | ------------------------------- |
| **[DOCKER.md](DOCKER.md)**                   | 🐳 Развертывание в Docker      |
| **[Dockerfile](Dockerfile)**                 | 📦 Конфигурация Docker образа  |
| **[docker-compose.yml](docker-compose.yml)** | 🐳 Docker Compose конфигурация |

## 📝 Другие файлы

| Файл                                     | Описание                        |
| ---------------------------------------- | ------------------------------- |
| **[CHANGELOG.md](CHANGELOG.md)**         | 📋 История изменений           |
| **[requirements.txt](requirements.txt)** | 📦 Python зависимости          |
| **[.env.example](.env.example)**         | 🔑 Пример переменных окружения |
| **[.gitignore](.gitignore)**             | 🚫 Git ignore правила          |

## 🎯 快速 навигация

### Я хочу запустить бота...

**...локально на своем компьютере**
→ Смотрите [README.md](README.md) раздел "Быстрый старт"

**...на VPS (лучший вариант)**
→ Смотрите [DEPLOYMENT.md](DEPLOYMENT.md) или [QUICK_START.md](QUICK_START.md)

**...в Docker**
→ Смотрите [DOCKER.md](DOCKER.md)

**...быстро за 5 минут**
→ Смотрите [QUICK_START.md](QUICK_START.md)

### У меня возник вопрос о...

**...развертывании**
→ Смотрите [DEPLOYMENT.md](DEPLOYMENT.md) или [DOCKER.md](DOCKER.md)

**...управлении ботом**
→ Используйте `./manage-bot.sh` или смотрите [DEPLOYMENT.md](DEPLOYMENT.md)

**...частых проблемах**
→ Смотрите [FAQ.md](FAQ.md)

## 📋 Рекомендуемый путь

### День 1: Тестирование локально

```bash
# 1. Читаете README.md
# 2. Устанавливаете локально
# 3. Тестируете функции
```

### День 2: Развертывание на VPS

```bash
# Выберите один вариант:
# A) systemd (рекомендуется)
#    - Читайте DEPLOYMENT.md
#    - Запустите deploy.sh
#    - Используйте manage-bot.sh для управления

# B) Docker (если нужна изоляция)
#    - Читайте DOCKER.md
#    - Используйте docker-compose

# C) Быстрый способ
#    - Смотрите QUICK_START.md
#    - Выполняйте команды пошагово
```

### День 3+: Управление и мониторинг

```bash
# Используйте команды из DEPLOYMENT.md:
sudo systemctl status drunk-bot
sudo journalctl -u drunk-bot -f

# Обновления
cd /home/botuser/drunk-bot
git pull
sudo systemctl restart drunk-bot
```

## 🆘 Помощь

1. **Прочитайте [FAQ.md](FAQ.md)** - ответы на 95% вопросов
2. **Проверьте логи** - `sudo journalctl -u drunk-bot -f`
3. **Создайте Issue** на GitHub с:
   - Дистрибутивом ОС
   - Логами ошибок
   - Шагами воспроизведения

## 🔗 Ссылки на команды

### Управление сервисом
```bash
sudo systemctl status drunk-bot     # Статус
sudo systemctl restart drunk-bot    # Перезагрузить
sudo systemctl start drunk-bot      # Запустить
sudo systemctl stop drunk-bot       # Остановить
sudo systemctl enable drunk-bot     # Автозагрузка вкл
sudo systemctl disable drunk-bot    # Автозагрузка выкл
```

### Логи
```bash
sudo journalctl -u drunk-bot -f             # Реальное время
sudo journalctl -u drunk-bot -n 100         # Последние 100 строк
sudo journalctl -u drunk-bot --since "1h"   # За час
```

### Управление
```bash
./manage-bot.sh                              # Интерактивное меню
cd /home/botuser/drunk-bot
sudo -u botuser git pull                     # Обновить код
sudo systemctl restart drunk-bot             # Перезагрузить
```

## 📞 Контакты

- 🐛 Баги и предложения → Issues на GitHub
- 💬 Вопросы → Discussions на GitHub
- 📧 Email → [ваш email]

---

**Версия:** 1.0.0  
**Последнее обновление:** 2026-07-25  
**Статус:** ✅ Production Ready
