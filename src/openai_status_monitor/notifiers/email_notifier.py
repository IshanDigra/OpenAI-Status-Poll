"""
email_notifier.py

Email notifier using SMTP.
"""

import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .base_notifier import BaseNotifier

logger = logging.getLogger(__name__)


class EmailNotifier(BaseNotifier):
    """Sends incident notifications via email using SMTP."""
    
    def __init__(self, smtp_host, smtp_port, smtp_user, smtp_password, email_from, email_to):
        """
        Initialize email notifier.
        
        Args:
            smtp_host (str): SMTP server hostname
            smtp_port (int): SMTP server port
            smtp_user (str): SMTP username
            smtp_password (str): SMTP password
            email_from (str): From email address
            email_to (str): To email address
        """
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.email_from = email_from
        self.email_to = email_to
        logger.debug(f"EmailNotifier initialized: {email_from} -> {email_to}")
    
    def notify(self, incident):
        """Send incident notification via email."""
        if not all([self.smtp_user, self.smtp_password, self.email_from, self.email_to]):
            logger.warning("Email configuration incomplete. Skipping email notification.")
            return
        
        # Create email message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"🚨 OpenAI Status Alert: {incident['title']}"
        msg['From'] = self.email_from
        msg['To'] = self.email_to
        
        # Create plain text and HTML versions
        text = f"""
OpenAI Status Alert
{'='*60}

Title: {incident['title']}
Updated: {incident['updated']}
Link: {incident['link']}

Summary:
{incident['summary']}

{'='*60}
"""
        
        html = f"""
<html>
  <body style="font-family: Arial, sans-serif;">
    <div style="background-color: #f44336; color: white; padding: 20px; border-radius: 5px;">
      <h2>🚨 OpenAI Status Alert</h2>
    </div>
    <div style="padding: 20px; background-color: #f9f9f9; margin-top: 10px; border-radius: 5px;">
      <h3>{incident['title']}</h3>
      <p><strong>Updated:</strong> {incident['updated']}</p>
      <p><strong>Summary:</strong></p>
      <p>{incident['summary']}</p>
      <p><a href="{incident['link']}" style="color: #1976d2;">View Full Details</a></p>
    </div>
  </body>
</html>
"""
        
        # Attach parts
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        try:
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Email notification sent successfully for: {incident['title']}")
        except Exception as e:
            logger.error(f"Failed to send email notification: {e}")
            raise
