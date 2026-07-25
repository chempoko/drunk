FROM python:3.11-slim

# Установим переменные окружения
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Установим рабочую директорию
WORKDIR /app

# Скопируем requirements.txt
COPY requirements.txt .

# Установим зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопируем весь код
COPY . .

# Запустим бота
CMD ["python", "main.py"]
