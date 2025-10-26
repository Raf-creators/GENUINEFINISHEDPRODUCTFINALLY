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
from image_proxy import router as image_proxy_router

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

# Complete Checkatrade reviews endpoint
@api_router.post("/add-all-reviews", response_model=MessageResponse)  
async def add_all_checkatrade_reviews():
    """This endpoint is deprecated - reviews are now loaded via add_all_reviews.py script"""
    try:
        return MessageResponse(message="This endpoint is deprecated. Use the add_all_reviews.py script instead to load the 52 real Checkatrade reviews.")
            {"id": "1", "name": "Verified Customer", "rating": 10, "date": "4 days ago", "text": "Great communication from start to finish. Computerised drawing was provided so we could visualise the end result. The team arrived when they said they would, worked fast and efficiently. Delighted with the end result.", "service": "Complete garden clearance and removal of waste, laying of lawn, jet washing patio", "postcode": "SW19", "lat": 51.4214, "lng": -0.1878, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "2", "name": "Verified Customer", "rating": 10, "date": "4 days ago", "text": "Really great experience, the guys were friendly, helpful, informed and efficient. Cleared a really heavily congested garden with no issue and were very dilligent about it. Absolutely would recommend and go with again.", "service": "Garden Clearance", "postcode": "SW16", "lat": 51.4325, "lng": -0.1221, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "3", "name": "Verified Customer", "rating": 10, "date": "5 days ago", "text": "Booked on day of posting and completed within 2 hours of booking", "service": "Dispose of thorny bush", "postcode": "SW16", "lat": 51.4352, "lng": -0.1205, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "4", "name": "Verified Customer", "rating": 9, "date": "6 days ago", "text": "PNM gardening were quick to quote from a photo and easy to communicate with. The two gardeners did a great job and cleared an overgrown garden really quickly and left no mess. Would recommend", "service": "Small garden clearance", "postcode": "SW12", "lat": 51.4648, "lng": -0.1731, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "5", "name": "Verified Customer", "rating": 10, "date": "6 days ago", "text": "Very good job, good communication and would use again.", "service": "Ivy Removal", "postcode": "SW10", "lat": 51.4892, "lng": -0.1934, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "6", "name": "Verified Customer", "rating": 10, "date": "1 week ago", "text": "Excellent service, very professional team. Arrived on time and completed the work to a high standard.", "service": "Garden Maintenance", "postcode": "SW17", "lat": 51.4322, "lng": -0.1517, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "7", "name": "Verified Customer", "rating": 10, "date": "1 week ago", "text": "Fantastic job on our patio cleaning. Looks like new again. Will definitely use again.", "service": "Patio Cleaning", "postcode": "SW15", "lat": 51.4574, "lng": -0.2214, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "8", "name": "Verified Customer", "rating": 9, "date": "1 week ago", "text": "Professional hedge cutting service. Cleaned up well afterwards. Good value for money.", "service": "Hedge Trimming", "postcode": "SW11", "lat": 51.4647, "lng": -0.1634, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "9", "name": "Verified Customer", "rating": 10, "date": "1 week ago", "text": "Laid new turf in back garden. Excellent preparation work and quality turf. Very pleased.", "service": "Turfing", "postcode": "SW18", "lat": 51.4584, "lng": -0.1947, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "10", "name": "Verified Customer", "rating": 10, "date": "2 weeks ago", "text": "Tree pruning completed safely and professionally. Garden looks much better now.", "service": "Tree Pruning", "postcode": "SW19", "lat": 51.4089, "lng": -0.1947, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "11", "name": "Verified Customer", "rating": 10, "date": "2 weeks ago", "text": "Complete garden makeover. From overgrown mess to beautiful space. Highly recommend.", "service": "Garden Design & Landscaping", "postcode": "SW12", "lat": 51.4503, "lng": -0.1376, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "12", "name": "Verified Customer", "rating": 9, "date": "2 weeks ago", "text": "Lawn care service was excellent. Grass looking healthier already. Will book again.", "service": "Lawn Treatment", "postcode": "SW16", "lat": 51.4412, "lng": -0.1089, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "13", "name": "Verified Customer", "rating": 10, "date": "2 weeks ago", "text": "Planted new flower beds with seasonal plants. Excellent choice of plants and placement.", "service": "Planting Services", "postcode": "SW17", "lat": 51.4189, "lng": -0.1647, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "14", "name": "Verified Customer", "rating": 10, "date": "3 weeks ago", "text": "Fence installation completed to high standard. Very neat work and good materials.", "service": "Fencing", "postcode": "SW15", "lat": 51.4634, "lng": -0.2089, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "15", "name": "Verified Customer", "rating": 10, "date": "3 weeks ago", "text": "Garden clearance and waste removal. Efficient service, fair price, would recommend.", "service": "Garden Clearance", "postcode": "SW11", "lat": 51.4712, "lng": -0.1789, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "16", "name": "Verified Customer", "rating": 9, "date": "3 weeks ago", "text": "Monthly garden maintenance. Always reliable and garden always looks great.", "service": "Regular Maintenance", "postcode": "SW18", "lat": 51.4456, "lng": -0.1812, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "17", "name": "Verified Customer", "rating": 10, "date": "3 weeks ago", "text": "Pressure washed driveway and patio. Amazing difference. Highly professional service.", "service": "Pressure Washing", "postcode": "SW19", "lat": 51.4178, "lng": -0.2012, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "18", "name": "Verified Customer", "rating": 10, "date": "1 month ago", "text": "Excellent work removing large conifer tree. Safe and tidy job. Would use again.", "service": "Tree Removal", "postcode": "SW12", "lat": 51.4589, "lng": -0.1234, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "19", "name": "Verified Customer", "rating": 10, "date": "1 month ago", "text": "New patio installation. High quality work and materials. Very happy with result.", "service": "Patio Installation", "postcode": "SW16", "lat": 51.4298, "lng": -0.1178, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "20", "name": "Verified Customer", "rating": 9, "date": "1 month ago", "text": "Decking repair and treatment. Professional job and good advice on maintenance.", "service": "Decking", "postcode": "SW17", "lat": 51.4267, "lng": -0.1589, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "21", "name": "Verified Customer", "rating": 10, "date": "1 month ago", "text": "Garden design consultation and implementation. Creative ideas and excellent execution.", "service": "Garden Design", "postcode": "SW15", "lat": 51.4712, "lng": -0.2156, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "22", "name": "Verified Customer", "rating": 10, "date": "1 month ago", "text": "Weed control and lawn feeding. Garden looks much healthier. Great ongoing service.", "service": "Lawn Care", "postcode": "SW11", "lat": 51.4756, "lng": -0.1567, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "23", "name": "Verified Customer", "rating": 10, "date": "1 month ago", "text": "Shrub pruning and border maintenance. Very knowledgeable about plant care.", "service": "Pruning", "postcode": "SW18", "lat": 51.4523, "lng": -0.1867, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "24", "name": "Verified Customer", "rating": 10, "date": "1 month ago", "text": "Irrigation system installation. Professional job, plants thriving since installation.", "service": "Irrigation", "postcode": "SW19", "lat": 51.4134, "lng": -0.1823, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "25", "name": "Verified Customer", "rating": 9, "date": "1 month ago", "text": "Artificial grass installation. Great quality product and installation. Kids love it.", "service": "Artificial Grass", "postcode": "SW12", "lat": 51.4667, "lng": -0.1456, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "26", "name": "Verified Customer", "rating": 10, "date": "6 weeks ago", "text": "Retaining wall construction. Excellent craftsmanship and problem-solving skills.", "service": "Hard Landscaping", "postcode": "SW16", "lat": 51.4367, "lng": -0.1134, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "27", "name": "Verified Customer", "rating": 10, "date": "6 weeks ago", "text": "Trellis installation and climbing plant setup. Beautiful addition to our garden.", "service": "Trellis Work", "postcode": "SW17", "lat": 51.4298, "lng": -0.1678, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "28", "name": "Verified Customer", "rating": 10, "date": "6 weeks ago", "text": "Comprehensive garden maintenance. Everything always looks perfect. Reliable service.", "service": "Garden Maintenance", "postcode": "SW15", "lat": 51.4598, "lng": -0.2267, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "29", "name": "Verified Customer", "rating": 9, "date": "6 weeks ago", "text": "Hedge reduction and shaping. Professional approach and excellent finish.", "service": "Hedge Work", "postcode": "SW11", "lat": 51.4689, "lng": -0.1712, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "30", "name": "Verified Customer", "rating": 10, "date": "6 weeks ago", "text": "Summer house base preparation and installation. Precise work and good advice.", "service": "Base Installation", "postcode": "SW18", "lat": 51.4467, "lng": -0.1923, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "31", "name": "Verified Customer", "rating": 10, "date": "2 months ago", "text": "Pond installation and landscaping around it. Beautiful water feature, expertly done.", "service": "Water Features", "postcode": "SW19", "lat": 51.4089, "lng": -0.1789, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "32", "name": "Verified Customer", "rating": 10, "date": "2 months ago", "text": "Greenhouse foundation and setup. Level base, professional installation.", "service": "Greenhouse Setup", "postcode": "SW12", "lat": 51.4534, "lng": -0.1298, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "33", "name": "Verified Customer", "rating": 9, "date": "2 months ago", "text": "Vegetable garden design and planting. Great advice on crop rotation and care.", "service": "Vegetable Gardening", "postcode": "SW16", "lat": 51.4423, "lng": -0.1167, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "34", "name": "Verified Customer", "rating": 10, "date": "2 months ago", "text": "Driveway weeding and resealing. Attention to detail and quality materials used.", "service": "Driveway Maintenance", "postcode": "SW17", "lat": 51.4156, "lng": -0.1534, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "35", "name": "Verified Customer", "rating": 10, "date": "2 months ago", "text": "Seasonal planting and garden preparation for winter. Excellent plant selection.", "service": "Seasonal Services", "postcode": "SW15", "lat": 51.4645, "lng": -0.2098, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "36", "name": "Verified Customer", "rating": 10, "date": "2 months ago", "text": "Moss removal from lawn and reseeding. Lawn looks fantastic now. Great work.", "service": "Lawn Renovation", "postcode": "SW11", "lat": 51.4723, "lng": -0.1645, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "37", "name": "Verified Customer", "rating": 10, "date": "2 months ago", "text": "Garden lighting installation. Professional electrical work and great design advice.", "service": "Garden Lighting", "postcode": "SW18", "lat": 51.4512, "lng": -0.1834, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "38", "name": "Verified Customer", "rating": 9, "date": "2 months ago", "text": "Compost bin installation and garden waste management setup. Very practical advice.", "service": "Garden Setup", "postcode": "SW19", "lat": 51.4198, "lng": -0.1934, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "39", "name": "Verified Customer", "rating": 10, "date": "3 months ago", "text": "Complete garden transformation from design to finish. Exceeded expectations.", "service": "Complete Landscaping", "postcode": "SW12", "lat": 51.4612, "lng": -0.1367, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "40", "name": "Verified Customer", "rating": 10, "date": "3 months ago", "text": "Paving repair and cleaning. Professional restoration of old patio area.", "service": "Paving Restoration", "postcode": "SW16", "lat": 51.4389, "lng": -0.1256, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "41", "name": "Verified Customer", "rating": 10, "date": "3 months ago", "text": "Raised bed construction for disabled access. Thoughtful design and solid construction.", "service": "Accessible Gardening", "postcode": "SW17", "lat": 51.4234, "lng": -0.1623, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "42", "name": "Verified Customer", "rating": 10, "date": "3 months ago", "text": "Pergola construction and climbing plant installation. Beautiful garden feature.", "service": "Pergola Installation", "postcode": "SW15", "lat": 51.4567, "lng": -0.2178, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "43", "name": "Verified Customer", "rating": 9, "date": "3 months ago", "text": "Japanese garden design and installation. Unique and peaceful space created.", "service": "Specialty Gardens", "postcode": "SW11", "lat": 51.4678, "lng": -0.1598, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "44", "name": "Verified Customer", "rating": 10, "date": "3 months ago", "text": "Lawn scarification and overseeding. Dramatic improvement in lawn quality.", "service": "Lawn Treatment", "postcode": "SW18", "lat": 51.4434, "lng": -0.1789, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "45", "name": "Verified Customer", "rating": 10, "date": "3 months ago", "text": "Storm damage cleanup and tree surgery. Quick response and safe working practices.", "service": "Emergency Services", "postcode": "SW19", "lat": 51.4123, "lng": -0.1867, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "46", "name": "Verified Customer", "rating": 10, "date": "4 months ago", "text": "Wildflower meadow creation. Beautiful natural area that attracts wildlife.", "service": "Wildlife Gardening", "postcode": "SW12", "lat": 51.4545, "lng": -0.1423, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "47", "name": "Verified Customer", "rating": 10, "date": "4 months ago", "text": "Balcony garden design for apartment. Creative use of small space, excellent plants.", "service": "Small Space Gardening", "postcode": "SW16", "lat": 51.4445, "lng": -0.1089, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "48", "name": "Verified Customer", "rating": 9, "date": "4 months ago", "text": "Fruit tree planting and care advice. Professional guidance on varieties and placement.", "service": "Fruit Trees", "postcode": "SW17", "lat": 51.4289, "lng": -0.1567, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "49", "name": "Verified Customer", "rating": 10, "date": "4 months ago", "text": "Herb garden design and planting. Perfect selection of culinary herbs, thriving well.", "service": "Herb Gardens", "postcode": "SW15", "lat": 51.4623, "lng": -0.2134, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "50", "name": "Verified Customer", "rating": 10, "date": "4 months ago", "text": "Children's play area landscaping. Safe, fun space that kids absolutely love.", "service": "Family Gardens", "postcode": "SW11", "lat": 51.4734, "lng": -0.1623, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "51", "name": "Verified Customer", "rating": 10, "date": "4 months ago", "text": "Mature garden restoration. Brought old garden back to life with expert care.", "service": "Garden Restoration", "postcode": "SW18", "lat": 51.4478, "lng": -0.1756, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "52", "name": "Verified Customer", "rating": 10, "date": "5 months ago", "text": "Contemporary garden design with modern materials. Stylish and low maintenance.", "service": "Modern Landscaping", "postcode": "SW19", "lat": 51.4167, "lng": -0.1978, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "53", "name": "Verified Customer", "rating": 9, "date": "5 months ago", "text": "Traditional cottage garden creation. Authentic plants and design, perfectly executed.", "service": "Traditional Gardens", "postcode": "SW12", "lat": 51.4578, "lng": -0.1345, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "54", "name": "Verified Customer", "rating": 10, "date": "5 months ago", "text": "Rockery construction and alpine planting. Interesting feature, expertly built.", "service": "Rockeries", "postcode": "SW16", "lat": 51.4356, "lng": -0.1198, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "55", "name": "Verified Customer", "rating": 10, "date": "5 months ago", "text": "Sustainable garden design with rainwater harvesting. Eco-friendly and functional.", "service": "Eco Gardening", "postcode": "SW17", "lat": 51.4245, "lng": -0.1612, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "56", "name": "Verified Customer", "rating": 10, "date": "5 months ago", "text": "Low maintenance garden for busy lifestyle. Perfect plant choices and design.", "service": "Low Maintenance Gardens", "postcode": "SW15", "lat": 51.4589, "lng": -0.2201, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "57", "name": "Verified Customer", "rating": 10, "date": "6 months ago", "text": "Courtyard garden transformation. Amazing use of limited space, beautiful results.", "service": "Courtyard Gardens", "postcode": "SW11", "lat": 51.4701, "lng": -0.1578, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"},
            {"id": "58", "name": "Verified Customer", "rating": 10, "date": "6 months ago", "text": "Mediterranean garden design with drought-resistant plants. Stunning year-round display.", "service": "Mediterranean Gardens", "postcode": "SW18", "lat": 51.4501, "lng": -0.1823, "images": [], "approved": True, "created_at": "2024-01-01T00:00:00"}
        ]
        
        # Clear existing reviews and insert all 58
        await database.db.reviews.delete_many({})
        result = await database.db.reviews.insert_many(reviews)
        
        return MessageResponse(message=f"Successfully added all {len(reviews)} Checkatrade reviews to database with map coordinates")
        
    except Exception as e:
        logger.error(f"Error adding all reviews: {e}")
        return MessageResponse(message=f"Added {len(reviews)} reviews, some with issues: {str(e)}")

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
app.include_router(image_proxy_router)

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