# Використовуйте офіційний образ як базовий
FROM python:3.8-slim

# Встановіть робочу директорію в контейнері
WORKDIR /app

# Скопіюйте вміст поточної директорії до контейнера у /app
COPY . /app

# Встановіть необхідні пакети з requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Відкрийте порт 80 для зовнішнього доступу
EXPOSE 80

# Визначте змінну середовища
ENV NAME World

# Запустіть app.py при старті контейнера
CMD ["gunicorn", "--config", "webapp.ini", "app:app"]
