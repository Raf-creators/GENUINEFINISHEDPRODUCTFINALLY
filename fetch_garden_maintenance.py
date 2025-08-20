#!/usr/bin/env python3
"""
Fetch Garden Maintenance photos from specific Google Drive folder
Folder ID: 1VElZ2qjL_Yu-I9tHCRgxWe7qD7IcFXrn
"""

import sys
sys.path.append('/app')
import json
from google_drive_api import RealGoogleDriveAPI

def fetch_garden_maintenance_photos():
    """Fetch all photos from the Garden Maintenance Google Drive folder"""
    
    try:
        print("🔗 FETCHING GARDEN MAINTENANCE PHOTOS FROM GOOGLE DRIVE...")
        print("📁 Folder: https://drive.google.com/drive/folders/1VElZ2qjL_Yu-I9tHCRgxWe7qD7IcFXrn")
        
        # Initialize Google Drive API
        drive_api = RealGoogleDriveAPI()
        
        # Garden Maintenance folder ID from your link
        garden_maintenance_folder_id = "1VElZ2qjL_Yu-I9tHCRgxWe7qD7IcFXrn"
        
        # Get all photos from this specific folder
        results = drive_api.service.files().list(
            q=f"'{garden_maintenance_folder_id}' in parents and (mimeType contains 'image/' or name contains '.jpg' or name contains '.jpeg' or name contains '.png' or name contains '.heic')",
            fields='files(id, name, size, createdTime, mimeType)',
            orderBy='name'
        ).execute()
        
        photos = results.get('files', [])
        
        print(f"📸 Found {len(photos)} photos in Garden Maintenance folder:")
        
        # Convert to gallery format
        garden_maintenance_photos = []
        
        for i, photo in enumerate(photos):
            photo_data = {
                'id': f"garden_maintenance_gd_{i + 1}",
                'name': photo['name'],
                'url': f"https://drive.google.com/uc?export=view&id={photo['id']}",
                'thumbnail_url': f"https://drive.google.com/thumbnail?id={photo['id']}&sz=w400",
                'service': 'Garden Maintenance',
                'description': f"Professional garden maintenance work in Balham - {photo['name']}",
                'size': photo.get('size', ''),
                'mime_type': photo.get('mimeType', ''),
                'created': photo.get('createdTime', ''),
                'drive_id': photo['id']
            }
            
            garden_maintenance_photos.append(photo_data)
            print(f"   {i+1}. {photo['name']} (ID: {photo['id']})")
        
        return garden_maintenance_photos
        
    except Exception as e:
        print(f"❌ Error fetching Garden Maintenance photos: {e}")
        return []

def update_gallery_with_real_photos():
    """Update the gallery with real Garden Maintenance photos from Google Drive"""
    
    # Fetch the photos
    garden_maintenance_photos = fetch_garden_maintenance_photos()
    
    if not garden_maintenance_photos:
        print("❌ No photos fetched, keeping existing photos")
        return False
    
    try:
        # Load current gallery data
        with open('/app/frontend/public/real_gallery_data.json', 'r') as f:
            gallery_data = json.load(f)
        
        # Update Garden Maintenance with real Google Drive photos
        if 'Garden Maintenance' in gallery_data:
            gallery_data['Garden Maintenance']['photos'] = garden_maintenance_photos
            gallery_data['Garden Maintenance']['photo_count'] = len(garden_maintenance_photos)
            
            print(f"✅ Updated Garden Maintenance with {len(garden_maintenance_photos)} real Google Drive photos")
        
        # Save updated gallery data
        with open('/app/frontend/public/real_gallery_data.json', 'w') as f:
            json.dump(gallery_data, f, indent=2)
        
        with open('/app/real_gallery_data.json', 'w') as f:
            json.dump(gallery_data, f, indent=2)
        
        print("\n✅ GALLERY UPDATED WITH REAL GARDEN MAINTENANCE PHOTOS!")
        print(f"📸 Total Garden Maintenance photos: {len(garden_maintenance_photos)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating gallery: {e}")
        return False

if __name__ == "__main__":
    success = update_gallery_with_real_photos()
    if success:
        print("\n🎉 SUCCESS: Garden Maintenance photos updated from Google Drive!")
    else:
        print("\n❌ FAILED: Could not update Garden Maintenance photos")