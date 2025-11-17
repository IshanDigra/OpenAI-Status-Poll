"""
parser.py

Parses the OpenAI status Atom feed and extracts incident data.
"""

import logging
from bs4 import BeautifulSoup
from dateutil import parser as date_parser

logger = logging.getLogger(__name__)


def parse_feed(feed):
    """
    Parse feedparser feed object and extract incident information.
    
    Args:
        feed: feedparser feed object
        
    Returns:
        List of incident dictionaries with keys: id, title, updated, summary, link
    """
    incidents = []
    
    for entry in feed.entries:
        try:
            # Extract HTML summary and convert to plain text
            summary_html = entry.get('summary', '')
            soup = BeautifulSoup(summary_html, 'html.parser')
            summary_text = soup.get_text(separator=' ', strip=True)
            
            incident = {
                'id': entry.get('id', ''),
                'title': entry.get('title', 'Unknown Title'),
                'updated': entry.get('updated', ''),
                'summary': summary_text,
                'link': entry.get('link', '')
            }
            
            # Parse the updated timestamp
            if incident['updated']:
                try:
                    incident['updated_dt'] = date_parser.parse(incident['updated'])
                except Exception as e:
                    logger.warning(f"Failed to parse date '{incident['updated']}': {e}")
                    incident['updated_dt'] = None
            else:
                incident['updated_dt'] = None
                
            incidents.append(incident)
            
        except Exception as e:
            logger.error(f"Error parsing feed entry: {e}")
            continue
    
    return incidents
