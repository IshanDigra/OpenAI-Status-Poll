"""
file_state_manager.py

File-based state management using local JSON file.
"""

import json
import logging
import os
from .base_state_manager import BaseStateManager

logger = logging.getLogger(__name__)


class FileStateManager(BaseStateManager):
    """Manages state using a local JSON file."""
    
    def __init__(self, file_path):
        """
        Initialize file-based state manager.
        
        Args:
            file_path (str): Path to the state JSON file
        """
        self.file_path = file_path
        logger.debug(f"FileStateManager initialized with path: {file_path}")
    
    def load_state(self):
        """Load state from JSON file."""
        if not os.path.exists(self.file_path):
            logger.info(f"State file not found. Starting with empty state.")
            return {}
        
        try:
            with open(self.file_path, 'r') as f:
                state = json.load(f)
                logger.debug(f"State loaded from {self.file_path}")
                return state
        except Exception as e:
            logger.error(f"Failed to load state from {self.file_path}: {e}")
            return {}
    
    def save_state(self, state):
        """Save state to JSON file."""
        try:
            with open(self.file_path, 'w') as f:
                json.dump(state, f, indent=2)
                logger.debug(f"State saved to {self.file_path}")
        except Exception as e:
            logger.error(f"Failed to save state to {self.file_path}: {e}")
            raise
