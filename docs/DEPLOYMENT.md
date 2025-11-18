# Deployment Guide

Comprehensive guide for deploying OpenAI Status Monitor in various environments.

## Prerequisites

- Python 3.11+
- Git
- Access to notification services (Slack, Email, etc.)
- Cloud account (optional, for cloud deployments)

## Deployment Options

### 1. GitHub Actions (Recommended)

#### Advantages

- ✅ Zero infrastructure cost
- ✅ Automatic execution every 5 minutes
- ✅ No server maintenance
- ✅ Built-in monitoring and logs
- ✅ Easy rollback

#### Setup Steps

**Step 1: Create Gist for State Storage**

1. Go to https://gist.github.com/
2. Click "Create secret gist" (not public!)
3. Filename: `state.json`
4. Content: `{}`
5. Click "Create secret gist"
6. Copy Gist ID from URL: `gist.github.com/username/{GIST_ID}`

**Step 2: Generate GitHub Personal Access Token**

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Name: `OpenAI Status Monitor`
4. Expiration: Choose based on security policy
5. Scopes: **Check only `gist`**
6. Click "Generate token"
7. **Copy the token immediately** (won't be shown again)

**Step 3: Get Slack Webhook URL**

1. Go to https://api.slack.com/apps
2. Create New App → "From scratch"
3. Name: `OpenAI Status Monitor`
4. Select your workspace
5. Click "Incoming Webhooks" → Toggle ON
6. Click "Add New Webhook to Workspace"
7. Select channel for notifications
8. Click "Allow"
9. Copy webhook URL

**Step 4: Add Repository Secrets**

1. Go to repository Settings
2. Navigate to Secrets and variables → Actions
3. Click "New repository secret"
4. Add these secrets:

| Name | Value |
|------|-------|
| `GIST_ID` | Your Gist ID from Step 1 |
| `GIST_TOKEN` | Your PAT from Step 2 |
| `SLACK_WEBHOOK_URL` | Your webhook from Step 3 |

**Step 5: Enable GitHub Actions**

1. Go to Settings → Actions → General
2. Under "Actions permissions":
   - Select "Allow all actions and reusable workflows"
3. Under "Workflow permissions":
   - Select "Read and write permissions"
4. Click "Save"

**Step 6: Test Workflow**

1. Go to Actions tab
2. Select "OpenAI Status Monitor (Gist-based State)"
3. Click "Run workflow" → "Run workflow"
4. Wait ~30 seconds
5. Click on the run to view logs
6. Verify success

**Troubleshooting:**

- **Workflow doesn't appear**: Check that `.github/workflows/monitor-gist.yml` exists
- **Permission errors**: Verify "Read and write permissions" is enabled
- **Gist errors**: Check GIST_ID and GIST_TOKEN are correct
- **No notifications**: Verify SLACK_WEBHOOK_URL secret

---

### 2. Local Development

#### Use Cases

- Development and testing
- Custom deployment environments
- Full control over execution

#### Setup

```bash
# Clone repository
git clone https://github.com/IshanDigra/OpenAI-Status-Poll.git
cd OpenAI-Status-Poll

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Test run
python -m src.openai_status_monitor --run-once
```

#### Running Continuously

```bash
# Run in foreground
python -m src.openai_status_monitor

# Run in background (Linux/Mac)
nohup python -m src.openai_status_monitor > monitor.log 2>&1 &

# Check logs
tail -f monitor.log
```

---

### 3. Google Cloud Run

#### Advantages

- Serverless deployment
- Auto-scaling
- Pay-per-use pricing
- Integrated with GCP services

#### Prerequisites

- Google Cloud account
- `gcloud` CLI installed
- GCS bucket for state storage

#### Setup

**Step 1: Create GCS Bucket**

```bash
gsutil mb gs://your-status-monitor-state/
```

**Step 2: Deploy to Cloud Run**

```bash
gcloud run deploy openai-status-monitor \
  --source . \
  --platform managed \
  --region us-central1 \
  --memory 256Mi \
  --cpu 1 \
  --timeout 60 \
  --set-env-vars FEED_URL=https://status.openai.com/history.atom \
  --set-env-vars STATE_BACKEND=gcs \
  --set-env-vars GCS_BUCKET_NAME=your-status-monitor-state \
  --set-env-vars NOTIFIERS=slack \
  --set-env-vars SLACK_WEBHOOK_URL=your-webhook-url
```

**Step 3: Set Up Cloud Scheduler**

```bash
# Create scheduler job
gcloud scheduler jobs create http openai-status-monitor \
  --schedule="*/5 * * * *" \
  --uri=YOUR_CLOUD_RUN_URL \
  --http-method=GET
```

---

### 4. Cron Job (Linux)

#### Setup

```bash
# Edit crontab
crontab -e

# Add entry (runs every 5 minutes)
*/5 * * * * cd /path/to/OpenAI-Status-Poll && /path/to/venv/bin/python -m src.openai_status_monitor --run-once >> /var/log/openai-monitor.log 2>&1
```

#### With Environment File

```bash
# Create wrapper script: /usr/local/bin/openai-monitor.sh
#!/bin/bash
set -a
source /path/to/OpenAI-Status-Poll/.env
set +a
cd /path/to/OpenAI-Status-Poll
/path/to/venv/bin/python -m src.openai_status_monitor --run-once

# Make executable
chmod +x /usr/local/bin/openai-monitor.sh

# Add to crontab
*/5 * * * * /usr/local/bin/openai-monitor.sh
```

---

### 5. Systemd Service (Linux)

#### Create Service File

```ini
# /etc/systemd/system/openai-status-monitor.service
[Unit]
Description=OpenAI Status Monitor
After=network.target

[Service]
Type=simple
User=monitor
Group=monitor
WorkingDirectory=/opt/openai-status-monitor
EnvironmentFile=/opt/openai-status-monitor/.env
ExecStart=/opt/openai-status-monitor/venv/bin/python -m src.openai_status_monitor
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### Enable and Start

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable openai-status-monitor

# Start service
sudo systemctl start openai-status-monitor

# Check status
sudo systemctl status openai-status-monitor

# View logs
sudo journalctl -u openai-status-monitor -f
```

---

### 6. Docker

#### Create Dockerfile

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ ./src/
COPY .env.example .env.example

# Run
CMD ["python", "-m", "src.openai_status_monitor", "--run-once"]
```

#### Build and Run

```bash
# Build image
docker build -t openai-status-monitor .

# Run with environment file
docker run --env-file .env openai-status-monitor

# Run with environment variables
docker run -e NOTIFIERS=console \
  -e STATE_BACKEND=file \
  openai-status-monitor

# Run continuously
docker run --env-file .env \
  openai-status-monitor \
  python -m src.openai_status_monitor
```

#### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  monitor:
    build: .
    env_file: .env
    restart: unless-stopped
    command: python -m src.openai_status_monitor
```

```bash
# Run with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## Configuration Best Practices

### Security

- **Never commit `.env` files** to version control
- Use **secrets management** (GitHub Secrets, GCP Secret Manager)
- **Rotate credentials** regularly
- Use **app passwords** for email (not account password)
- Apply **principle of least privilege**

### Reliability

- Set up **monitoring/alerts** for workflow failures
- Implement **logging** for troubleshooting
- Use **retries** for transient failures
- Test **failure scenarios**

### Performance

- Adjust **poll interval** based on requirements (default: 5 min)
- Monitor **GitHub Actions quota** (2,000 free minutes/month)
- Use **appropriate log level** (INFO for production)

## Cost Comparison

| Deployment | Monthly Cost | Maintenance | Complexity |
|------------|--------------|-------------|------------|
| GitHub Actions | $0 (free tier) | None | Low |
| Google Cloud Run | $0-5 | Low | Medium |
| Local Server | Variable | High | Low |
| Docker | Hosting cost | Medium | Medium |

## Monitoring

### GitHub Actions

- View runs: https://github.com/YOUR_USERNAME/YOUR_REPO/actions
- Set up email notifications: Settings → Notifications
- Enable workflow failure alerts

### Cloud Run

```bash
# View logs
gcloud run logs read openai-status-monitor

# Monitor metrics
gcloud monitoring dashboards list
```

### Local/Cron

```bash
# Check cron logs
grep CRON /var/log/syslog

# View application logs
tail -f /var/log/openai-monitor.log

# Check systemd status
systemctl status openai-status-monitor
```

## Scaling

### Monitor Multiple Services

Duplicate workflow or deployment for each service:

```yaml
# .github/workflows/monitor-github-status.yml
name: GitHub Status Monitor
on:
  schedule:
    - cron: '*/5 * * * *'
jobs:
  monitor:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - name: Run monitor
        env:
          FEED_URL: https://www.githubstatus.com/history.atom
          STATE_BACKEND: gist
          GIST_ID: ${{ secrets.GITHUB_STATUS_GIST_ID }}
          GIST_TOKEN: ${{ secrets.GIST_TOKEN }}
          NOTIFIERS: slack
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
        run: python -m src.openai_status_monitor --run-once
```

## Support

For deployment issues:
1. Check logs for error messages
2. Verify configuration
3. Review documentation
4. Open an issue on GitHub

---

**Need help? Open an issue with your deployment method and error details.**
