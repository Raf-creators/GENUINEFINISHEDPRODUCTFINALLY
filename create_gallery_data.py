#!/usr/bin/env python3
"""
Create Real Gallery Data for PNM Gardeners
Fetches all photos from Google Drive and creates gallery data file
"""

import json
import sys
import os
sys.path.append('/app')

from google_drive_api import RealGoogleDriveAPI

def create_gallery_data_file():
    """Create the real gallery data file for the frontend"""
    
    print("🚀 Creating real gallery data from Google Drive...")
    
    # Initialize Google Drive API
    drive_api = RealGoogleDriveAPI()
    
    # Get all service albums with real photos
    albums = drive_api.get_all_service_albums()
    
    if not albums:
        print("❌ Failed to retrieve albums from Google Drive")
        return False
    
    # Format the data for frontend consumption
    formatted_albums = {}
    
    for service_name, album in albums.items():
        # Convert photos to frontend format
        frontend_photos = []
        for i, photo in enumerate(album['photos']):
            frontend_photo = {
                'id': f"{service_name.lower().replace(' ', '_')}_{i + 1}",
                'name': photo['name'],
                'url': photo['direct_url'],
                'thumbnail_url': photo['thumbnail_url'], 
                'service': service_name,
                'description': f"Professional {service_name.lower()} work",
                'size': photo.get('size', ''),
                'mime_type': photo.get('mime_type', ''),
                'created': photo.get('created', ''),
                'drive_id': photo['id']
            }
            frontend_photos.append(frontend_photo)
        
        # Create album data
        formatted_albums[service_name] = {
            'service_name': service_name,
            'photo_count': album['photo_count'],
            'description': album['description'],
            'cover_photo': album['cover_photo'],
            'photos': frontend_photos
        }
    
    # Save to JSON files
    gallery_data_path = '/app/frontend/public/real_gallery_data.json'
    backend_gallery_data_path = '/app/real_gallery_data.json'
    
    try:
        # Save to frontend public directory
        with open(gallery_data_path, 'w') as f:
            json.dump(formatted_albums, f, indent=2)
        
        # Also save to backend for API serving
        with open(backend_gallery_data_path, 'w') as f:
            json.dump(formatted_albums, f, indent=2)
        
        total_photos = sum(album['photo_count'] for album in formatted_albums.values())
        
        print(f"✅ Gallery data created successfully!")
        print(f"📁 Frontend file: {gallery_data_path}")
        print(f"📁 Backend file: {backend_gallery_data_path}")
        print(f"📸 Total photos: {total_photos}")
        print(f"🗂️ Albums created: {len(formatted_albums)}")
        
        # Show album breakdown
        print(f"\n📊 ALBUMS BREAKDOWN:")
        for service_name, album in formatted_albums.items():
            print(f"   {service_name}: {album['photo_count']} photos")
            if album['photos']:
                print(f"      Sample URL: {album['photos'][0]['url']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to save gallery data: {e}")
        return False

if __name__ == "__main__":
    success = create_gallery_data_file()
    if success:
        print(f"\n🎉 SUCCESS! Real gallery data is ready for use.")
        print(f"💡 The frontend will now display real Google Drive photos.")
    else:
        print(f"\n❌ FAILED! Could not create gallery data.")
        sys.exit(1)