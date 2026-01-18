FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY transprutSolutions /app/transprutSolutions

EXPOSE 8000

CMD ["sh", "-c", "gunicorn webserver.wsgi --chdir transprutSolutions --bind 0.0.0.0:${PORT:-8000}"]
