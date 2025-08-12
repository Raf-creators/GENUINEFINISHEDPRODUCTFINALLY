# Real Google Drive Photos for Gallery
# This will serve the actual photos from your Google Drive folders

import json
import asyncio
import sys
sys.path.append('/app')
from google_drive_api import RealGoogleDriveAPI

def create_real_gallery_data():
    """Create gallery data with real Google Drive photos"""
    
    print("🔄 CREATING REAL GALLERY DATA FROM GOOGLE DRIVE")
    print("="*60)
    
    # Get real photos from Google Drive
    drive_api = RealGoogleDriveAPI()
    albums = drive_api.get_all_service_albums()
    
    if not albums:
        print("❌ No albums found. Check folder permissions.")
        return None
    
    # Convert to JSON format for React
    gallery_data = {}
    total_photos = 0
    
    for service_name, album in albums.items():
        # Create photos array with real Google Drive URLs
        photos = []
        for i, photo in enumerate(album['photos']):
            photos.append({
                'id': photo['id'],
                'name': photo['name'],
                'url': photo['direct_url'],  # Direct Google Drive image URL
                'thumbnail_url': photo['thumbnail_url'],  # Google Drive thumbnail
                'service': service_name,
                'description': f"Professional {service_name.lower()} work - {photo['name']}",
                'size': photo.get('size', 0),
                'created': photo.get('created', ''),
                'file_type': photo.get('mime_type', '').split('/')[-1] if photo.get('mime_type') else 'image'
            })
        
        gallery_data[service_name] = {
            'service_name': service_name,
            'photo_count': len(photos),
            'description': album['description'],
            'cover_photo': album['cover_photo'],
            'photos': photos
        }
        
        total_photos += len(photos)
        print(f"✅ {service_name}: {len(photos)} real photos")
    
    print(f"\n🎉 TOTAL REAL PHOTOS: {total_photos}")
    
    # Save to file for React to use
    with open('/app/frontend/src/real_gallery_data.json', 'w') as f:
        json.dump(gallery_data, f, indent=2)
    
    print(f"💾 Real gallery data saved to real_gallery_data.json")
    
    return gallery_data

if __name__ == "__main__":
    create_real_gallery_data()