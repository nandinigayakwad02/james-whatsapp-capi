import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Meta/Facebook Configuration
    META_PIXEL_ID = os.getenv("META_PIXEL_ID")
    META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
    META_API_VERSION = "v18.0"
    META_API_URL = f"https://graph.facebook.com/{META_API_VERSION}"
    
    # Server Configuration
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Optional: ManyChat Verification
    MANYCHAT_VERIFICATION_TOKEN = os.getenv("MANYCHAT_VERIFICATION_TOKEN")
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.META_PIXEL_ID:
            raise ValueError("META_PIXEL_ID is required in .env file")
        if not cls.META_ACCESS_TOKEN:
            raise ValueError("META_ACCESS_TOKEN is required in .env file")
        
        print("✅ Configuration validated successfully")
        print(f"📍 Meta Pixel ID: {cls.META_PIXEL_ID}")
        print(f"🔗 API URL: {cls.META_API_URL}")
