"""
config.py

Loads configuration from environment variables using Python's
built-in 'os' module.
"""

import os
import logging

# --- Core Monitor Settings ---
FEED_URL = os.environ.get("FEED_URL", "https://status.openai.com/history.atom")
POLL_INTERVAL_SECONDS = int(os.environ.get("POLL_INTERVAL_SECONDS", "60"))

# --- State Management ---
STATE_BACKEND = os.environ.get("STATE_BACKEND", "file")
STATE_FILE_PATH = os.environ.get("STATE_FILE_PATH", "state.json")

# GCS State Backend
GCS_BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME", "")
GCS_STATE_BLOB_NAME = os.environ.get("GCS_STATE_BLOB_NAME", "openai_status_state.json")

# --- Notifiers ---
NOTIFIERS = os.environ.get("NOTIFIERS", "console").split(",")

# Slack Notifier
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL", "")

# Email Notifier
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
EMAIL_FROM = os.environ.get("EMAIL_FROM", "")
EMAIL_TO = os.environ.get("EMAIL_TO", "")

# --- Logging ---
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
