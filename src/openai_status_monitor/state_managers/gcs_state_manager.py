"""
gcs_state_manager.py

Google Cloud Storage-based state management.
"""

import json
import logging
from google.cloud import storage
from google.api_core import exceptions
from .base_state_manager import BaseStateManager

logger = logging.getLogger(__name__)


class GCSStateManager(BaseStateManager):
    """Manages state using Google Cloud Storage."""
    
    def __init__(self, bucket_name, blob_name):
        """
        Initialize GCS-based state manager.
        
        Args:
            bucket_name (str): GCS bucket name
            blob_name (str): Blob name (file path in bucket)
        """
        self.bucket_name = bucket_name
        self.blob_name = blob_name
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)
        self.blob = self.bucket.blob(blob_name)
        logger.debug(f"GCSStateManager initialized: {bucket_name}/{blob_name}")
    
    def load_state(self):
        """Load state from GCS blob."""
        try:
            if not self.blob.exists():
                logger.info(f"State blob not found in GCS. Starting with empty state.")
                return {}
            
            state_json = self.blob.download_as_text()
            state = json.loads(state_json)
            logger.debug(f"State loaded from GCS: {self.bucket_name}/{self.blob_name}")
            return state
        except exceptions.NotFound:
            logger.info(f"State blob not found in GCS. Starting with empty state.")
            return {}
        except Exception as e:
            logger.error(f"Failed to load state from GCS: {e}")
            return {}
    
    def save_state(self, state):
        """Save state to GCS blob."""
        try:
            state_json = json.dumps(state, indent=2)
            self.blob.upload_from_string(state_json, content_type='application/json')
            logger.debug(f"State saved to GCS: {self.bucket_name}/{self.blob_name}")
        except Exception as e:
            logger.error(f"Failed to save state to GCS: {e}")
            raise
