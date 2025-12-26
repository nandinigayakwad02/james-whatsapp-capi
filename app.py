from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
import logging
from config import Config
from meta_capi import MetaConversionAPI
from utils import validate_webhook_payload

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="ManyChat to Meta CAPI Bridge",
    description="Webhook server to receive ManyChat events and send to Meta Conversion API",
    version="1.0.0"
)

# Initialize Meta CAPI client
meta_capi = MetaConversionAPI()

# Pydantic models for request validation
class WebhookPayload(BaseModel):
    phone: str = Field(..., description="User's phone number from WhatsApp")
    timestamp: Optional[str] = Field(None, description="Event timestamp (ISO format)")
    flow_name: Optional[str] = Field(None, description="ManyChat flow name")
    user_id: Optional[str] = Field(None, description="ManyChat user ID")
    full_name: Optional[str] = Field(None, description="User's full name")
    
    # Campaign attribution parameters
    fbclid: Optional[str] = Field(None, description="Facebook Click ID (for ad attribution)")
    fbc: Optional[str] = Field(None, description="Facebook Click cookie")
    fbp: Optional[str] = Field(None, description="Facebook Pixel cookie")
    
    class Config:
        json_schema_extra = {
            "example": {
                "phone": "+919876543210",
                "timestamp": "2025-12-22T12:42:00Z",
                "flow_name": "Welcome Flow",
                "user_id": "manychat_user_123",
                "full_name": "John Doe",
                "fbclid": "IwAR123abc",
                "fbc": "fb.1.1596403881668.IwAR123abc",
                "fbp": "fb.1.1596403881668.1098115397"
            }
        }

@app.on_event("startup")
async def startup_event():
    """Validate configuration on startup"""
    logger.info("🚀 Starting ManyChat to Meta CAPI Bridge...")
    
    try:
        Config.validate()
        logger.info("✅ Server started successfully!")
    except ValueError as e:
        logger.error(f"❌ Configuration error: {str(e)}")
        raise
 
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "service": "ManyChat to Meta CAPI Bridge",
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "meta_pixel_id": Config.META_PIXEL_ID,
        "api_version": Config.META_API_VERSION
    }

@app.post("/webhook")
async def webhook(payload: WebhookPayload):
    """
    Main webhook endpoint to receive ManyChat data
    
    This endpoint:
    1. Receives webhook from ManyChat
    2. Validates the payload
    3. Sends event to Meta Conversion API
    4. Returns success response
    """
    try:
        logger.info("=" * 60)
        logger.info("📨 WEBHOOK RECEIVED FROM MANYCHAT")
        logger.info("=" * 60)
        
        # Print FULL payload for debugging
        print("\n COMPLETE PAYLOAD:")
        print(f"   Phone: {payload}")
        # print(f"   Timestamp: {payload.timestamp}")
        print(f"   Flow Name: {payload.flow_name}")
        # # print(f"   Subscriber Data: {payload.subscriber_data}")
        # print(f"   User ID: {payload.user_id}")
        # print(f"   Full Name: {payload.full_name}")
        # print(f"    fbclid: {payload.fbclid or 'Not provided'}")
        # print(f"    fbc: {payload.fbc or 'Not provided'}")
        # print(f"    fbp: {payload.fbp or 'Not provided'}")
        
        logger.info(f"📱 Phone (masked): {payload.phone[-4:].rjust(len(payload.phone), '*')}")
        logger.info(f"🔄 Flow: {payload.flow_name or 'N/A'}")
        
        # Send event to Meta CAPI with campaign attribution
        # Using Meta's standard event for Click-to-WhatsApp ads
        result = meta_capi.send_event(
            phone=payload.phone,
            event_name="messaging_conversation_started_7d",
            timestamp_str=payload.timestamp,
            flow_name=payload.flow_name,
            additional_data={
                "user_id": payload.user_id,
                "full_name": payload.full_name
            } if payload.user_id else None,
            fbclid=payload.fbclid,
            fbc=payload.fbc,
            fbp=payload.fbp
        )
        
        # Print Meta API Response
        print("\n📤 META API RESPONSE:")
        print(f"   Success: {result.get('success')}")
        print(f"   Events Received: {result.get('events_received')}")
        print(f"   FBTrace ID: {result.get('fbtrace_id')}")
        if not result["success"]:
            print(f" Error: {result.get('error')}")
        print("=" * 60 + "\n")
        
        if result["success"]:
            logger.info("✅ Webhook processed successfully")
            
            return JSONResponse(
                status_code=200,
                content={
                    "status": "success",
                    "message": "Event sent to Meta successfully",
                    "events_received": result.get("events_received"),
                    "fbtrace_id": result.get("fbtrace_id")
                }
            )
        else:
            logger.error("❌ Failed to send event to Meta")
            
            # Still return 200 to ManyChat to prevent retries
            # Log the error for manual review
            return JSONResponse(
                status_code=200,
                content={
                    "status": "error",
                    "message": "Failed to send to Meta, but webhook acknowledged",
                    "error": result.get("error")
                }
            )
    
    except Exception as e:
        logger.error(f"❌ Webhook processing error: {str(e)}")
        
        # Return 200 to prevent ManyChat retries
        return JSONResponse(
            status_code=200,
            content={
                "status": "error",
                "message": "Internal error, but webhook acknowledged",
                "error": str(e)
            }
        )

@app.post("/test-event")
async def test_event(payload: WebhookPayload):
    """
    Test endpoint to manually send events
    Useful for testing without ManyChat
    """
    logger.info("🧪 Test event triggered")
    
    result = meta_capi.send_event(
        phone=payload.phone,
        event_name="whatsapp_conversation_started",
        timestamp_str=payload.timestamp,
        flow_name=payload.flow_name or "Test Flow"
    )
    
    return result

@app.get("/test-connection")
async def test_connection():
    """Test Meta CAPI connection"""
    success = meta_capi.test_connection()
    
    if success:
        return {"status": "success", "message": "Meta CAPI connection successful"}
    else:
        return {"status": "error", "message": "Meta CAPI connection failed"}

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=Config.PORT,
        reload=Config.DEBUG
    )
