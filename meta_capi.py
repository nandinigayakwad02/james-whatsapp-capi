import requests
import logging
from typing import Dict, Optional
from datetime import datetime

from config import Config
from utils import normalize_phone, hash_phone, get_unix_timestamp

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MetaConversionAPI:
    """Meta Conversion API integration"""
    
    def __init__(self):
        self.pixel_id = Config.META_PIXEL_ID
        self.access_token = Config.META_ACCESS_TOKEN
        self.api_url = f"{Config.META_API_URL}/{self.pixel_id}/events"
    
    def build_event_payload(
        self,
        phone: str,
        event_name: str = "whatsapp_conversation_started",
        timestamp_str: Optional[str] = None,
        custom_data: Optional[Dict] = None,
        fbclid: Optional[str] = None,
        fbc: Optional[str] = None,
        fbp: Optional[str] = None
    ) -> Dict:
        """
        Build Meta Conversion API event payload
        
        Args:
            phone: User's phone number
            event_name: Name of the event (default: whatsapp_conversation_started)
            timestamp_str: ISO timestamp of event
            custom_data: Additional custom data
            fbclid: Facebook Click ID (for ad attribution)
            fbc: Facebook Click cookie (for ad attribution)
            fbp: Facebook Pixel cookie (for ad attribution)
        
        Returns:
            Complete CAPI event payload
        """
        # Normalize and hash phone
        normalized_phone = normalize_phone(phone)
        hashed_phone = hash_phone(normalized_phone)
        
        # Get Unix timestamp
        event_time = get_unix_timestamp(timestamp_str)
        
        # Build user_data with required fields
        user_data = {
            "ph": [hashed_phone],  # Hashed phone (REQUIRED)
            "external_id": [hashed_phone]  # Use hashed phone as external ID (REQUIRED)
        }
        
        # Add campaign attribution if available
        if fbc:
            user_data["fbc"] = fbc  # Facebook Click cookie
        if fbp:
            user_data["fbp"] = fbp  # Facebook Pixel cookie
        
        # Build event data with REQUIRED parameters
        event_data = {
            "event_name": event_name,
            "event_time": event_time,
            "event_source_url": "whatsapp://conversation",  # REQUIRED
            "action_source": "chat",  # REQUIRED
            "user_data": user_data
        }
        
        # Add Facebook Click ID if available (for campaign attribution)
        if fbclid:
            if not custom_data:
                custom_data = {}
            custom_data["fbclid"] = fbclid
        
        # Add custom data if provided
        if custom_data:
            event_data["custom_data"] = custom_data
        
        # Complete payload
        payload = {
            "data": [event_data],
            "access_token": self.access_token
        }
        
        logger.info(f"📦 Event payload built for phone: {phone[-4:].rjust(len(phone), '*')}")
        if fbclid or fbc or fbp:
            logger.info(f"🎯 Campaign attribution included: fbclid={'✅' if fbclid else '❌'}, fbc={'✅' if fbc else '❌'}, fbp={'✅' if fbp else '❌'}")
        
        return payload
    
    def send_event(
        self,
        phone: str,
        event_name: str = "whatsapp_conversation_started",
        timestamp_str: Optional[str] = None,
        flow_name: Optional[str] = None,
        additional_data: Optional[Dict] = None,
        fbclid: Optional[str] = None,
        fbc: Optional[str] = None,
        fbp: Optional[str] = None
    ) -> Dict:
        """
        Send conversion event to Meta CAPI
        
        Args:
            phone: User's phone number
            event_name: Name of the event
            timestamp_str: ISO timestamp
            flow_name: ManyChat flow name
            additional_data: Any other custom data
            fbclid: Facebook Click ID (for ad attribution)
            fbc: Facebook Click cookie (for ad attribution)
            fbp: Facebook Pixel cookie (for ad attribution)
        
        Returns:
            API response dictionary
        """
        try:
            # Build custom data
            custom_data = {}
            if flow_name:
                custom_data["flow_name"] = flow_name
            if additional_data:
                custom_data.update(additional_data)
            
            # Build payload with campaign attribution
            payload = self.build_event_payload(
                phone=phone,
                event_name=event_name,
                timestamp_str=timestamp_str,
                custom_data=custom_data if custom_data else None,
                fbclid=fbclid,
                fbc=fbc,
                fbp=fbp
            )
            
            # Send to Meta
            logger.info(f"🚀 Sending event to Meta CAPI: {self.api_url}")
            
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=10
            )
            
            # Check response
            response.raise_for_status()
            response_data = response.json()
            
            # Log success
            events_received = response_data.get('events_received', 0)
            fbtrace_id = response_data.get('fbtrace_id', 'N/A')
            
            logger.info(f"✅ Event sent successfully!")
            logger.info(f"   Events received: {events_received}")
            logger.info(f"   FBTrace ID: {fbtrace_id}")
            
            return {
                "success": True,
                "events_received": events_received,
                "fbtrace_id": fbtrace_id,
                "response": response_data
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Failed to send event to Meta: {str(e)}")
            
            # Try to extract error details
            error_detail = str(e)
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                except:
                    error_detail = e.response.text
            
            return {
                "success": False,
                "error": str(e),
                "error_detail": error_detail
            }
        
        except Exception as e:
            logger.error(f"❌ Unexpected error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def test_connection(self) -> bool:
        """
        Test Meta CAPI connection with a test event
        
        Returns:
            True if connection successful, False otherwise
        """
        logger.info("🧪 Testing Meta CAPI connection...")
        
        result = self.send_event(
            phone="+1234567890",
            event_name="whatsapp_conversation_started",
            flow_name="Test Flow"
        )
        
        if result["success"]:
            logger.info("✅ Connection test passed!")
            return True
        else:
            logger.error("❌ Connection test failed!")
            logger.error(f"Error: {result.get('error')}")
            return False
