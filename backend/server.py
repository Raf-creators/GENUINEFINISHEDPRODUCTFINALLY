from fastapi import FastAPI, APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from typing import List
from datetime import datetime

# Import models and database
from models import (
    Service, ServiceCreate, Review, ReviewCreate, 
    QuoteRequest, QuoteRequestCreate, Contact, ContactCreate,
    GalleryImage, GalleryImageCreate, MessageResponse, ErrorResponse
)
from database import Database
from email_service import email_service

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db_client = client[os.environ['DB_NAME']]

# Initialize database helper
database = Database()

# Create the main app
app = FastAPI(
    title="PNM Gardeners API",
    description="Backend API for PNM Gardeners website",
    version="1.0.0"
)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Startup event - seed initial data
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up PNM Gardeners API...")
    try:
        await database.seed_initial_data()
        logger.info("Database initialization completed")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")

# Health check endpoint
@api_router.get("/", response_model=MessageResponse)
async def root():
    return MessageResponse(message="PNM Gardeners API is running")

# Services Endpoints
@api_router.get("/services", response_model=List[Service])
async def get_all_services():
    """Get all gardening services"""
    try:
        services = await database.get_all_services()
        return services
    except Exception as e:
        logger.error(f"Error fetching services: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch services"
        )

@api_router.get("/services/{service_id}", response_model=Service)
async def get_service(service_id: str):
    """Get a specific service by ID"""
    try:
        service = await database.get_service_by_id(service_id)
        if not service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service not found"
            )
        return service
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching service {service_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch service"
        )

# Reviews Endpoints
@api_router.get("/reviews", response_model=List[Review])
async def get_all_reviews():
    """Get all approved customer reviews"""
    try:
        reviews = await database.get_all_reviews()
        return reviews
    except Exception as e:
        logger.error(f"Error fetching reviews: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch reviews"
        )

@api_router.post("/reviews", response_model=MessageResponse)
async def create_review(review_data: ReviewCreate):
    """Submit a new customer review"""
    try:
        # Add current date for the review
        current_date = datetime.now().strftime("%d %b %Y")
        review = Review(**review_data.dict(), date=current_date, approved=False)  # New reviews need approval
        review_id = await database.create_review(review)
        return MessageResponse(
            message="Review submitted successfully and is pending approval",
            id=review_id
        )
    except Exception as e:
        logger.error(f"Error creating review: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to submit review"
        )

# Database initialization endpoint for production
@api_router.post("/init-db", response_model=MessageResponse)
async def initialize_database():
    """Initialize database with seed data (admin only)"""
    try:
        await database.seed_initial_data()
        return MessageResponse(message="Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initialize database: {str(e)}"
        )

# Simple reviews endpoint for production
@api_router.post("/add-reviews", response_model=MessageResponse)  
async def add_basic_reviews():
    """Add basic reviews for map and reviews section"""
    try:
        # Simple reviews data for map
        reviews = [
            {"id": "1", "name": "Verified Customer", "rating": 10, "date": "4 days ago", "text": "Great communication from start to finish. Delighted with the end result.", "service": "Garden clearance", "postcode": "SW19", "lat": 51.4214, "lng": -0.1878, "images": []},
            {"id": "2", "name": "Verified Customer", "rating": 10, "date": "4 days ago", "text": "Really great experience, the guys were friendly and efficient.", "service": "Garden Clearance", "postcode": "SW16", "lat": 51.4325, "lng": -0.1221, "images": []},
            {"id": "3", "name": "Verified Customer", "rating": 10, "date": "5 days ago", "text": "Quick and professional service.", "service": "Bush removal", "postcode": "SW16", "lat": 51.4352, "lng": -0.1205, "images": []}
        ]
        
        # Insert into database
        for review in reviews:
            await database.db["reviews"].insert_one(review)
        
        return MessageResponse(message="Reviews added successfully")
    except Exception as e:
        logger.error(f"Error adding reviews: {e}")
        return MessageResponse(message=f"Added reviews with some issues: {str(e)}")

# Quote Requests Endpoints
@api_router.post("/quotes", response_model=MessageResponse)
async def create_quote_request(quote_data: QuoteRequestCreate):
    """Submit a quote request"""
    try:
        quote = QuoteRequest(**quote_data.dict())
        quote_id = await database.create_quote_request(quote)
        
        logger.info(f"New quote request received from {quote_data.name} for {quote_data.service}")
        
        # Send email notifications
        try:
            # Send notification to business email
            await email_service.send_quote_notification(quote_data)
            
            # Send confirmation to customer
            await email_service.send_customer_confirmation(
                quote_data.email, 
                quote_data.name, 
                "quote"
            )
            
            logger.info(f"Email notifications sent for quote request {quote_id}")
        except Exception as email_error:
            logger.error(f"Failed to send email notifications: {email_error}")
            # Don't fail the request if email fails
        
        return MessageResponse(
            message="Quote request submitted successfully. We'll get back to you within 24 hours!",
            id=quote_id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating quote request: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to submit quote request"
        )

@api_router.get("/quotes", response_model=List[QuoteRequest])
async def get_all_quotes():
    """Get all quote requests (admin endpoint)"""
    try:
        quotes = await database.get_all_quote_requests()
        return quotes
    except Exception as e:
        logger.error(f"Error fetching quotes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch quotes"
        )

# Contact Endpoints
@api_router.post("/contact", response_model=MessageResponse)
async def create_contact(contact_data: ContactCreate):
    """Submit a contact form"""
    try:
        contact = Contact(**contact_data.dict())
        contact_id = await database.create_contact(contact)
        
        logger.info(f"New contact form received from {contact_data.name}")
        
        # Send email notifications
        try:
            # Send notification to business email
            await email_service.send_contact_notification(contact_data)
            
            # Send confirmation to customer
            await email_service.send_customer_confirmation(
                contact_data.email, 
                contact_data.name, 
                "contact"
            )
            
            logger.info(f"Email notifications sent for contact form {contact_id}")
        except Exception as email_error:
            logger.error(f"Failed to send email notifications: {email_error}")
            # Don't fail the request if email fails
        
        return MessageResponse(
            message="Thank you for contacting us. We'll respond to your inquiry soon!",
            id=contact_id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating contact: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to submit contact form"
        )

@api_router.get("/contacts", response_model=List[Contact])
async def get_all_contacts():
    """Get all contact form submissions (admin endpoint)"""
    try:
        contacts = await database.get_all_contacts()
        return contacts
    except Exception as e:
        logger.error(f"Error fetching contacts: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch contacts"
        )

# Gallery Endpoints
@api_router.get("/gallery", response_model=List[GalleryImage])
async def get_gallery_images():
    """Get all gallery images"""
    try:
        images = await database.get_all_gallery_images()
        return images
    except Exception as e:
        logger.error(f"Error fetching gallery images: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch gallery images"
        )

@api_router.get("/gallery/real-photos")
async def get_real_gallery_photos():
    """Get real Google Drive gallery photos organized by service"""
    try:
        import json
        gallery_data_path = '/app/real_gallery_data.json'
        
        if not os.path.exists(gallery_data_path):
            # Create the gallery data if it doesn't exist
            logger.info("Gallery data file not found, creating it...")
            import subprocess
            result = subprocess.run(['python', '/app/create_gallery_data.py'], 
                                  capture_output=True, text=True, cwd='/app')
            if result.returncode != 0:
                raise Exception(f"Failed to create gallery data: {result.stderr}")
        
        with open(gallery_data_path, 'r') as f:
            gallery_data = json.load(f)
        
        logger.info(f"Serving real gallery data with {len(gallery_data)} service albums")
        return gallery_data
        
    except Exception as e:
        logger.error(f"Error fetching real gallery photos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch real gallery photos: {str(e)}"
        )

@api_router.post("/gallery", response_model=MessageResponse)
async def create_gallery_image(image_data: GalleryImageCreate):
    """Upload a new gallery image (admin endpoint)"""
    try:
        image = GalleryImage(**image_data.dict())
        image_id = await database.create_gallery_image(image)
        return MessageResponse(
            message="Gallery image uploaded successfully",
            id=image_id
        )
    except Exception as e:
        logger.error(f"Error creating gallery image: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload gallery image"
        )

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "details": str(exc)}
    )

# Include the router in the main app
app.include_router(api_router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    await database.close()
    client.close()
    logger.info("Database connections closed")
if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)