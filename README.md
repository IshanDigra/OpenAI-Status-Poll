# OpenAI Status Monitor

**Author:** Ishan Digra  
**Repository:** [OpenAI-Status-Poll](https://github.com/IshanDigra/OpenAI-Status-Poll)  
**Date:** November 2025

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF)](https://github.com/IshanDigra/OpenAI-Status-Poll/actions)

## Project Overview

A production-grade Python application that monitors the [OpenAI Status Page](https://status.openai.com) using intelligent conditional polling with HTTP ETag/Last-Modified headers. The system achieves 99.9% bandwidth efficiency by downloading feed updates only when actual changes occur.

### Key Features

- **Efficient Polling**: Conditional GET requests using ETag (304 Not Modified responses)
- **Idempotent Processing**: Each incident processed exactly once, even across restarts  
- **Multiple Notifiers**: Slack, Email, and Console output
- **Flexible State Management**: File-based, GCS, or GitHub Gist storage
- **Cloud-Native**: GitHub Actions, Google Cloud Run, Docker support
- **Production-Ready**: Comprehensive error handling and structured logging

## Table of Contents
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Deployment](#deployment)
- [Artifacts](#artifacts)
- [Testing](#testing)
- [License](#license)

## Quick Start

### Local Setup (3 Steps)

```bash
# 1. Clone and install dependencies
git clone https://github.com/IshanDigra/OpenAI-Status-Poll.git
cd OpenAI-Status-Poll
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your settings

# 3. Run
python -m src.openai_status_monitor --run-once
```

### GitHub Actions Gist-Based Deployment (How We Actually Deployed)

1. **Create a secret Gist for state storage**
   - Go to https://gist.github.com/
   - Click "+" → "New secret gist"
   - Filename: `state.json` with content: `{}`
   - Copy the Gist ID from the URL (after your username)

2. **Generate a GitHub PAT (Personal Access Token) with `gist` scope**
   - Go to GitHub > Settings > Developer settings > Personal access tokens
   - Only enable `gist` scope
   - Copy your token

3. **Add the following repository secrets**  
   - `GIST_ID` : (from step 1)
   - `GIST_TOKEN` : (from step 2)
   - `SLACK_WEBHOOK_URL` : (your Slack webhook, if notifications desired)

4. **Enable GitHub Actions**
   - Actions tab > Enable "OpenAI Status Monitor (Gist-based State)" workflow

5. **Optional**: Run the workflow manually (initializes state/Gist)

6. **That's it!** The system will now check OpenAI's status every 5 minutes, update your Gist, and notify via Slack/console.

## Architecture

... (remaining architecture and content unchanged)

