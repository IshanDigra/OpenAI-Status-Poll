"""
base_notifier.py

Abstract base class for notifiers.
"""

from abc import ABC, abstractmethod


class BaseNotifier(ABC):
    """Abstract base class for notification channels."""
    
    @abstractmethod
    def notify(self, incident):
        """
        Send notification about an incident.
        
        Args:
            incident (dict): Incident data with keys: id, title, updated, summary, link
        """
        pass
