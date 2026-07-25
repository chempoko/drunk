# 🐳 Развертывание в Docker (альтернативный вариант)

Docker вариант проще для изоляции и масштабирования, но требует Docker на сервере.

## Требования

- VPS с Ubuntu 20.04+
- Docker и Docker Compose установлены

## 🚀 Установка Docker

```bash
# Обновите пакеты
sudo apt update && sudo apt upgrade -y

# Установите Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
rm get-docker.sh

# Добавьте пользователя в группу docker
sudo usermod -aG docker $USER

# Установите Docker Compose
sudo apt install -y docker-compose

# Проверьте версии
docker --version
docker-compose --version
```

## 📦 Развертывание бота

### Шаг 1: Клонируйте репозиторий

```bash
git clone https://github.com/yourusername/drunk-bot.git
cd drunk-bot
```

### Шаг 2: Создайте .env файл

```bash
cp .env.example .env
nano .env
```

Добавьте:
```
TELEGRAM_BOT_TOKEN=ваш_токен
```

### Шаг 3: Запустите бота

```bash
# Первый запуск (скачает образ и запустит)
docker-compose up -d

# Проверьте статус
docker-compose ps
```

## 📋 Управление Docker контейнером

| Команда | Описание |
|---------|---------|
| `docker-compose ps` | Статус контейнера |
| `docker-compose logs -f` | Логи в реальном времени |
| `docker-compose logs --tail 100` | Последние 100 строк логов |
| `docker-compose restart` | Перезагрузить бота |
| `docker-compose stop` | Остановить бота |
| `docker-compose start` | Запустить бота |
| `docker-compose up -d` | Запустить в фоне |
| `docker-compose down` | Остановить и удалить контейнер |

## 🔄 Обновление кода

```bash
git pull
docker-compose up -d --build
```

## 💾 Резервная копия БД

```bash
# Скопируйте БД из контейнера
docker cp drunk-bot:/app/sobriety.db ./backups/sobriety.db.backup

# Или локально (БД находится в текущей папке)
cp sobriety.db backups/sobriety.db.$(date +%Y%m%d_%H%M%S)
```

## 🔍 Диагностика

```bash
# Логи ошибок
docker-compose logs -f --tail 50

# Войти в контейнер
docker-compose exec drunk-bot bash

# Статистика использования ресурсов
docker stats

# Информация о контейнере
docker inspect drunk-bot
```

## 🌐 Использование с nginx (обратный прокси)

```nginx
upstream drunk_bot {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://drunk_bot;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## ⚡ Оптимизация

### Ограничение ресурсов

Отредактируйте `docker-compose.yml`:

```yaml
services:
  drunk-bot:
    # ... остальное
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

### Использование .dockerignore

Создайте файл `.dockerignore`:

```
.git
.gitignore
__pycache__
*.pyc
*.pyo
.env
sobriety.db
```

## 🛑 Полный перезапуск

```bash
# Остановите все контейнеры
docker-compose down

# Удалите образ (опционально)
docker rmi drunk-bot:latest

# Запустите заново
docker-compose up -d --build
```

## 📊 Мониторинг

```bash
# Реальное время статистики
docker stats

# История использования
docker-compose logs | grep ERROR
```

## 🔐 Безопасность

1. **Не коммитьте .env файл!** - используйте `.gitignore`
2. **Используйте переменные окружения** - не hardcode токены
3. **Регулярно обновляйте** - `docker pull` и `git pull`
4. **Ограничивайте ресурсы** - как показано выше

## 🎉 Готово!

Ваш бот работает в Docker контейнере и автоматически перезагружается при падении!

---

## 📌 Сравнение: systemd vs Docker

| Параметр | systemd | Docker |
|----------|---------|--------|
| **Сложность** | Средняя | Высокая |
| **Ресурсы** | Минимальные | Больше |
| **Изоляция** | Нет | Да |
| **Масштабируемость** | Плохая | Хорошая |
| **Обновления** | Ручные | Простые |
| **Рекомендуется** | Для малых проектов | Для production |

Рекомендуем **systemd** для начала, Docker для более сложных случаев.
