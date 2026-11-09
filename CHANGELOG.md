# Changelog

All notable changes to this project. Format based on [Keep a Changelog](https://keepachangelog.com/).

## [2.0.0] - 2026-11-09

A full update of the project, three years after the first version.

### Added
- Docker setup: `Dockerfile`, `docker-compose.yml` with PostgreSQL 16, gunicorn and nginx (serving static and media files), automatic migrations and `collectstatic`.
- `besound/settings/docker.py`, configured with environment variables (`.env.example`).
- Audio upload validation: files are checked by their real content (WebM, MP4/M4A, MP3, OGG, WAV) and by size (`MAX_AUDIO_UPLOAD_MB`, 10 MB by default). The front-end sends WebM recordings named `.mp3`, so the file name and declared type are not trusted.
- Optional pagination of `/v1/posts/list` with `?limit=&offset=` (max 100 per page). Without parameters it still returns the plain list, so the current front-end keeps working.
- Tests for registration, upload validation, pagination and deletion.
- `manage.py` (it was excluded from the repo), README in English and Spanish, this changelog.
- `docker-compose.server.yml` and a deployment guide (`docs/DESPLIEGUE.md`) for a server with Caddy in front, able to host several projects.

### Changed
- Django 4.2 (end of support) → 5.2 LTS. DRF, django-cors-headers and django-solo updated.
- django-ckeditor (CKEditor 4, end of support) → django-ckeditor-5. Stored texts are unchanged.
- psycopg2 → psycopg 3, Unipath → pathlib, Python 3.12.
- `secret.json` is now optional; settings can also come from environment variables.
- Deleting someone else's sound returns `403 Forbidden` instead of `401`.
- nginx keeps the original `X-Forwarded-Proto` when there is another proxy in front, avoiding an HTTPS redirect loop.

### Fixed
- `/v1/register` returned the password hash in its response, skipped password validation and briefly stored the password in plain text.
- Deleting a sound left its audio file on disk.
- Database engine `postgresql_psycopg2` no longer exists in modern Django; now `postgresql`.
- `ImproperlyConfigured` was used in settings without being imported.

### Security
- Production: `DEBUG` off by default, HTTPS redirect, secure cookies and HSTS always on.
- CORS limited to the front-end (`localhost:3000` and `besound.vercel.app`) instead of any origin.
- CSRF and clickjacking middleware enabled again (they protect the admin; the API uses tokens).
- User audio recordings are no longer tracked in git.

## [1.0.0] - 2023-06-28

First version: Django REST API for the besound front-end, with users and token authentication, audio posts (list, upload, delete) and all page texts editable from the Django admin.
