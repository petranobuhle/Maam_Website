# MAAM — Beyond the Silence

MAAM (Mwana Asingachemi Anofira Mumbereko) is an independent, youth-led mental health awareness and advocacy initiative. Its first community focus is young people in urban Zimbabwe; that starting point does not represent every African community.

The proverb means, “The baby that does not cry will die in the cradle.” MAAM's message is that people should feel safe expressing struggles and that communities have a responsibility to listen and create safe spaces.

MAAM is educational and advocacy-focused. It is not a diagnosis application, AI therapist, counselling or treatment service, or emergency response platform.

## Run locally

From PowerShell in the project folder:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

Open **http://127.0.0.1:8000/**. If no `.venv` exists, create one with `py -3.13 -m venv .venv` before installing requirements. Use the standard Python 3.13, not the free-threaded 3.13t build, which the PostgreSQL driver does not support.

To access content management, create a local administrator:

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

Then open **http://127.0.0.1:8000/admin/**.

## Prototype content and presentation notes

- Articles, translations, audio, campaigns and the support directory include seeded demonstration records. The website labels sample articles and campaigns; the sample support organisation/service is explicitly unverified, inactive and withheld from public listings.
- No real stories, verified support contacts, MAAM statistics, videos, or library downloads are included yet. Those sections use clear empty states rather than fabricated material.
- The hero and content artwork are original CSS layout placeholders, not photographs. Replace them with licensed images used with appropriate consent; add accurate alt text.
- Review all educational text and translations against credible sources before public launch. The article admin includes source fields.
- The volunteer and partnership forms collect contact details for follow-up. Do not enter health details or information about another person.
- Survey written answers are never included in public reporting. Public reports use preset choice answers only and suppress small groups.

## Content management

Use the Django admin to manage:

- Articles, topics, translations and audio resources
- Video/documentary/podcast metadata and transcripts
- Downloadable library resources
- Campaign records (the public Campaigns page was retired on 18 November 2026; the data is kept in the admin)
- Support organisations and services
- Stories: community stories (need consent), open-licence republished stories (need full credit), and external links (no copied text). See [docs/story-permissions.md](docs/story-permissions.md).

Only publish support entries after checking their official source and current contact details. Keep media permissions, story consent and editorial review outside the public-facing content itself.

The local media directory is `media/` and is served by Django only in development. Production media storage must be configured separately.

## Database and production

Local development uses SQLite at `db.sqlite3`. Production uses Neon PostgreSQL through the `DATABASE_URL` environment variable (see [docs/deployment.md](docs/deployment.md)). Never reset or replace the database to apply updates—use Django migrations.

Production needs a unique secret key, `DEBUG=False`, a strict host list, HTTPS, secure cookie/redirect settings, a production media-storage plan, backups, reviewed privacy/retention arrangements and verified launch content. Consult [docs/deployment.md](docs/deployment.md). This prototype has not been deployed.

## Checks and tests

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

## Project structure

- `maam_project/` — Django configuration and root routes
- `core/` — homepage, About, privacy and safeguarding
- `education/` — articles, audio, media, stories and resources
- `campaigns/` — campaign records (admin only; no public page)
- `directory/` — verified support organisations and services
- `research/` — voluntary surveys and aggregate reporting
- `analytics/` — staff-only aggregate dashboard
- `participation/` — volunteer and partnership inquiries
- `docs/` — architecture, schema, privacy and deployment notes
