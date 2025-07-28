FROM --platform=linux/amd64 python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

ENV INPUT_DIR=/input
ENV OUTPUT_DIR=/output

CMD ["python", "main.py"]
