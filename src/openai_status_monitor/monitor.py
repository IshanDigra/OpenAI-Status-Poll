"""
monitor.py

Core monitoring logic with conditional polling using ETag/Last-Modified.
"""

import logging
import feedparser
from . import config
from .parser import parse_feed

logger = logging.getLogger(__name__)


class StatusMonitor:
    """Monitors OpenAI status feed with efficient conditional polling."""
    
    def __init__(self, state_manager, notifiers):
        """
        Initialize the monitor.
        
        Args:
            state_manager: State manager instance (file or GCS)
            notifiers: List of notifier instances
        """
        self.state_manager = state_manager
        self.notifiers = notifiers
        self.feed_url = config.FEED_URL
        
    def check_for_updates(self):
        """
        Check feed for updates using conditional GET.
        
        Returns:
            Tuple of (new_incidents_found: bool, incident_count: int)
        """
        logger.info(f"Checking feed: {self.feed_url}")
        
        # Load current state
        state = self.state_manager.load_state()
        processed_ids = set(state.get('processed_incident_ids', []))
        etag = state.get('etag')
        last_modified = state.get('last_modified')
        
        # Perform conditional GET request
        logger.debug(f"Using ETag: {etag}, Last-Modified: {last_modified}")
        
        feed = feedparser.parse(
            self.feed_url,
            etag=etag,
            modified=last_modified
        )
        
        # Check if feed was modified
        if feed.status == 304:
            logger.info("Feed not modified (304 Not Modified). No updates.")
            return False, 0
        
        if feed.status != 200:
            logger.error(f"Failed to fetch feed. HTTP Status: {feed.status}")
            return False, 0
        
        logger.info(f"Feed updated (200 OK). Processing {len(feed.entries)} entries.")
        
        # Parse incidents
        incidents = parse_feed(feed)
        
        # Find new incidents
        new_incidents = [inc for inc in incidents if inc['id'] not in processed_ids]
        
        if new_incidents:
            logger.info(f"Found {len(new_incidents)} new incident(s).")
            
            # Notify about new incidents
            for incident in new_incidents:
                self._notify_incident(incident)
                processed_ids.add(incident['id'])
        else:
            logger.info("No new incidents detected.")
        
        # Update state with new HTTP validators and processed IDs
        new_state = {
            'etag': feed.get('etag'),
            'last_modified': feed.get('modified'),
            'processed_incident_ids': list(processed_ids)
        }
        
        self.state_manager.save_state(new_state)
        logger.debug("State saved successfully.")
        
        return len(new_incidents) > 0, len(new_incidents)
    
    def _notify_incident(self, incident):
        """Send notifications for a new incident."""
        for notifier in self.notifiers:
            try:
                notifier.notify(incident)
            except Exception as e:
                logger.error(f"Notifier {notifier.__class__.__name__} failed: {e}")
