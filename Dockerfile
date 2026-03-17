# Базовый Python образ
FROM python:3.12-slim

# Убираем блокировку Python вывода (полезно для логов Django)
ENV PYTHONUNBUFFERED=1

# Устанавливаем зависимости для компиляции и SQLite
RUN apt-get update && apt-get install -y \
    build-essential \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . /app/

# Открываем порт (если используешь Django runserver)
EXPOSE 8000

# Команда запуска (можно изменить под gunicorn)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
