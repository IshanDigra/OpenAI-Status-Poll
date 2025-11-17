"""
console_notifier.py

Console/stdout notifier for logging incidents.
"""

import logging
from .base_notifier import BaseNotifier

logger = logging.getLogger(__name__)


class ConsoleNotifier(BaseNotifier):
    """Outputs incident notifications to console/logs."""
    
    def notify(self, incident):
        """Print incident to console."""
        print("\n" + "="*80)
        print("🚨 NEW OPENAI STATUS INCIDENT 🚨")
        print("="*80)
        print(f"Title: {incident['title']}")
        print(f"Updated: {incident['updated']}")
        print(f"Link: {incident['link']}")
        print(f"\nSummary:\n{incident['summary']}")
        print("="*80 + "\n")
        
        logger.info(f"New incident: {incident['title']}")
