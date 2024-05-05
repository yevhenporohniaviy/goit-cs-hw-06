# Використовуємо базовий образ Python
FROM python:3.11

# Встановлюємо залежності проєкту
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копіюємо файли проєкту в контейнер
COPY main.py /app/main.py
COPY front /app/front
COPY servers /app/servers

# Встановлюємо робочу директорію
WORKDIR /app

# Запускаємо main.py
CMD ["python", "main.py"]