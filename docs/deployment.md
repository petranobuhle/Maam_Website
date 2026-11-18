# Local and production configuration

## Local development

Use SQLite. From PowerShell in the project directory:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

Open `http://127.0.0.1:8000/`. If `.env` already exists, preserve it rather than overwriting it.

## PostgreSQL

For production, use `DATABASE_URL` (see "Database: Neon PostgreSQL" below). The older `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` and `DB_PORT` variables still work when `DATABASE_URL` is not set. The `psycopg` driver is included in `requirements.txt`.

**Local Python:** use the **standard** Python 3.13, not the experimental "free-threaded" 3.13t build. The PostgreSQL driver does not support 3.13t. Create the environment with `py -3.13 -m venv .venv`.

## Environment settings (prepared in Batch 1, 18 November 2026)

`DEBUG` is **off by default**. Local development turns it on through `.env` (`DEBUG=True`).

| Variable | Production value | Notes |
|---|---|---|
| `DEBUG` | `False` | Off is also the default if the variable is missing. |
| `SECRET_KEY` | Long random value | Required. Startup fails if it is missing, a placeholder, or shorter than 50 characters. |
| `ALLOWED_HOSTS` | Your custom domain(s), comma-separated | Render's `RENDER_EXTERNAL_HOSTNAME` is added automatically. |
| `CSRF_TRUSTED_ORIGINS` | `https://your-domain` | Must include `https://`. `https://<RENDER_EXTERNAL_HOSTNAME>` is added automatically. |
| `TRUST_PROXY_SSL_HEADER` | (leave unset) | Defaults to on when `DEBUG` is off, so Django trusts Render's `X-Forwarded-Proto` header. |
| `SECURE_SSL_REDIRECT` | (leave unset) | Defaults to on when `DEBUG` is off. |
| `SECURE_HSTS_SECONDS` | `0` | Raise it only after HTTPS works on the final domain. |

To generate a secret key, run this on your own computer and paste the result into Render's Environment settings. Never commit it:

```powershell
.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_urlsafe(64))"
```

`gunicorn` is included in `requirements.txt` for Render (Linux). The Render start command is configured in the deploy batch.

## Static files (prepared in Batch 2)

- **WhiteNoise** serves CSS, JavaScript and images when `DEBUG` is off. The middleware sits directly after `SecurityMiddleware`.
- **Production storage:** `whitenoise.storage.CompressedManifestStaticFilesStorage`.
  - Every file gets a fingerprinted name (e.g. `styles.5d3672732e11.css`), a gzip copy and a one-year `immutable` cache header.
  - Local development (`DEBUG=True`) keeps Django's plain storage, so you don't need `collectstatic` on your laptop.
- **`WHITENOISE_MANIFEST_STRICT = False`:** a mistyped image path entered in the admin falls back to a plain URL instead of crashing the page.
- **Build step:** Render must run `collectstatic` during the build. It writes to `staticfiles/`, which is not committed:

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

## Database: Neon PostgreSQL (prepared in Batch 3)

- **Production:** set `DATABASE_URL` to Neon's connection string. If `DEBUG` is off and `DATABASE_URL` is missing, the site refuses to start, because Render's disk is wiped on every deploy and a SQLite file there would lose everything.
- **Local development:** leave `DATABASE_URL` unset to keep using SQLite (`db.sqlite3`).
- **Connection settings:** SSL is required by default (`DB_SSL_REQUIRE`). Connections are reused for 60 seconds (`DB_CONN_MAX_AGE`) and health-checked, because Neon pauses idle databases.
- **Content:** every article, translation, story, resource, image credit and support listing is created by migrations. `python manage.py migrate` on an empty Neon database recreates all 82 content rows. This was tested on a real PostgreSQL 16 server, and all 20 tables matched SQLite exactly.

### Create the Neon database (your Neon account)

1. Sign in at https://neon.com and create a **project**, for example `maam`. Choose the region closest to your Render region.
2. Open **Connect**. Choose the **direct** connection (turn off "Connection pooling"). Copy the connection string. It looks like `postgresql://USER:PASSWORD@ep-xxxx.REGION.aws.neon.tech/neondb?sslmode=require`.
3. In Render, open your service, then **Environment**, and add `DATABASE_URL` with that value. **Never** paste it into a file in this project.
4. Render's build or start step runs `python manage.py migrate` (configured in the deploy batch).

### Backups and free-plan limits

- **Free plan (Neon FAQ, checked November 2026):** 1 GB storage per project and 100 compute-hours per month. Writes fail if storage is full; there are no surprise charges.
- **Idle pauses:** the database pauses when idle, so the first visit after a quiet period can take a moment longer.
- **Restore history is short on the free plan.** Do not rely on it as a backup. Check the current window in Neon's console.
- **Monthly backup routine (recommended):** run this on your laptop and store the file somewhere private, not in this project folder:

```powershell
$env:DATABASE_URL = "<paste Neon connection string>"
.\.venv\Scripts\python.exe manage.py dumpdata --natural-foreign --natural-primary --exclude contenttypes --exclude auth.permission --exclude sessions --indent 2 -o maam-backup-YYYY-MM-DD.json
Remove-Item Env:DATABASE_URL
```

The backup contains volunteer and partnership submissions, so treat it as private personal data. Store it encrypted or in a private location, and delete old copies under your retention plan.

## Admin account (prepared in Batch 3)

- **Shell access:** Render's free plan has **no Shell or SSH access**, so create the first admin account **from your laptop**, connected directly to Neon. The password is typed interactively. It is never stored in code, files or Render settings, only as a secure hash in the database.
- **Command** (after the first successful deploy has run the migrations):

```powershell
$env:DATABASE_URL = "<paste Neon connection string>"
.\.venv\Scripts\python.exe manage.py createsuperuser
Remove-Item Env:DATABASE_URL
```

- **Password:** use a unique passphrase of at least **12 characters**. The site now rejects shorter ones.
- **Optional private admin address:** set `ADMIN_URL` in Render, e.g. `maam-staff-7q4/`, to move the admin away from `/admin/`. Bookmark the new address.
- **Sign-in sessions** expire after 8 hours.

## Staff email notifications: Resend (prepared in Batch 3)

- **What it does:** each successful Volunteer or Partnership form sends **one** email to `NOTIFICATION_EMAIL` (default `mahwadupetra@gmail.com`).
- **What the email contains:** only the form type, time, reference ID and an admin link. **Names, email addresses and messages are deliberately not included.** Read submissions in the password-protected admin.
- **Why the HTTPS API:** Render's free plan blocks SMTP ports 25, 465 and 587, so MAAM uses Resend's HTTPS API, not SMTP.
- **Duplicate prevention:** an atomic database claim, plus a Resend `Idempotency-Key` per attempt, plus redirect-after-submit.
- **Statuses in the admin:**
  - *Accepted by Resend (delivery not confirmed)*
  - *Failed*
  - *Not sent – notifications switched off*
- **Retrying:** use the admin action **"Retry staff email notification"** for failed or switched-off items. It never resends accepted ones.
- **If email fails:** the visitor still sees the normal "received" message, because their submission is safely saved. Logs record only the reference ID and HTTP status.

### What you must do in Resend

1. Create a Resend account **using `mahwadupetra@gmail.com`**.
2. Create an **API key** with "Sending access" only. Add it in Render as `RESEND_API_KEY`. Never put it in a file.
3. **Sender address:**
   - Without your own domain, `onboarding@resend.dev` (the default `RESEND_FROM_EMAIL`) can only send to the email address on your Resend account. That is enough for staff notifications to yourself, but Resend describes it as a testing address.
   - For reliable long-term use, verify a domain you own at resend.com/domains: add the DNS records Resend shows you. Then set `RESEND_FROM_EMAIL`, e.g. `MAAM Website <notifications@your-domain>`.
4. After deploying, submit one test form and confirm the email arrives. Check the spam folder the first time.

## Render web service settings (Deployment Phase 1)

Tested with a full simulated build: `bash build.sh` with `DEBUG=False` against an empty PostgreSQL 16 database. Static files were collected, every migration ran, all 82 content rows matched, and every page and static file was served over HTTPS.

| Render field | Value |
|---|---|
| Language | Python 3 |
| Branch | `main` |
| Root Directory | (leave blank) |
| Build Command | `bash build.sh` |
| Start Command | `gunicorn maam_project.wsgi:application` |
| Instance Type | **Free** |
| Region | Frankfurt (EU Central) is closest to Zimbabwe. Create the Neon project in the matching region (AWS Europe Central / Frankfurt). |
| Health Check Path | (leave blank) |

- **`build.sh`:** installs packages, runs `check --deploy`, then `collectstatic`, then `migrate`. Migrations run during the build because Render's separate pre-deploy step may not be available on free instances.
- **`gunicorn.conf.py`:** gunicorn loads it automatically. It listens on Render's `PORT`, runs 2 workers (override with `WEB_CONCURRENCY`) and has a 60-second timeout.

### Environment variables to add in Render (Environment tab)

| Key | Value | When |
|---|---|---|
| `PYTHON_VERSION` | `3.13` | Required. Pins standard Python 3.13 (latest patch). Render's default is older. |
| `DEBUG` | `False` | Required. Off is also the default, but set it explicitly. |
| `SECRET_KEY` | Generate on your laptop (command above) | Required. 50+ characters. Paste only into Render, never into chat or files. |
| `DATABASE_URL` | Neon **direct** connection string | Required. |
| `RESEND_API_KEY` | Resend API key | Add later, when you approve the first email test. Without it, notifications are switched off. |
| `NOTIFICATION_EMAIL` | `mahwadupetra@gmail.com` | Optional (this is already the default). |
| `RESEND_FROM_EMAIL` | `MAAM Website <onboarding@resend.dev>` | Optional (default). Change it after verifying your own domain. |
| `ADMIN_URL` | e.g. `maam-staff-7q4/` | Optional private admin address. |
| `ALLOWED_HOSTS` / `CSRF_TRUSTED_ORIGINS` | (leave unset) | Only needed for a custom domain. The `*.onrender.com` address is added automatically. |
| `SECURE_HSTS_SECONDS` | (leave unset) | Only after HTTPS has been confirmed on the final domain. |

### Free-plan behaviour

- **Sleeping:** the service sleeps after 15 minutes without visitors. The next visit wakes it, which takes about a minute.
- **Monthly hours:** 750 free instance hours per workspace each month. That is enough for one service; a sleeping service uses none.
- **Shell access:** none on the free plan. Create the admin account from your laptop (see "Admin account").

## Production checklist

- Set a unique secret `SECRET_KEY`; startup fails if `DEBUG=False` and no key is configured.
- Set `DEBUG=False` and a strict `ALLOWED_HOSTS`.
- Serve only over HTTPS, enable secure cookies and configure SSL redirect.
- Set `SECURE_HSTS_SECONDS` only after HTTPS is confirmed throughout the host. Include subdomains/preload only when the domain setup is ready.
- Run `manage.py check --deploy` and resolve all warnings.
- Run `manage.py migrate`; never reset or overwrite an existing database.
- Run `manage.py collectstatic` and configure static hosting.
- Configure persistent, access-controlled media storage and file-size limits; Django serves uploaded media only in local debug mode.
- Configure backups, privacy/retention, logging, administrator access, and incident response.
- Replace demonstration content with editorially reviewed, sourced material and verified support details.

This project has not been deployed publicly.
