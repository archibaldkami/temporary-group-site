# Використовуємо офіційний образ Python
FROM python:3.11-slim

# Вимикаємо кешування .pyc файлів та буферизацію виводу
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо залежності та встановлюємо їх
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код у робочу директорію
COPY . .

# Відкриваємо порт для додатку
EXPOSE 5003

# Створюємо некореневого користувача і налаштовуємо права
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Запускаємо додаток через Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5003", "app:app"]