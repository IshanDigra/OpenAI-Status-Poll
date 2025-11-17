# 🚀 Quick Start Guide

Get your OpenAI Status Monitor running in **under 5 minutes**!

## 🎯 Choose Your Deployment Method

### Option 1: GitHub Actions (Easiest - **Recommended**) ⭐

**Zero infrastructure needed! Runs automatically on GitHub's servers.**

```bash
# 1. Add Slack webhook to repository secrets
#    Go to: Settings → Secrets → Actions → New repository secret
#    Name: SLACK_WEBHOOK_URL
#    Value: https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# 2. Enable GitHub Actions
#    Go to: Settings → Actions → General → Allow all actions

# 3. Manually run the workflow once to test
#    Go to: Actions → "OpenAI Status Monitor (Commit-based State)" → Run workflow

# That's it! 🎉
# The monitor now runs automatically every 5 minutes.
```

**Get Slack Webhook URL:**
1. Go to https://api.slack.com/apps
2. Create New App → From scratch
3. Enable "Incoming Webhooks"
4. Add New Webhook to Workspace
5. Copy the webhook URL

---

### Option 2: Run Locally

```bash
# 1. Clone and install
git clone https://github.com/IshanDigra/OpenAI-Status-Poll.git
cd OpenAI-Status-Poll
pip install -r requirements.txt

# 2. Configure (for testing, just use console)
cp .env.example .env
# Edit .env: Set NOTIFIERS=console

# 3. Run once to test
python -m src.openai_status_monitor --run-once

# 4. Run continuously (keeps checking every 60 seconds)
python -m src.openai_status_monitor
```

---

### Option 3: Docker (Coming Soon)

```bash
# Build image
docker build -t openai-status-monitor .

# Run with environment variables
docker run -e NOTIFIERS=console -e STATE_BACKEND=file \
  openai-status-monitor --run-once
```

---

## 🔔 Notification Setup

### Console (Default)
```bash
export NOTIFIERS=console
```
Outputs to stdout - perfect for testing.

### Slack (Recommended)
```bash
export NOTIFIERS=slack
export SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

### Email (Gmail)
```bash
export NOTIFIERS=email
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USER=your-email@gmail.com
export SMTP_PASSWORD=your-app-password  # Not your regular password!
export EMAIL_FROM=your-email@gmail.com
export EMAIL_TO=recipient@example.com
```

**Gmail App Password:**
1. Go to https://myaccount.google.com/apppasswords
2. Generate app password for "Mail"
3. Use that as `SMTP_PASSWORD`

### Multiple Notifiers
```bash
export NOTIFIERS=console,slack,email
```

---

## 📁 State Management

### Local File (Default)
```bash
export STATE_BACKEND=file
export STATE_FILE_PATH=state.json
```
Perfect for local development and GitHub Actions commit-based mode.

### Google Cloud Storage
```bash
export STATE_BACKEND=gcs
export GCS_BUCKET_NAME=my-bucket
export GCS_STATE_BLOB_NAME=openai_status_state.json
```
For multi-instance deployments.

---

## ✅ Verify It's Working

### Test 1: Check Feed Access
```bash
curl -I https://status.openai.com/history.atom
# Should return: HTTP/2 200
```

### Test 2: Run Once
```bash
export NOTIFIERS=console
python -m src.openai_status_monitor --run-once
```
Should output: "Check complete. No new incidents." (unless there's an active incident)

### Test 3: Check State File
```bash
cat state.json
```
Should contain ETag and list of processed incident IDs.

---

## 🐛 Troubleshooting

### "No module named 'feedparser'"
```bash
pip install -r requirements.txt
```

### "Feed not modified (304)"
This is **good**! It means the efficient polling is working.

### "No notifiers configured"
```bash
export NOTIFIERS=console  # Enable at least one notifier
```

### GitHub Actions not running
- Check: Settings → Actions → General → Actions permissions
- Enable: "Allow all actions and reusable workflows"

---

## 📊 What to Expect

### First Run
```
INFO - Starting OpenAI Status Monitor
INFO - Feed URL: https://status.openai.com/history.atom
INFO - Run Mode: One-time
INFO - Using file-based state management: state.json
INFO - Enabling console notifier
INFO - Checking feed: https://status.openai.com/history.atom
INFO - Feed updated (200 OK). Processing 30 entries.
INFO - No new incidents detected.
INFO - Check complete. No new incidents.
```

### When New Incident Occurs
```
INFO - Found 1 new incident(s).

================================================================================
🚨 NEW OPENAI STATUS INCIDENT 🚨
================================================================================
Title: Elevated API Error Rates
Updated: 2024-11-17T10:30:00Z
Link: https://status.openai.com/incidents/abc123

Summary:
We are investigating elevated error rates affecting the ChatGPT API...
================================================================================

INFO - Slack notification sent successfully
```

---

## ⏱️ Scheduling

### Cron (Linux/Mac)
```bash
# Check every 5 minutes
*/5 * * * * cd /path/to/OpenAI-Status-Poll && python -m src.openai_status_monitor --run-once
```

### Windows Task Scheduler
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily, repeat every 5 minutes
4. Action: Start a program
5. Program: `python`
6. Arguments: `-m src.openai_status_monitor --run-once`
7. Start in: `C:\path\to\OpenAI-Status-Poll`

### GitHub Actions (Recommended)
Already configured! Just enable the workflow.

---

## 🔗 Useful Commands

```bash
# Test with debug logging
export LOG_LEVEL=DEBUG
python -m src.openai_status_monitor --run-once

# Check version
python -c "from src.openai_status_monitor import __version__; print(__version__)"

# View logs (GitHub Actions)
gh run list --workflow=monitor-commit.yml
gh run view <run-id> --log

# Clear state (start fresh)
rm state.json
```

---

## 🎓 Next Steps

1. ✅ Get it running locally with console output
2. ✅ Set up Slack notifications
3. ✅ Deploy to GitHub Actions
4. ✅ Monitor for a week
5. 🚀 Scale to monitor multiple status pages!

---

**Need help?** Open an issue: https://github.com/IshanDigra/OpenAI-Status-Poll/issues
