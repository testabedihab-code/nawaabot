FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY telegram_clinic_bot_complete.py .
COPY .env .

CMD ["python", "telegram_clinic_bot_complete.py"]
