#!/usr/bin/env bash
# Render build script. Render runs this with the build command:  bash build.sh
# It needs DEBUG, SECRET_KEY and DATABASE_URL to be set in Render's Environment settings.
set -o errexit   # stop the build at the first error
set -o pipefail
set -o nounset

echo "==> Python version"
python --version

echo "==> Installing dependencies"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "==> Checking Django configuration"
python manage.py check --deploy

echo "==> Collecting static files (WhiteNoise)"
python manage.py collectstatic --noinput

echo "==> Applying database migrations to Neon"
python manage.py migrate --noinput

echo "==> Build finished"
