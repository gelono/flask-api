# Используем базовый образ Python
FROM python:3.9

# Устанавливаем переменную окружения для обеспечения работоспособности приложения в контейнере
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Обновляем pip до последней версии
RUN pip install --no-cache-dir --upgrade pip

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости приложения
RUN pip install web3==6.18.0
RUN pip install hyperliquid-python-sdk

# Определяем порт, который будет прослушивать приложение
EXPOSE 5000

# Команда для запуска вашего приложения
CMD ["python", "sock/skt_server.py"]