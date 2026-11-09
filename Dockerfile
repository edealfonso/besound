FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DJANGO_SETTINGS_MODULE=besound.settings.docker

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN useradd --create-home appuser \
    && mkdir -p /app/staticfiles /app/media \
    && chown -R appuser /app/staticfiles /app/media \
    && chmod +x docker/entrypoint.sh
USER appuser

EXPOSE 8000

ENTRYPOINT ["docker/entrypoint.sh"]
# PORT is set by Render; WEB_CONCURRENCY (gunicorn workers) defaults to 2 to fit in 512 MB
ENV WEB_CONCURRENCY=2
CMD ["sh", "-c", "exec gunicorn besound.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]
