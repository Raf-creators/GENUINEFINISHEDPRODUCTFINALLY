from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Dict, Any, Optional
import os
from models import Service, Review, QuoteRequest, Contact, GalleryImage
import logging

# Setup logging
logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        mongo_url = os.environ['MONGO_URL']
        self.client = AsyncIOMotorClient(mongo_url)
        self.db = self.client[os.environ['DB_NAME']]
        
    async def close(self):
        self.client.close()
    
    # Services Collection
    async def get_all_services(self) -> List[Dict[str, Any]]:
        try:
            services = await self.db.services.find().to_list(1000)
            return services
        except Exception as e:
            logger.error(f"Error fetching services: {e}")
            return []
    
    async def get_service_by_id(self, service_id: str) -> Optional[Dict[str, Any]]:
        try:
            service = await self.db.services.find_one({"id": service_id})
            return service
        except Exception as e:
            logger.error(f"Error fetching service {service_id}: {e}")
            return None
    
    async def create_service(self, service: Service) -> str:
        try:
            result = await self.db.services.insert_one(service.dict())
            return service.id
        except Exception as e:
            logger.error(f"Error creating service: {e}")
            raise e
    
    # Reviews Collection
    async def get_all_reviews(self) -> List[Dict[str, Any]]:
        try:
            reviews = await self.db.reviews.find({"approved": True}).sort("created_at", -1).to_list(1000)
            return reviews
        except Exception as e:
            logger.error(f"Error fetching reviews: {e}")
            return []
    
    async def create_review(self, review: Review) -> str:
        try:
            result = await self.db.reviews.insert_one(review.dict())
            return review.id
        except Exception as e:
            logger.error(f"Error creating review: {e}")
            raise e
    
    # Quote Requests Collection
    async def create_quote_request(self, quote: QuoteRequest) -> str:
        try:
            result = await self.db.quote_requests.insert_one(quote.dict())
            return quote.id
        except Exception as e:
            logger.error(f"Error creating quote request: {e}")
            raise e
    
    async def get_all_quote_requests(self) -> List[Dict[str, Any]]:
        try:
            quotes = await self.db.quote_requests.find().sort("created_at", -1).to_list(1000)
            return quotes
        except Exception as e:
            logger.error(f"Error fetching quote requests: {e}")
            return []
    
    # Contacts Collection
    async def create_contact(self, contact: Contact) -> str:
        try:
            result = await self.db.contacts.insert_one(contact.dict())
            return contact.id
        except Exception as e:
            logger.error(f"Error creating contact: {e}")
            raise e
    
    async def get_all_contacts(self) -> List[Dict[str, Any]]:
        try:
            contacts = await self.db.contacts.find().sort("created_at", -1).to_list(1000)
            return contacts
        except Exception as e:
            logger.error(f"Error fetching contacts: {e}")
            return []
    
    # Gallery Collection
    async def get_all_gallery_images(self) -> List[Dict[str, Any]]:
        try:
            images = await self.db.gallery.find().sort("created_at", -1).to_list(1000)
            return images
        except Exception as e:
            logger.error(f"Error fetching gallery images: {e}")
            return []
    
    async def create_gallery_image(self, image: GalleryImage) -> str:
        try:
            result = await self.db.gallery.insert_one(image.dict())
            return image.id
        except Exception as e:
            logger.error(f"Error creating gallery image: {e}")
            raise e
    
    # Seed initial data
    async def seed_initial_data(self):
        """Seed database with initial data if collections are empty"""
        try:
            # Check if data already exists
            services_count = await self.db.services.count_documents({})
            if services_count > 0:
                logger.info("Database already seeded, skipping...")
                return
            
            # Seed services
            services_data = [
                {
                    "id": "1",
                    "title": "Garden Maintenance",
                    "description": "Comprehensive garden maintenance including lawn mowing, hedge trimming, weeding, and general upkeep. Professional service to keep your garden looking its best all year round.",
                    "image": "https://customer-assets.emergentagent.com/job_balham-gardening-hub/artifacts/iavpo09s_Garden%20Maintenance.jpeg",
                    "features": ["Lawn Mowing", "Hedge Trimming", "Weeding", "General Upkeep", "Seasonal Maintenance"],
                    "created_at": "2024-01-01T00:00:00",
                    "updated_at": "2024-01-01T00:00:00"
                },
                {
                    "id": "2",
                    "title": "Garden Clearance",
                    "description": "Complete garden clearance services including removal of overgrown vegetation, waste disposal, and site preparation. Fast and efficient clearance with professional waste removal.",
                    "image": "https://customer-assets.emergentagent.com/job_balham-gardening-hub/artifacts/tu9u2wbq_Garden%20Clearance.jpeg",
                    "features": ["Overgrown Garden Clearance", "Waste Removal", "Site Preparation", "Ivy Removal", "Thorny Bush Disposal"],
                    "created_at": "2024-01-01T00:00:00",
                    "updated_at": "2024-01-01T00:00:00"
                },
                {
                    "id": "3",
                    "title": "Hedge Trimming & Removal",
                    "description": "Professional hedge trimming and removal services. Expert maintenance to keep your hedges neat and healthy, or complete removal when needed.",
                    "image": "https://customer-assets.emergentagent.com/job_balham-gardening-hub/artifacts/ccw4wf98_Hedge%20Trimming.jpeg",
                    "features": ["Hedge Trimming", "Hedge Removal", "Hedge Shaping", "Pruning", "Cleanup Service"],
                    "created_at": "2024-01-01T00:00:00",
                    "updated_at": "2024-01-01T00:00:00"
                },
                {
                    "id": "4",
                    "title": "Turfing",
                    "description": "Professional turf laying services to create beautiful, lush lawns. From ground preparation to final installation of premium quality turf.",
                    "image": "https://customer-assets.emergentagent.com/job_balham-gardening-hub/artifacts/p467qw39_Turfing.jpeg",
                    "features": ["Ground Preparation", "Turf Installation", "Lawn Creation", "Soil Treatment", "Aftercare Advice"],
                    "created_at": "2024-01-01T00:00:00",
                    "updated_at": "2024-01-01T00:00:00"
                },
                {
                    "id": "5",
                    "title": "Lawn Care",
                    "description": "Professional lawn care services including mowing, edging, weed treatment, and overseeding. Keep your lawn healthy and beautiful throughout the year.",
                    "image": "https://customer-assets.emergentagent.com/job_balham-gardening-hub/artifacts/84y7gk19_Lawn%20Care.jpeg",
                    "features": ["Lawn Mowing", "Edging", "Weed Treatment", "Overseeding", "Lawn Health Assessment"],
                    "created_at": "2024-01-01T00:00:00",
                    "updated_at": "2024-01-01T00:00:00"
                },
                {
                    "id": "6",
                    "title": "Planting Services",
                    "description": "Expert planting schemes to suit your space and style. Professional plant selection, installation, and ongoing care to create beautiful garden displays.",
                    "image": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHw2fHxwbGFudGluZ3xlbnwwfHx8fDE3NTQ4Mzc5NDJ8MA&ixlib=rb-4.1.0&q=85",
                    "features": ["Plant Selection", "Flower Bed Design", "Seasonal Planting", "Bulb Planting", "Plant Care Advice"],
                    "created_at": "2024-01-01T00:00:00",
                    "updated_at": "2024-01-01T00:00:00"
                },
                {
                    "id": "7",
                    "title": "Patio Services",
                    "description": "Professional patio installation, repair, and maintenance. From new patio construction to pressure washing and restoration of existing patios.",
                    "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHw1fHxwYXRpb3xlbnwwfHx8fDE3NTQ4Mzc5NDJ8MA&ixlib=rb-4.1.0&q=85",
                    "features": ["Patio Installation", "Patio Repair", "Pressure Washing", "Stone & Block Paving", "Patio Design"],
                    "created_at": "2024-01-01T00:00:00",
                    "updated_at": "2024-01-01T00:00:00"
                },
                {
                    "id": "8",
                    "title": "Pruning",
                    "description": "Expert pruning services for trees, shrubs, and plants. Professional techniques to promote healthy growth and maintain the shape and size of your plants.",
                    "image": "https://images.unsplash.com/photo-1515150144380-bca9f1650ed9?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzd8MHwxfHNlYXJjaHwyfHxnYXJkZW5pbmd8ZW58MHx8fHwxNzU0ODM3OTM2fDA&ixlib=rb-4.1.0&q=85",
                    "features": ["Tree Pruning", "Shrub Pruning", "Seasonal Pruning", "Health Assessment", "Shape Maintenance"],
                    "created_at": "2024-01-01T00:00:00",
                    "updated_at": "2024-01-01T00:00:00"
                },
                {
                    "id": "9",
                    "title": "Trellis & Fencing",
                    "description": "Professional trellis installation and fencing services. Custom solutions for privacy, plant support, and garden structure. Quality materials and expert installation.",
                    "image": "https://images.unsplash.com/photo-1585128792020-803d29415281?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHw3fHx0cmVsbGlzfGVufDB8fHx8MTc1NDgzNzk0Mnww&ixlib=rb-4.1.0&q=85",
                    "features": ["Trellis Installation", "Garden Fencing", "Privacy Screens", "Plant Support Systems", "Custom Design"],
                    "created_at": "2024-01-01T00:00:00",
                    "updated_at": "2024-01-01T00:00:00"
                }
            ]
            
            await self.db.services.insert_many(services_data)
            
            # Seed reviews - Use existing reviews dataset
            all_reviews = [
                {
                    "id": "1",
                    "name": "Verified Customer",
                    "rating": 10,
                    "date": "4 days ago",
                    "text": "Great communication from start to finish. Computerised drawing was provided so we could visualise the end result. The team arrived when they said they would, worked fast and efficiently. Delighted with the end result.",
                    "service": "Complete garden clearance and removal of waste, laying of lawn, jet washing patio",
                    "postcode": "SW19",
                    "lat": 51.4214,
                    "lng": -0.1878,
                    "images": [
                        "https://storage.googleapis.com/core-media-service-production/user-media/01K20D7JF9PAXZC50HKQXKWQ2N.8A587B8F-ECA9-4B62-A048-F173619539FA.thumb.jpeg",
                        "https://storage.googleapis.com/core-media-service-production/user-media/01K20D7JTQNTDA7ZV9RF88CCQD.36BE73D4-47B7-4FFD-A13C-072AB930D37F.thumb.jpeg"
                    ],
                    "created_at": "2024-01-01T00:00:00"
                },
                {
                    "id": "2", 
                    "name": "Verified Customer",
                    "rating": 10,
                    "date": "4 days ago",
                    "text": "Really great experience, the guys were friendly, helpful, informed and efficient. Cleared a really heavily congested garden with no issue and were very dilligent about it. Absolutely would recommend and go with again.",
                    "service": "Garden Clearance",
                    "postcode": "SW16",
                    "lat": 51.4325,
                    "lng": -0.1221,
                    "images": [
                        "https://storage.googleapis.com/core-media-service-production/user-media/01K1Z59GTJSEAYJ1C52M16ZVX8.WhatsApp%20Image%202025-08-05%20at%2018.20.28_08e28d1a.thumb.jpg",
                        "https://storage.googleapis.com/core-media-service-production/user-media/01K1Z59H44TRPFVJQSX8BA1GP4.WhatsApp%20Image%202025-08-05%20at%2018.20.26_8984b8ef.thumb.jpg"
                    ],
                    "created_at": "2024-01-01T00:00:00"
                },
                {
                    "id": "3",
                    "name": "Verified Customer",
                    "rating": 10,
                    "date": "5 days ago", 
                    "text": "Booked on day of posting and completed within 2 hours of booking",
                    "service": "Dispose of thorny bush",
                    "postcode": "SW16",
                    "lat": 51.4352,
                    "lng": -0.1205,
                    "images": [],
                    "created_at": "2024-01-01T00:00:00"
                },
                {
                    "id": "4",
                    "name": "Verified Customer", 
                    "rating": 9,
                    "date": "6 days ago",
                    "text": "PNM gardening were quick to quote from a photo and easy to communicate with. The two gardeners did a great job and cleared an overgrown garden really quickly and left no mess. Would recommend",
                    "service": "Small garden clearance", 
                    "postcode": "SW12",
                    "lat": 51.4648,
                    "lng": -0.1731,
                    "images": [],
                    "created_at": "2024-01-01T00:00:00"
                },
                {
                    "id": "5",
                    "name": "Verified Customer",
                    "rating": 10,
                    "date": "6 days ago",
                    "text": "Very good job, good communication and would use again.",
                    "service": "Ivy Removal",
                    "postcode": "SW10", 
                    "lat": 51.4892,
                    "lng": -0.1934,
                    "images": [],
                    "created_at": "2024-01-01T00:00:00"
                }
            ]
            # DISABLED - Reviews are loaded via add_all_reviews.py script
            # await self.db.reviews.insert_many(all_reviews)
            logger.info(f"Review seeding disabled - use add_all_reviews.py script")
            
            # Seed gallery images
            gallery_data = [
                {
                    "id": "1",
                    "src": "https://images.unsplash.com/photo-1597201278257-3687be27d954?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHw0fHxsYW5kc2NhcGluZ3xlbnwwfHx8fDE3NTQ4Mzc5NDJ8MA&ixlib=rb-4.1.0&q=85",
                    "title": "Beautiful Flower Garden",
                    "category": "Garden Design",
                    "created_at": "2024-01-01T00:00:00"
                },
                {
                    "id": "2",
                    "src": "https://images.pexels.com/photos/5905352/pexels-photo-5905352.jpeg",
                    "title": "Professional Garden Work",
                    "category": "Maintenance",
                    "created_at": "2024-01-01T00:00:00"
                },
                {
                    "id": "3",
                    "src": "https://images.pexels.com/photos/1301856/pexels-photo-1301856.jpeg",
                    "title": "Tree Surgery",
                    "category": "Tree Care",
                    "created_at": "2024-01-01T00:00:00"
                },
                {
                    "id": "4",
                    "src": "https://images.unsplash.com/photo-1458245201577-fc8a130b8829?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHwzfHxsYW5kc2NhcGluZ3xlbnwwfHx8fDE3NTQ4Mzc5NDJ8MA&ixlib=rb-4.1.0&q=85",
                    "title": "Lawn Maintenance",
                    "category": "Lawn Care",
                    "created_at": "2024-01-01T00:00:00"
                }
            ]
            
            await self.db.gallery.insert_many(gallery_data)
            
            logger.info("Database seeded successfully with initial data")
            
        except Exception as e:
            logger.error(f"Error seeding database: {e}")
            raise e