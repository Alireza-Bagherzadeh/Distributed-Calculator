FROM python:3.10-slim
WORKDIR /app
# اضافه شدن پکیج‌های لازم برای کامپایل psycopg2
RUN apt-get update && apt-get install -y libpq-dev gcc
# نصب کتابخانه‌ها
RUN pip install flask requests psycopg2-binary flask-cors
COPY parser-service-app.py .
CMD ["python","parser-service-app.py"]



