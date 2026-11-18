"""Production settings behaviour. Each case loads settings in a fresh Python process."""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.management import call_command
from django.test import Client, SimpleTestCase, override_settings

PROJECT_DIR = Path(__file__).resolve().parent.parent
GOOD_KEY = "k" * 64  # test-only value, never used outside these subprocesses
# Made-up Neon-style connection string. Nothing connects to it; settings only parse it.
FAKE_NEON_URL = (
    "postgresql://maam_owner:not-a-real-password@ep-example-123456.eu-central-1.aws.neon.tech/maam?sslmode=require"
)

PROBE = """
import json
from django.conf import settings
print(json.dumps({
    "DEBUG": settings.DEBUG,
    "ALLOWED_HOSTS": settings.ALLOWED_HOSTS,
    "CSRF_TRUSTED_ORIGINS": settings.CSRF_TRUSTED_ORIGINS,
    "SECURE_PROXY_SSL_HEADER": getattr(settings, "SECURE_PROXY_SSL_HEADER", None),
    "SECURE_SSL_REDIRECT": settings.SECURE_SSL_REDIRECT,
    "SESSION_COOKIE_SECURE": settings.SESSION_COOKIE_SECURE,
    "CSRF_COOKIE_SECURE": settings.CSRF_COOKIE_SECURE,
    "SECURE_HSTS_SECONDS": settings.SECURE_HSTS_SECONDS,
    "STATIC_BACKEND": settings.STORAGES["staticfiles"]["BACKEND"],
    "MIDDLEWARE": settings.MIDDLEWARE,
    "DB": {k: v for k, v in settings.DATABASES["default"].items() if k != "PASSWORD"},
    "DB_HAS_PASSWORD": bool(settings.DATABASES["default"].get("PASSWORD")),
    "ADMIN_URL": settings.ADMIN_URL,
}, default=str))
"""


def load_settings(**env):
    # Empty strings stop python-dotenv from filling these values from a local .env file.
    base = {
        "DEBUG": "",
        "SECRET_KEY": "",
        "ALLOWED_HOSTS": "",
        "CSRF_TRUSTED_ORIGINS": "",
        "RENDER_EXTERNAL_HOSTNAME": "",
        "SECURE_SSL_REDIRECT": "",
        "SECURE_HSTS_SECONDS": "",
        "TRUST_PROXY_SSL_HEADER": "",
        "DATABASE_URL": FAKE_NEON_URL,
        "ALLOW_SQLITE_IN_PRODUCTION": "",
        "ADMIN_URL": "",
        "RESEND_API_KEY": "",
    }
    base.update(env)
    process_env = {**os.environ, **base, "DJANGO_SETTINGS_MODULE": "maam_project.settings"}
    return subprocess.run(
        [sys.executable, "-c", "import django; django.setup()\n" + PROBE],
        cwd=PROJECT_DIR,
        env=process_env,
        capture_output=True,
        text=True,
        timeout=60,
    )


class ProductionSettingsTests(SimpleTestCase):
    def test_debug_is_off_by_default_and_requires_a_secret_key(self):
        result = load_settings()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Set SECRET_KEY", result.stderr)

    def test_placeholder_or_short_secret_key_is_rejected_in_production(self):
        for key in ("replace-with-a-random-local-secret", "django-insecure-" + "x" * 60, "short"):
            with self.subTest(key=key[:20]):
                result = load_settings(SECRET_KEY=key)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("placeholder or too short", result.stderr)

    def test_render_production_settings(self):
        result = load_settings(SECRET_KEY=GOOD_KEY, RENDER_EXTERNAL_HOSTNAME="maam-test.onrender.com")
        self.assertEqual(result.returncode, 0, result.stderr)
        values = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertFalse(values["DEBUG"])
        self.assertEqual(values["ALLOWED_HOSTS"], ["maam-test.onrender.com"])
        self.assertEqual(values["CSRF_TRUSTED_ORIGINS"], ["https://maam-test.onrender.com"])
        self.assertEqual(values["SECURE_PROXY_SSL_HEADER"], ["HTTP_X_FORWARDED_PROTO", "https"])
        self.assertTrue(values["SECURE_SSL_REDIRECT"])
        self.assertTrue(values["SESSION_COOKIE_SECURE"])
        self.assertTrue(values["CSRF_COOKIE_SECURE"])
        self.assertEqual(values["SECURE_HSTS_SECONDS"], 0)
        self.assertEqual(values["STATIC_BACKEND"], "whitenoise.storage.CompressedManifestStaticFilesStorage")
        self.assertEqual(
            values["MIDDLEWARE"][:2],
            ["django.middleware.security.SecurityMiddleware", "whitenoise.middleware.WhiteNoiseMiddleware"],
        )

    def test_production_requires_a_database_url(self):
        result = load_settings(SECRET_KEY=GOOD_KEY, DATABASE_URL="")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Set DATABASE_URL", result.stderr)

    def test_neon_connection_string_is_read_securely(self):
        result = load_settings(SECRET_KEY=GOOD_KEY)
        self.assertEqual(result.returncode, 0, result.stderr)
        values = json.loads(result.stdout.strip().splitlines()[-1])
        db = values["DB"]
        self.assertEqual(db["ENGINE"], "django.db.backends.postgresql")
        self.assertEqual(db["HOST"], "ep-example-123456.eu-central-1.aws.neon.tech")
        self.assertEqual(db["NAME"], "maam")
        self.assertEqual(db["USER"], "maam_owner")
        self.assertTrue(values["DB_HAS_PASSWORD"])
        self.assertEqual(db["OPTIONS"]["sslmode"], "require")
        self.assertTrue(db["CONN_HEALTH_CHECKS"])
        self.assertEqual(db["CONN_MAX_AGE"], 60)
        self.assertNotIn("not-a-real-password", result.stdout + result.stderr)

    def test_admin_address_can_be_moved(self):
        result = load_settings(SECRET_KEY=GOOD_KEY, ADMIN_URL="/maam-staff-7q4/")
        values = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertEqual(values["ADMIN_URL"], "maam-staff-7q4/")

    def test_custom_domain_is_added_alongside_render_host(self):
        result = load_settings(
            SECRET_KEY=GOOD_KEY,
            RENDER_EXTERNAL_HOSTNAME="maam-test.onrender.com",
            ALLOWED_HOSTS="www.example.org",
            CSRF_TRUSTED_ORIGINS="https://www.example.org",
        )
        values = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertEqual(values["ALLOWED_HOSTS"], ["www.example.org", "maam-test.onrender.com"])
        self.assertEqual(
            values["CSRF_TRUSTED_ORIGINS"],
            ["https://www.example.org", "https://maam-test.onrender.com"],
        )

    def test_csrf_origin_without_scheme_is_rejected(self):
        result = load_settings(SECRET_KEY=GOOD_KEY, CSRF_TRUSTED_ORIGINS="www.example.org")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("need a scheme", result.stderr)

    def test_local_development_still_works_with_debug_on(self):
        result = load_settings(DEBUG="True", DATABASE_URL="")
        self.assertEqual(result.returncode, 0, result.stderr)
        values = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertTrue(values["DEBUG"])
        self.assertIn("127.0.0.1", values["ALLOWED_HOSTS"])
        self.assertIsNone(values["SECURE_PROXY_SSL_HEADER"])
        self.assertFalse(values["SECURE_SSL_REDIRECT"])
        self.assertEqual(values["STATIC_BACKEND"], "django.contrib.staticfiles.storage.StaticFilesStorage")
        self.assertEqual(values["DB"]["ENGINE"], "django.db.backends.sqlite3")
        self.assertEqual(values["ADMIN_URL"], "admin/")


class ProductionStaticFilesTests(SimpleTestCase):
    """collectstatic + WhiteNoise with DEBUG off, using a temporary folder."""

    def test_collectstatic_builds_hashed_compressed_files_served_by_whitenoise(self):
        with tempfile.TemporaryDirectory() as static_root, override_settings(
            DEBUG=False,
            STATIC_ROOT=static_root,
            STORAGES={
                "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
                "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
            },
        ):
            call_command("collectstatic", interactive=False, verbosity=0)
            root = Path(static_root)
            self.assertTrue((root / "staticfiles.json").exists())
            hashed_css = staticfiles_storage.url("css/styles.css")
            self.assertRegex(hashed_css, r"^/static/css/styles\.[0-9a-f]{12}\.css$")
            self.assertTrue((root / "css" / "styles.css.gz").exists())

            client = Client()
            for path in (
                "css/styles.css",
                "js/site.js",
                "favicon.svg",
                "images/homepage-maam-hero.jpg",
                "images/about-highfield-harare-dawn.jpg",
                "images/resources/friendship-bench-harare-costa-juta.jpg",
                "images/flags/zw.svg",
            ):
                with self.subTest(path=path):
                    response = client.get(staticfiles_storage.url(path))
                    self.assertEqual(response.status_code, 200)
                    self.assertIn("max-age=315360000", response.get("Cache-Control", ""))
                    response.close()

            gzip_response = client.get(hashed_css, HTTP_ACCEPT_ENCODING="gzip")
            self.assertEqual(gzip_response.get("Content-Encoding"), "gzip")
            gzip_response.close()

            # A page rendered with DEBUG off links to the hashed CSS file.
            page = client.get("/about/", secure=True)
            self.assertContains(page, hashed_css)
