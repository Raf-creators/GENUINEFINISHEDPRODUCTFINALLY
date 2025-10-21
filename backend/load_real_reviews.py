"""
Load real scraped Checkatrade reviews into MongoDB with geocoding
"""
import asyncio
import json
import logging
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Postcode to coordinates mapping for London SW postcodes
POSTCODE_COORDS = {
    'CR4': (51.3827, -0.1137),  # Mitcham
    'SW2': (51.4500, -0.1167),  # Brixton
    'SW4': (51.4627, -0.1460),  # Clapham
    'SW10': (51.4892, -0.1934), # West Brompton
    'SW11': (51.4647, -0.1634), # Battersea
    'SW12': (51.4648, -0.1731), # Balham
    'SW15': (51.4574, -0.2214), # Putney
    'SW16': (51.4325, -0.1221), # Streatham
    'SW17': (51.4322, -0.1517), # Tooting
    'SW18': (51.4584, -0.1947), # Wandsworth
    'SW19': (51.4214, -0.1878), # Wimbledon
}

async def load_real_checkatrade_reviews():
    """Load real scraped reviews from JSON file into MongoDB"""
    
    # Load environment
    ROOT_DIR = Path(__file__).parent
    load_dotenv(ROOT_DIR / '.env')
    
    # Connect to MongoDB
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    try:
        # Load scraped reviews
        reviews_file = '/app/backend/checkatrade_reviews.json'
        with open(reviews_file, 'r') as f:
            scraped_reviews = json.load(f)
        
        logger.info(f"Loaded {len(scraped_reviews)} reviews from {reviews_file}")
        
        # Transform reviews for MongoDB
        mongo_reviews = []
        for review in scraped_reviews:
            # Get coordinates for postcode
            postcode = review.get('postcode', 'SW11')
            lat, lng = POSTCODE_COORDS.get(postcode, (51.4647, -0.1634))  # Default to Battersea
            
            # Create review document
            review_doc = {
                'id': str(uuid.uuid4()),
                'name': review.get('customer_name', 'Anonymous'),
                'rating': review.get('rating', 10),
                'date': review.get('date', 'Recently'),
                'text': review.get('text', ''),
                'service': review.get('service', 'Garden Service'),
                'postcode': postcode,
                'lat': lat,
                'lng': lng,
                'images': review.get('images', []),
                'approved': True,
                'created_at': '2024-01-01T00:00:00'
            }
            
            mongo_reviews.append(review_doc)
            logger.info(f"Prepared review: {review_doc['service'][:50]} - {postcode} ({lat}, {lng})")
        
        # Clear existing reviews
        delete_result = await db.reviews.delete_many({})
        logger.info(f"Deleted {delete_result.deleted_count} existing reviews")
        
        # Insert new reviews
        if mongo_reviews:
            result = await db.reviews.insert_many(mongo_reviews)
            logger.info(f"✅ Inserted {len(result.inserted_ids)} real Checkatrade reviews")
        
        # Print summary
        print("\n📊 Review Import Summary:")
        print(f"Total reviews imported: {len(mongo_reviews)}")
        print(f"Reviews with images: {sum(1 for r in mongo_reviews if r.get('images'))}")
        print(f"Average rating: {sum(r['rating'] for r in mongo_reviews) / len(mongo_reviews):.1f}/10")
        print(f"\nPostcodes covered:")
        for pc in sorted(set(r['postcode'] for r in mongo_reviews)):
            count = sum(1 for r in mongo_reviews if r['postcode'] == pc)
            print(f"  {pc}: {count} reviews")
        
        return len(mongo_reviews)
        
    except Exception as e:
        logger.error(f"Error loading reviews: {e}")
        raise
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(load_real_checkatrade_reviews())
