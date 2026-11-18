"""Gunicorn settings for Render. Gunicorn loads this file automatically from the project folder.

Start command on Render:  gunicorn maam_project.wsgi:application
"""
import os

# Render tells the app which port to listen on through the PORT variable (10000 by default).
bind = f"0.0.0.0:{os.environ.get('PORT', '10000')}"

# Render's free instance has 512 MB of memory; 2 workers fit comfortably. Override with WEB_CONCURRENCY.
workers = int(os.environ.get("WEB_CONCURRENCY", "2"))

# Allow time for a sleeping Neon database to wake and for the Resend call (10-second limit).
timeout = 60
graceful_timeout = 30

# Send request and error logs to Render's Logs tab. Request lines contain paths only, no form contents.
accesslog = "-"
errorlog = "-"
loglevel = "info"
