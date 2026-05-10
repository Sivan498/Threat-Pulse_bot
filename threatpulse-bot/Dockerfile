FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
VOLUME ["/app/data"]
ENV DATA_DIR=/app/data
WORKDIR /app/src
CMD ["python", "main.py"]
