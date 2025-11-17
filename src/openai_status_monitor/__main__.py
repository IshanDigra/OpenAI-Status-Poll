"""
__main__.py

Main entry point for the OpenAI Status Monitor application.
"""

import sys
import time
import logging
import argparse
from . import config
from .monitor import StatusMonitor
from .state_managers.file_state_manager import FileStateManager
from .state_managers.gcs_state_manager import GCSStateManager
from .notifiers.console_notifier import ConsoleNotifier
from .notifiers.slack_notifier import SlackNotifier
from .notifiers.email_notifier import EmailNotifier

logger = logging.getLogger(__name__)


def create_state_manager():
    """Create and return the appropriate state manager based on configuration."""
    backend = config.STATE_BACKEND.lower()
    
    if backend == "file":
        logger.info(f"Using file-based state management: {config.STATE_FILE_PATH}")
        return FileStateManager(config.STATE_FILE_PATH)
    
    elif backend == "gcs":
        if not config.GCS_BUCKET_NAME:
            raise ValueError("GCS_BUCKET_NAME must be set when using GCS backend")
        logger.info(f"Using GCS state management: {config.GCS_BUCKET_NAME}/{config.GCS_STATE_BLOB_NAME}")
        return GCSStateManager(config.GCS_BUCKET_NAME, config.GCS_STATE_BLOB_NAME)
    
    else:
        raise ValueError(f"Unknown STATE_BACKEND: {backend}. Use 'file' or 'gcs'.")


def create_notifiers():
    """Create and return list of notifiers based on configuration."""
    notifiers = []
    
    for notifier_name in config.NOTIFIERS:
        notifier_name = notifier_name.strip().lower()
        
        if notifier_name == "console":
            logger.info("Enabling console notifier")
            notifiers.append(ConsoleNotifier())
        
        elif notifier_name == "slack":
            if config.SLACK_WEBHOOK_URL:
                logger.info("Enabling Slack notifier")
                notifiers.append(SlackNotifier(config.SLACK_WEBHOOK_URL))
            else:
                logger.warning("Slack notifier requested but SLACK_WEBHOOK_URL not configured")
        
        elif notifier_name == "email":
            if all([config.SMTP_USER, config.SMTP_PASSWORD, config.EMAIL_FROM, config.EMAIL_TO]):
                logger.info("Enabling email notifier")
                notifiers.append(EmailNotifier(
                    config.SMTP_HOST,
                    config.SMTP_PORT,
                    config.SMTP_USER,
                    config.SMTP_PASSWORD,
                    config.EMAIL_FROM,
                    config.EMAIL_TO
                ))
            else:
                logger.warning("Email notifier requested but email configuration incomplete")
        
        else:
            logger.warning(f"Unknown notifier: {notifier_name}")
    
    if not notifiers:
        logger.warning("No notifiers configured! Notifications will not be sent.")
    
    return notifiers


def main():
    """Main application entry point."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="OpenAI Status Monitor - Efficient polling of status.openai.com"
    )
    parser.add_argument(
        "--run-once",
        action="store_true",
        help="Run once and exit (useful for cron/scheduled tasks)"
    )
    args = parser.parse_args()
    
    logger.info("Starting OpenAI Status Monitor")
    logger.info(f"Feed URL: {config.FEED_URL}")
    logger.info(f"Poll Interval: {config.POLL_INTERVAL_SECONDS} seconds")
    logger.info(f"Run Mode: {'One-time' if args.run_once else 'Continuous'}")
    
    try:
        # Initialize components with dependency injection
        state_manager = create_state_manager()
        notifiers = create_notifiers()
        monitor = StatusMonitor(state_manager, notifiers)
        
        if args.run_once:
            # Single execution mode (for cron/schedulers)
            logger.info("Running single check...")
            has_new, count = monitor.check_for_updates()
            
            if has_new:
                logger.info(f"Check complete. Found {count} new incident(s).")
                sys.exit(0)  # Success with new incidents
            else:
                logger.info("Check complete. No new incidents.")
                sys.exit(0)  # Success, no incidents
        
        else:
            # Continuous monitoring mode
            logger.info("Starting continuous monitoring loop...")
            logger.info(f"Press Ctrl+C to stop.\n")
            
            while True:
                try:
                    monitor.check_for_updates()
                except Exception as e:
                    logger.error(f"Error during check: {e}", exc_info=True)
                
                logger.info(f"Sleeping for {config.POLL_INTERVAL_SECONDS} seconds...\n")
                time.sleep(config.POLL_INTERVAL_SECONDS)
    
    except KeyboardInterrupt:
        logger.info("\nReceived interrupt signal. Shutting down gracefully...")
        sys.exit(0)
    
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
