# Architecture

MAAM remains a modular Django project. SQLite is the local-development database; production PostgreSQL is configurable via environment variables. No frontend framework or large JavaScript dependency is used.

## Apps

- `core`: homepage, About, privacy, safeguarding and contact
- `education`: topics, articles and translations, audio, media, stories and downloadable resources
- `campaigns`: country-specific campaigns and attached materials
- `directory`: support organisations/services and verification metadata
- `research`: consent-based surveys and privacy-protected aggregate insights
- `analytics`: staff-only aggregate dashboard
- `participation`: volunteer and partnership forms
- `accounts`: user profiles

Content is managed through Django admin. Public views read published content from the database, filter by the active country and require explicit publication/verification state. The seeded article and campaign content is labelled demonstration content; seeded support details are unverified and not publicly listed.

## Media and static files

Small custom CSS and JavaScript files are served from `static/`. The interface uses CSS-drawn visual placeholders until licensed, consented photography is supplied. Admin-managed resource files use `MEDIA_ROOT`; Django serves these only in development. Production requires separately configured media storage and static-file hosting.

## Migrations

Schema and seed-status changes use additive Django migrations. Existing migration files and records are retained. Apply changes with `manage.py migrate`; do not reset the database.
