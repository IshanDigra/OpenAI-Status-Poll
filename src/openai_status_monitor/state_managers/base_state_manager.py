"""
base_state_manager.py

Abstract base class for state management.
"""

from abc import ABC, abstractmethod


class BaseStateManager(ABC):
    """Abstract base class for state persistence."""
    
    @abstractmethod
    def load_state(self):
        """
        Load state from storage.
        
        Returns:
            dict: State dictionary with keys: etag, last_modified, processed_incident_ids
        """
        pass
    
    @abstractmethod
    def save_state(self, state):
        """
        Save state to storage.
        
        Args:
            state (dict): State dictionary to save
        """
        pass
