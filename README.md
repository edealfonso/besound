# besound

[English](README.md) · [Español](README.es.md)

![besound home page: a list of recorded sounds, each labelled with a word](docs/screenshot.png)

> besound was my final project for my university master's degree, built in 2023 and updated in 2026 (see [My contribution](#my-contribution)).

besound is a web app for sharing short sound experiences. Anyone can open the site and listen to the sounds other people have recorded, each labelled with a single word. Registered users record up to 15 seconds of audio from the browser, give it a title and publish it, and can delete it later if they change their mind.

This repository is the **back-end**: a REST API built with Django that handles users, authentication and audio uploads, plus an admin where every text shown in the app can be edited without touching code. The front-end is a Next.js app in [besound-front](https://github.com/edealfonso/besound-front).

## Features

- **REST API** for registration, token login, and listing, uploading and deleting sounds.
- **Editable content**: every text of the app (home, login, register, record and about pages) is a singleton model in the Django admin, with a rich text editor for the recording instructions.
- **Safe uploads**: audio files are validated by their real content (WebM, MP4/M4A, MP3, OGG, WAV) and by size, not by the name or type the browser declares.
- **Ownership**: only the author can delete a sound, and its file is removed from disk too.
- **Optional pagination** of the sound list with `?limit=&offset=`.
- **Docker**: PostgreSQL, gunicorn and nginx start with one command for local development.
- **Free deployment**: API on Render, database on Neon and audio files on Cloudflare R2, with a one-click Render Blueprint (`render.yaml`).
- **Secure by default**: secrets out of the repo, CORS limited to the front-end, HTTPS redirect, secure cookies and HSTS in production.
- **Tested**: registration, upload validation, pagination and deletion.

## Tech stack

| Area | Technologies |
|---|---|
| Back-end | Python 3.12, Django 5.2 LTS, Django REST Framework, PostgreSQL 16 (psycopg 3), django-solo, django-ckeditor-5, django-cors-headers |
| Front-end ([besound-front](https://github.com/edealfonso/besound-front)) | Next.js, React, Sass, MediaRecorder API |
| Storage | Cloudflare R2 for audio files (django-storages, S3 API), whitenoise for static files |
| Infrastructure | Docker, Docker Compose, gunicorn, nginx (local) · Render (API), Neon (PostgreSQL), Vercel (front-end) |

## Quick start

Requires only [Docker](https://docs.docker.com/get-docker/) (with Compose v2).

```bash
git clone https://github.com/edealfonso/besound.git
cd besound
cp .env.example .env   # set DJANGO_DEBUG=1 to try it on http://localhost
docker compose up -d --build
docker compose exec web python manage.py createsuperuser
```

The API is at http://localhost:8000/v1/ and the admin at http://localhost:8000/admin/. If port 8000 is taken, use another one: `BESOUND_PORT=8080 docker compose up -d`.

To run the front-end against it, clone [besound-front](https://github.com/edealfonso/besound-front) and start it with `BACKEND_SERVER=http://localhost:8000/ npm run dev`.

Run the tests with:

```bash
docker compose exec web python manage.py test apps
```

## Deployment

Step-by-step guide (in Spanish) to deploy it for free with Render (API), Neon (PostgreSQL) and Cloudflare R2 (audio files), no credit card or server to manage: [docs/DESPLIEGUE.md](docs/DESPLIEGUE.md).

Alternative for your own server (VPS, Oracle Cloud…) with Docker Compose and Caddy, able to host several projects: [docs/DESPLIEGUE-SERVIDOR-PROPIO.md](docs/DESPLIEGUE-SERVIDOR-PROPIO.md).

## API

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/v1/home`, `/v1/about` | – | Page texts |
| GET / POST | `/v1/register` | – | Page texts / create a user |
| GET / POST | `/v1/login` | – | Page texts / get a token (`username` = email) |
| GET | `/v1/posts/list` | – | All sounds. With `?limit=20&offset=0`, a paginated response |
| GET / POST | `/v1/posts/new` | Token | Page texts / upload a sound (`title`, `audio`; max 10 MB) |
| DELETE | `/v1/posts/delete/<id>` | Token | Delete one of your sounds |

Authenticated requests send the header `Authorization: Token <token>`.

## Demo

**[besound.vercel.app](https://besound.vercel.app/)**

The API runs on Render's free plan, which sleeps after 15 minutes without visits: the first visit after a while can take up to a minute to load.

## My contribution

- In 2023, as the final project of my university master's degree, I designed and built besound: the Figma design, this Django REST API and the [Next.js front-end](https://github.com/edealfonso/besound-front).
- In 2026 I updated and improved it with the help of [Claude Code](https://claude.com/claude-code): Docker, security fixes, Django 5.2 LTS, upload validation, pagination, tests and a free deployment on Render, Neon and Cloudflare R2. See the [changelog](CHANGELOG.md).

## Roadmap

- [x] Deploy the API again so the online demo works
- [ ] CI with GitHub Actions: run the tests on every push
- [x] Store audio files in object storage (Cloudflare R2) instead of the server disk
- [ ] Move the fixed interface texts (buttons, instructions) from the admin to the front-end, keeping in the admin only the content that really changes
