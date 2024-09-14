FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y sqlite3

ENV PYTHONPATH=/app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "rest_server:app", "--host", "0.0.0.0", "--port", "8000"]
