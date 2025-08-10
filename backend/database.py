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
                    "description": "Whether you require a complete garden clearing, one-off visit or regular maintenance visits to ensure a great looking garden all year round. We consist of a small team of gardeners and are not a franchise company.",
                    "image": "https://images.unsplash.com/photo-1621460248083-6271cc4437a8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzd8MHwxfHNlYXJjaHwxfHxnYXJkZW5pbmd8ZW58MHx8fHwxNzU0ODM3OTM2fDA&ixlib=rb-4.1.0&q=85",
                    "features": ["Hedge Trimming", "Leaf Clearance", "Pruning", "Weeding", "Seasonal Clean-ups"],
                    "created_at": "2024-01-01T00:00:00",
                    "updated_at": "2024-01-01T00:00:00"
                },
                {
                    "id": "2",
                    "title": "Lawn Care Services",
                    "description": "We provide professional lawn care services with cost effective solutions for any lawn problems. From mowing to seeding, we ensure your lawn stays healthy and beautiful all year round.",
                    "image": "https://images.unsplash.com/photo-1458245201577-fc8a130b8829?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHwzfHxsYW5kc2NhcGluZ3xlbnwwfHx8fDE3NTQ4Mzc5NDJ8MA&ixlib=rb-4.1.0&q=85",
                    "features": ["Lawn Mowing", "Edging", "Weed Treatment", "Overseeding", "Lawn Repair"],
                    "created_at": "2024-01-01T00:00:00",
                    "updated_at": "2024-01-01T00:00:00"
                },
                {
                    "id": "3",
                    "title": "Hedge Trimming & Planting",
                    "description": "Professional hedge trimming and planting services. We offer all types of hedge services whether it's replacing an existing hedge, planting a new hedge, or maintaining your current hedges.",
                    "image": "https://images.unsplash.com/photo-1605117882932-f9e32b03fea9?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHwyfHxsYW5kc2NhcGluZ3xlbnwwfHx8fDE3NTQ4Mzc5NDJ8MA&ixlib=rb-4.1.0&q=85",
                    "features": ["Hedge Trimming", "Hedge Planting", "Topiary Work", "Privacy Screens", "Hedge Removal"],
                    "created_at": "2024-01-01T00:00:00",
                    "updated_at": "2024-01-01T00:00:00"
                },
                {
                    "id": "4",
                    "title": "Turfing Services",
                    "description": "Lawn turfing in Balham is perfect if you're looking to improve the look of your lawn areas. All lawn turf we supply is sourced from premium suppliers for guaranteed quality.",
                    "image": "https://images.pexels.com/photos/5905352/pexels-photo-5905352.jpeg",
                    "features": ["New Lawn Installation", "Turf Laying", "Ground Preparation", "Artificial Grass", "Lawn Renovation"],
                    "created_at": "2024-01-01T00:00:00",
                    "updated_at": "2024-01-01T00:00:00"
                },
                {
                    "id": "5",
                    "title": "Pressure Washing",
                    "description": "The almost instant way to improve the look and feel of your outdoor space is by booking us to carry out professional pressure washing for your patios, driveways, and outdoor areas.",
                    "image": "https://images.unsplash.com/photo-1515150144380-bca9f1650ed9?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzd8MHwxfHNlYXJjaHwyfHxnYXJkZW5pbmd8ZW58MHx8fHwxNzU0ODM3OTM2fDA&ixlib=rb-4.1.0&q=85",
                    "features": ["Patio Cleaning", "Driveway Washing", "Fence Cleaning", "Decking Restoration", "Building Exterior"],
                    "created_at": "2024-01-01T00:00:00",
                    "updated_at": "2024-01-01T00:00:00"
                },
                {
                    "id": "6",
                    "title": "Tree Surgery & Pruning",
                    "description": "Professional tree surgery services including pruning, crown reduction, and tree removal. Our certified arborists ensure the health and safety of your trees while maintaining their beauty.",
                    "image": "https://images.pexels.com/photos/1301856/pexels-photo-1301856.jpeg",
                    "features": ["Tree Pruning", "Crown Reduction", "Tree Removal", "Stump Grinding", "Emergency Tree Services"],
                    "created_at": "2024-01-01T00:00:00",
                    "updated_at": "2024-01-01T00:00:00"
                }
            ]
            
            await self.db.services.insert_many(services_data)
            
            # Seed reviews
            reviews_data = [
                {
                    "id": "1",
                    "name": "Sarah Johnson",
                    "rating": 5,
                    "date": "15 Dec 2024",
                    "text": "Absolutely brilliant service! The PNM team transformed our overgrown back garden in Balham. They were professional, punctual, and cleaned up everything perfectly. Will definitely use them again.",
                    "service": "Garden Maintenance",
                    "approved": True,
                    "created_at": "2024-12-15T00:00:00"
                },
                {
                    "id": "2",
                    "name": "Michael Thompson",
                    "rating": 5,
                    "date": "08 Dec 2024",
                    "text": "Outstanding work on our hedge trimming. The team was efficient, friendly, and left our garden looking pristine. Great value for money and excellent customer service throughout.",
                    "service": "Hedge Trimming",
                    "approved": True,
                    "created_at": "2024-12-08T00:00:00"
                },
                {
                    "id": "3",
                    "name": "Emma Wilson",
                    "rating": 5,
                    "date": "02 Dec 2024",
                    "text": "We had PNM Gardeners install a new lawn and the results are fantastic! The preparation work was thorough and the new turf looks amazing. Highly recommend their turfing services.",
                    "service": "Turfing Services",
                    "approved": True,
                    "created_at": "2024-12-02T00:00:00"
                },
                {
                    "id": "4",
                    "name": "David Brown",
                    "rating": 5,
                    "date": "28 Nov 2024",
                    "text": "Excellent pressure washing service for our patio and driveway. The difference is remarkable - looks like new! Professional team and fair pricing. Will book them for regular maintenance.",
                    "service": "Pressure Washing",
                    "approved": True,
                    "created_at": "2024-11-28T00:00:00"
                },
                {
                    "id": "5",
                    "name": "Lisa Parker",
                    "rating": 5,
                    "date": "21 Nov 2024",
                    "text": "PNM Gardeners have been maintaining our garden for 6 months now. Consistently excellent service, always on time, and our garden has never looked better. True professionals!",
                    "service": "Garden Maintenance",
                    "approved": True,
                    "created_at": "2024-11-21T00:00:00"
                },
                {
                    "id": "6",
                    "name": "James Mitchell",
                    "rating": 5,
                    "date": "15 Nov 2024",
                    "text": "Brilliant tree pruning service. The team removed dangerous overhanging branches safely and tidied everything up. Very knowledgeable about tree care and reasonably priced.",
                    "service": "Tree Surgery",
                    "approved": True,
                    "created_at": "2024-11-15T00:00:00"
                }
            ]
            
            await self.db.reviews.insert_many(reviews_data)
            
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