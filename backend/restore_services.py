"""
Restore all original services to the database
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

async def restore_services():
    ROOT_DIR = Path('/app/backend')
    load_dotenv(ROOT_DIR / '.env')
    
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    # All 9 original services
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
            "title": "Garden Design",
            "description": "Creative garden design services tailored to your space and preferences. From concept to completion, we transform outdoor spaces into beautiful, functional gardens.",
            "image": "https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHwxfHxnYXJkZW4lMjBkZXNpZ258ZW58MHx8fHwxNzU0ODM3OTQyfDA&ixlib=rb-4.1.0&q=85",
            "features": ["Custom Design Plans", "Plant Selection", "Landscape Architecture", "3D Visualization", "Full Installation"],
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        },
        {
            "id": "7",
            "title": "Soft Landscaping",
            "description": "Expert soft landscaping including planting schemes, flower beds, borders, and seasonal displays. Professional plant selection and installation to create stunning garden features.",
            "image": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHw2fHxwbGFudGluZ3xlbnwwfHx8fDE3NTQ4Mzc5NDJ8MA&ixlib=rb-4.1.0&q=85",
            "features": ["Plant Selection", "Flower Bed Design", "Seasonal Planting", "Bulb Planting", "Plant Care Advice"],
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        },
        {
            "id": "8",
            "title": "Hard Landscaping",
            "description": "Professional hard landscaping including patios, pathways, driveways, and retaining walls. Quality construction using premium materials for long-lasting results.",
            "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHw1fHxwYXRpb3xlbnwwfHx8fDE3NTQ4Mzc5NDJ8MA&ixlib=rb-4.1.0&q=85",
            "features": ["Patio Installation", "Pathway Construction", "Driveway Paving", "Retaining Walls", "Stone & Block Paving"],
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        },
        {
            "id": "9",
            "title": "Pruning",
            "description": "Expert pruning services for trees, shrubs, and plants. Professional techniques to promote healthy growth and maintain the shape and size of your plants.",
            "image": "https://images.unsplash.com/photo-1515150144380-bca9f1650ed9?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzd8MHwxfHNlYXJjaHwyfHxnYXJkZW5pbmd8ZW58MHx8fHwxNzU0ODM3OTM2fDA&ixlib=rb-4.1.0&q=85",
            "features": ["Tree Pruning", "Shrub Pruning", "Seasonal Pruning", "Health Assessment", "Shape Maintenance"],
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        }
    ]
    
    # Delete existing services
    delete_result = await db.services.delete_many({})
    print(f"Deleted {delete_result.deleted_count} existing services")
    
    # Insert all 9 services
    result = await db.services.insert_many(services_data)
    print(f"✅ Restored {len(result.inserted_ids)} services")
    
    # Verify
    services = await db.services.find().to_list(100)
    print(f"\nServices now in database: {len(services)}")
    for s in services:
        print(f"  - {s['title']}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(restore_services())
