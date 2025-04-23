# FROM python:3.12
# WORKDIR /app
# COPY requirements.txt /app/
# RUN pip install --no-cache-dir -r requirements.txt
# CMD ["python", "main.py"]

FROM python:alpine

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app /app