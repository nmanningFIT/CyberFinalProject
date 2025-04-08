FROM python:3.12
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
# Don't copy app files here as they're mounted as a volume
CMD ["python", "main.py"]