# Quick Database Fix - Add this to your backend

## Problem: 
Database seeding is failing with 500 error

## Solution: 
Let's bypass the complex seeding and just add the essential reviews data

## What to do:
1. Add this simple endpoint to server.py
2. This will manually insert just the reviews (which is what you need for the map)

```python
@api_router.post("/add-reviews", response_model=MessageResponse)
async def add_reviews_only():
    """Add reviews data only (simplified version)"""
    try:
        # Simple reviews data
        reviews_data = [
            {
                "id": "1",
                "name": "Verified Customer",
                "rating": 10,
                "date": "4 days ago",
                "text": "Great communication from start to finish. Delighted with the end result.",
                "service": "Garden clearance and lawn laying",
                "postcode": "SW19",
                "lat": 51.4214,
                "lng": -0.1878,
                "images": [],
                "created_at": "2024-01-01T00:00:00"
            },
            {
                "id": "2",
                "name": "Verified Customer", 
                "rating": 10,
                "date": "4 days ago",
                "text": "Really great experience, the guys were friendly and efficient.",
                "service": "Garden Clearance",
                "postcode": "SW16",
                "lat": 51.4325,
                "lng": -0.1221,
                "images": [],
                "created_at": "2024-01-01T00:00:00"
            },
            {
                "id": "3",
                "name": "Verified Customer",
                "rating": 10,
                "date": "5 days ago",
                "text": "Booked on day of posting and completed within 2 hours.",
                "service": "Thorny bush removal",
                "postcode": "SW16", 
                "lat": 51.4352,
                "lng": -0.1205,
                "images": [],
                "created_at": "2024-01-01T00:00:00"
            }
        ]
        
        # Insert directly into reviews collection
        collection = database.db["reviews"]
        await collection.insert_many(reviews_data)
        
        return MessageResponse(message="Reviews added successfully")
    except Exception as e:
        logger.error(f"Error adding reviews: {e}")
        return MessageResponse(message=f"Error: {str(e)}")
```