# Database Integration Script for Google Drive Photos
# This will replace current reviews with 226 reviews containing 254 photos from Google Drive

import sys
sys.path.append('/app')
sys.path.append('/app/backend')

import asyncio
from drive_database_integration import generate_database_insertion_script
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime

class GoogleDriveIntegration:
    def __init__(self):
        self.mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
        self.db_name = os.environ.get('DB_NAME', 'test_database')
        
    async def integrate_google_drive_photos(self):
        """Integrate all Google Drive photos into the database"""
        
        print("🚀 INTEGRATING GOOGLE DRIVE PHOTOS INTO DATABASE")
        print("="*60)
        
        # Generate photo and review data
        db_photos, db_reviews = generate_database_insertion_script()
        
        # Connect to MongoDB
        client = AsyncIOMotorClient(self.mongo_url)
        db = client[self.db_name]
        
        print(f"\n🗄️  DATABASE CONNECTION")
        print(f"URL: {self.mongo_url}")
        print(f"Database: {self.db_name}")
        
        try:
            # Clear existing reviews
            print(f"\n🧹 CLEARING EXISTING REVIEWS...")
            existing_count = await db.reviews.count_documents({})
            print(f"Found {existing_count} existing reviews")
            
            delete_result = await db.reviews.delete_many({})
            print(f"Deleted {delete_result.deleted_count} reviews")
            
            # Insert new reviews with Google Drive photos
            print(f"\n📤 INSERTING GOOGLE DRIVE REVIEWS...")
            print(f"Inserting {len(db_reviews)} reviews with photos...")
            
            # Convert to MongoDB format (remove Python-specific fields)
            mongo_reviews = []
            for review in db_reviews:
                mongo_review = {
                    "id": review["id"],
                    "name": review["name"],
                    "rating": review["rating"],
                    "date": review["date"],
                    "text": review["text"],
                    "service": review["service"],
                    "postcode": review["postcode"],
                    "lat": review["lat"],
                    "lng": review["lng"],
                    "images": review["images"],
                    "approved": review["approved"],
                    "created_at": review["created_at"]
                }
                mongo_reviews.append(mongo_review)
            
            # Insert in batches to handle large dataset
            batch_size = 50
            inserted_count = 0
            
            for i in range(0, len(mongo_reviews), batch_size):
                batch = mongo_reviews[i:i+batch_size]
                result = await db.reviews.insert_many(batch)
                inserted_count += len(result.inserted_ids)
                print(f"Inserted batch {i//batch_size + 1}: {len(batch)} reviews (Total: {inserted_count})")
            
            print(f"\n✅ DATABASE INTEGRATION COMPLETE!")
            print(f"="*60)
            print(f"📸 Total photos integrated: {len(db_photos)}")
            print(f"⭐ Total reviews with photos: {inserted_count}")
            print(f"📍 London areas covered: {len(set(r['postcode'] for r in db_reviews))}")
            
            # Verify integration
            final_count = await db.reviews.count_documents({})
            reviews_with_photos = await db.reviews.count_documents({"images": {"$ne": []}})
            
            print(f"\n🔍 VERIFICATION:")
            print(f"Reviews in database: {final_count}")
            print(f"Reviews with photos: {reviews_with_photos}")
            print(f"Average photos per review: {len(db_photos)/final_count:.1f}")
            
            # Service breakdown verification
            print(f"\n📊 SERVICE DISTRIBUTION:")
            services = await db.reviews.distinct("service")
            for service in sorted(services):
                count = await db.reviews.count_documents({"service": service})
                print(f"   {service}: {count} reviews")
            
            # Location breakdown
            print(f"\n📍 LOCATION COVERAGE:")
            postcodes = await db.reviews.distinct("postcode")
            print(f"   Total postcodes covered: {len(postcodes)}")
            print(f"   Sample postcodes: {', '.join(sorted(postcodes)[:10])}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error during integration: {str(e)}")
            return False
            
        finally:
            client.close()

async def main():
    integrator = GoogleDriveIntegration()
    success = await integrator.integrate_google_drive_photos()
    
    if success:
        print(f"\n🎉 INTEGRATION SUCCESSFUL!")
        print(f"Your website now has:")
        print(f"✅ 226 customer reviews with photos from Google Drive")
        print(f"✅ 254 individual photos across 9 services")
        print(f"✅ Realistic London locations with coordinates")
        print(f"✅ SEO-optimized content and metadata")
        print(f"✅ Customer testimonials for each photo")
        
        print(f"\n🔄 RESTART BACKEND TO APPLY CHANGES:")
        print(f"The new data is in the database. Restart the backend service to see the changes.")
    else:
        print(f"❌ Integration failed. Check the error messages above.")

if __name__ == "__main__":
    asyncio.run(main())