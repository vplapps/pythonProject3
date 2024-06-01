# Використовуйте офіційний образ як базовий
FROM python:3.8-slim

# Встановіть робочу директорію в контейнері
WORKDIR /app

# Встановіть залежності для pyodbc і драйвера MS SQL
RUN apt-get update && apt-get install -y \
    unixodbc-dev \
    gcc \
    g++ \
    && apt-get clean

# Встановіть драйвер ODBC для SQL Server
RUN apt-get install -y curl apt-transport-https
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

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
