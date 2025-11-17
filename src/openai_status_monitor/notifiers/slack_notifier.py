"""
slack_notifier.py

Slack webhook notifier.
"""

import logging
import requests
from .base_notifier import BaseNotifier

logger = logging.getLogger(__name__)


class SlackNotifier(BaseNotifier):
    """Sends incident notifications to Slack via webhook."""
    
    def __init__(self, webhook_url):
        """
        Initialize Slack notifier.
        
        Args:
            webhook_url (str): Slack webhook URL
        """
        self.webhook_url = webhook_url
        logger.debug(f"SlackNotifier initialized")
    
    def notify(self, incident):
        """Send incident notification to Slack."""
        if not self.webhook_url:
            logger.warning("Slack webhook URL not configured. Skipping Slack notification.")
            return
        
        # Format Slack message
        message = {
            "text": f"🚨 *New OpenAI Status Incident* 🚨",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "🚨 OpenAI Status Update"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Title:*\n{incident['title']}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Updated:*\n{incident['updated']}"
                        }
                    ]
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Summary:*\n{incident['summary'][:500]}"  # Limit to 500 chars
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"<{incident['link']}|View Details>"
                    }
                }
            ]
        }
        
        try:
            response = requests.post(self.webhook_url, json=message, timeout=10)
            response.raise_for_status()
            logger.info(f"Slack notification sent successfully for: {incident['title']}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send Slack notification: {e}")
            raise
