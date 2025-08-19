#!/usr/bin/env python3
"""
Manually seed the database with updated services
"""
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient

async def main():
    try:
        # Connect to MongoDB
        mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017/pnm_gardeners')
        print(f"Connecting to: {mongo_url}")
        
        client = AsyncIOMotorClient(mongo_url)
        db = client.get_default_database()
        
        # Clear existing services
        result = await db.services.delete_many({})
        print(f"Cleared {result.deleted_count} existing services")
        
        # New services data with your uploaded images
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
        
        # Insert new services
        result = await db.services.insert_many(services_data)
        print(f"Inserted {len(result.inserted_ids)} services with your uploaded images!")
        
        # Verify by checking the first few
        first_service = await db.services.find_one({"id": "1"})
        if first_service:
            print(f"✅ Garden Maintenance: {first_service['image'][:60]}...")
        
        second_service = await db.services.find_one({"id": "2"})
        if second_service:
            print(f"✅ Garden Clearance: {second_service['image'][:60]}...")
            
        client.close()
        print("✅ Database seeding completed successfully!")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())