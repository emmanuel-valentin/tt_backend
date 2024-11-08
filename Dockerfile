FROM python:3.13.0-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x /app/start-server.sh

EXPOSE 8000

ENTRYPOINT ["/app/start-server.sh"]