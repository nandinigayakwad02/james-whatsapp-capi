import hashlib
import re
from datetime import datetime
from typing import Optional

def normalize_phone(phone: str) -> str:
    """
    Normalize phone number by removing all non-digit characters
    
    Example:
        +1 (234) 567-8900 -> 12345678900
        +91-9876543210 -> 919876543210
    """
    # Remove all non-digit characters
    normalized = re.sub(r'\D', '', phone)
    return normalized

def hash_phone(phone: str) -> str:
    """
    Hash phone number using SHA-256 as required by Meta CAPI
    
    Args:
        phone: Normalized phone number (digits only)
    
    Returns:
        SHA-256 hashed phone number in hexadecimal format
    """
    # Convert to lowercase and encode
    phone_lower = phone.lower().encode('utf-8')
    
    # Hash using SHA-256
    hashed = hashlib.sha256(phone_lower).hexdigest()
    
    return hashed

def get_unix_timestamp(timestamp_str: Optional[str] = None) -> int:
    """
    Convert ISO timestamp to Unix timestamp
    
    Args:
        timestamp_str: ISO format timestamp (e.g., "2025-12-22T12:42:00Z")
                      If None, uses current time
    
    Returns:
        Unix timestamp (seconds since epoch)
    """
    if timestamp_str:
        try:
            # Parse ISO format
            dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            return int(dt.timestamp())
        except:
            # Fallback to current time if parsing fails
            return int(datetime.now().timestamp())
    else:
        return int(datetime.now().timestamp())

def validate_webhook_payload(payload: dict) -> bool:
    """
    Validate ManyChat webhook payload has required fields
    
    Args:
        payload: Webhook payload dictionary
    
    Returns:
        True if valid, False otherwise
    """
    required_fields = ['phone']
    
    for field in required_fields:
        if field not in payload or not payload[field]:
            return False
    
    return True
