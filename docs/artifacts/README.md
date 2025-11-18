# Artifacts

This directory contains screenshots and visual documentation demonstrating the OpenAI Status Monitor in action.

## Required Artifacts

Please add the following screenshots to complete the assignment documentation:

### 1. workflow_success.png
**What to capture:**
- GitHub Actions workflow run page
- Show successful completion (green checkmark)
- Expand "Run status monitor" step to show logs
- Highlight key log lines:
  - "Checking feed: https://status.openai.com/history.atom"
  - "Feed updated (200 OK)" or "Feed not modified (304)"
  - "Check complete"

**How to capture:**
1. Go to: Actions → Select a successful workflow run
2. Click on the "monitor" job
3. Expand the "Run status monitor" step
4. Take screenshot showing the logs
5. Save as `workflow_success.png`

---

### 2. slack_notification.png
**What to capture:**
- Slack channel with notification message
- Show formatted incident alert with:
  - 🚨 OpenAI Status Update header
  - Incident title
  - Timestamp
  - Summary text
  - "View Details" link

**How to capture:**
1. Wait for a real incident OR clear state.json to simulate
2. Open your Slack channel
3. Locate the notification message
4. Take screenshot of the formatted message
5. Save as `slack_notification.png`

**To simulate for screenshot:**
```bash
# Delete or edit state.json in your Gist to trigger notifications
# Run workflow manually
```

---

### 3. state_json.png
**What to capture:**
- Your GitHub Gist page
- Show `state.json` file contents
- Display the JSON structure with:
  - `etag` field
  - `last_modified` field  
  - `processed_incident_ids` array

**How to capture:**
1. Go to your Gist: https://gist.github.com/{username}/{GIST_ID}
2. Open `state.json` file
3. Ensure JSON is visible and formatted
4. Take screenshot showing the structure
5. Save as `state_json.png`

**Example state.json:**
```json
{
  "etag": "W/\"abc123def456\"",
  "last_modified": "Mon, 17 Nov 2025 19:00:00 GMT",
  "processed_incident_ids": [
    "incident_123",
    "incident_124",
    "incident_125"
  ]
}
```

---

### 4. logs_example.png
**What to capture:**
- GitHub Actions workflow logs showing a complete monitoring cycle
- Key elements to show:
  - Startup message
  - Feed checking
  - HTTP response (200 or 304)
  - Processing summary
  - Completion message

**How to capture:**
1. Go to Actions → Recent workflow run
2. Expand "Run status monitor" step
3. Capture logs showing complete cycle
4. Save as `logs_example.png`

**Example log output:**
```
2025-11-17 19:05:35 - INFO - Starting OpenAI Status Monitor
2025-11-17 19:05:35 - INFO - Feed URL: https://status.openai.com/history.atom
2025-11-17 19:05:35 - INFO - Run Mode: One-time
2025-11-17 19:05:35 - INFO - Using gist-based state management
2025-11-17 19:05:35 - INFO - Enabling console notifier
2025-11-17 19:05:35 - INFO - Enabling Slack notifier
2025-11-17 19:05:35 - INFO - Checking feed: https://status.openai.com/history.atom
2025-11-17 19:05:36 - INFO - Feed not modified (304 Not Modified). No updates.
2025-11-17 19:05:36 - INFO - Check complete. No new incidents.
```

---

## File Naming Convention

Please use exactly these filenames:
- `workflow_success.png`
- `slack_notification.png`
- `state_json.png`
- `logs_example.png`

## Image Requirements

- **Format**: PNG
- **Size**: Reasonable resolution (1200-1920px width recommended)
- **Quality**: Clear and readable text
- **Content**: Actual working system (not mockups)

## Adding Your Screenshots

1. Take screenshots following above guidelines
2. Save with exact filenames
3. Place in this directory (`docs/artifacts/`)
4. Commit and push:
   ```bash
   git add docs/artifacts/*.png
   git commit -m "docs: add system artifacts and screenshots"
   git push origin implementation
   ```

## Verification

After adding screenshots, verify they appear correctly in README.md.

The README references these images as:
```markdown
![Description](docs/artifacts/filename.png)
```

Ensure the paths are correct and images render on GitHub.

---

**Note**: These screenshots are crucial for assignment evaluation as they demonstrate the working system.
