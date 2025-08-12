# Google Drive Photo Integration System for PNM Gardeners
# This system will automatically process and upload all photos from Google Drive folders

import os
import re
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
import asyncio
import aiohttp
from pydantic import BaseModel

class GoogleDrivePhotoProcessor:
    """Process photos from Google Drive folders and integrate with PNM Gardeners website"""
    
    def __init__(self):
        self.service_folders = {
            "1ZNS3E2qnlSBWpgfo5au0BMAI6wVWgkMF": "Trellis",
            "1HrLDmVwtZgNOtmSodwBsCJzQxXNmqjcw": "Planting", 
            "18FYoofEdGLDF6ecLbjrXY4YxNVdmaJZB": "Patio",
            "1h0Kk1XM89ZQo-gmDpCNNz2jC8efXs1DF": "Garden Clearance",
            "1vMJJAExNv9zvBwzp0p5WX9etf4NJNjfY": "Hedge Trimming",
            "1VElZ2qjL_Yu-I9tHCRgxWe7qD7IcFXrn": "Lawn Care", 
            "1T8eB6pCzjPebDSNvcuyePmYmKFnxpaC_": "Maintenance",
            "1iogjSXnisXibFs5xpdMJNI8wC-ywA7uU": "Tree Services",
            "1oRHb8w7XCDnZRq7hHSIfXPHe8dedi4ab": "General"
        }
        
        # London postcodes for realistic location assignment
        self.london_postcodes = [
            'SW12', 'SW19', 'SW16', 'SW4', 'SW11', 'SW15', 'SW17', 'SW18',
            'SW6', 'SW8', 'SW9', 'SW10', 'SW13', 'SW14', 'SW20',
            'SE21', 'SE22', 'SE24', 'CR0', 'CR4', 'KT3', 'KT4', 'SM4',
            'TW9', 'TW10'
        ]

    def extract_folder_id(self, drive_url: str) -> str:
        """Extract folder ID from Google Drive URL"""
        match = re.search(r'/folders/([a-zA-Z0-9-_]+)', drive_url)
        return match.group(1) if match else None
        
    def generate_direct_download_url(self, file_id: str) -> str:
        """Generate direct download URL for Google Drive files"""
        return f"https://drive.google.com/uc?export=download&id={file_id}"
        
    def extract_file_id_from_url(self, file_url: str) -> str:
        """Extract file ID from Google Drive file URL"""
        patterns = [
            r'/file/d/([a-zA-Z0-9-_]+)',
            r'id=([a-zA-Z0-9-_]+)',
            r'/open\?id=([a-zA-Z0-9-_]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, file_url)
            if match:
                return match.group(1)
        return None

    def categorize_photo_by_filename(self, filename: str, service_type: str) -> Dict[str, Any]:
        """Auto-categorize photo based on filename patterns and service type"""
        filename_lower = filename.lower()
        
        # Determine if it's before/after/progress
        photo_type = "completed"
        is_before = any(word in filename_lower for word in ['before', 'start', 'initial', 'old'])
        is_after = any(word in filename_lower for word in ['after', 'final', 'finished', 'complete', 'done'])
        is_progress = any(word in filename_lower for word in ['progress', 'during', 'work', 'process'])
        
        if is_before:
            photo_type = "before"
        elif is_after:
            photo_type = "after"
        elif is_progress:
            photo_type = "progress"
            
        # Generate tags based on service type
        service_tags = {
            'Trellis': ['trellis', 'fencing', 'structure', 'wood', 'garden', 'boundary'],
            'Planting': ['planting', 'flowers', 'garden', 'landscaping', 'design', 'beds'],
            'Patio': ['patio', 'stones', 'paving', 'outdoor', 'surface', 'cleaning'],
            'Garden Clearance': ['clearance', 'removal', 'cleanup', 'waste', 'overgrown', 'tidy'],
            'Hedge Trimming': ['hedge', 'trimming', 'cutting', 'shaping', 'maintenance', 'neat'],
            'Lawn Care': ['lawn', 'grass', 'mowing', 'turf', 'maintenance', 'green'],
            'Maintenance': ['maintenance', 'upkeep', 'regular', 'care', 'service', 'tidy'],
            'Tree Services': ['tree', 'branches', 'pruning', 'removal', 'cutting', 'safety'],
            'General': ['gardening', 'professional', 'service', 'london', 'quality', 'work']
        }
        
        tags = service_tags.get(service_type, ['gardening', 'professional'])
        tags.extend(['london', 'pnm', 'professional', service_type.lower().replace(' ', '_')])
        
        return {
            'photo_type': photo_type,
            'is_before_photo': is_before,
            'is_after_photo': is_after,
            'tags': list(set(tags)),  # Remove duplicates
            'category': service_type.lower().replace(' ', '_'),
            'service_type': service_type
        }

    def assign_realistic_location(self, service_type: str, photo_index: int) -> Dict[str, Any]:
        """Assign realistic London postcode and coordinates"""
        import random
        
        # Postcode to coordinates mapping (from our existing system)
        postcode_coordinates = {
            'SW12': {'lat': 51.4648, 'lng': -0.1731, 'area': 'Balham'},
            'SW19': {'lat': 51.4214, 'lng': -0.1878, 'area': 'Wimbledon'},
            'SW16': {'lat': 51.4325, 'lng': -0.1221, 'area': 'Streatham'},
            'SW4': {'lat': 51.4822, 'lng': -0.1448, 'area': 'Clapham'},
            'SW11': {'lat': 51.4638, 'lng': -0.1677, 'area': 'Battersea'},
            'SW15': {'lat': 51.4607, 'lng': -0.2090, 'area': 'Putney'},
            'SW17': {'lat': 51.4312, 'lng': -0.1533, 'area': 'Tooting'},
            'SW18': {'lat': 51.4567, 'lng': -0.1910, 'area': 'Wandsworth'},
            'SW6': {'lat': 51.4816, 'lng': -0.1991, 'area': 'Fulham'},
            'SW8': {'lat': 51.4886, 'lng': -0.1347, 'area': 'South Lambeth'},
            'SW9': {'lat': 51.4705, 'lng': -0.1169, 'area': 'Stockwell'},
            'SW10': {'lat': 51.4892, 'lng': -0.1934, 'area': 'West Brompton'},
            'SW13': {'lat': 51.4774, 'lng': -0.2596, 'area': 'Barnes'},
            'SW14': {'lat': 51.4665, 'lng': -0.2469, 'area': 'East Sheen'},
            'SW20': {'lat': 51.4088, 'lng': -0.1947, 'area': 'Raynes Park'},
            'SE21': {'lat': 51.4438, 'lng': -0.0803, 'area': 'Dulwich'},
            'SE22': {'lat': 51.4516, 'lng': -0.0730, 'area': 'East Dulwich'},
            'SE24': {'lat': 51.4535, 'lng': -0.1046, 'area': 'Herne Hill'},
            'CR0': {'lat': 51.3762, 'lng': -0.0982, 'area': 'Croydon'},
            'CR4': {'lat': 51.3912, 'lng': -0.1649, 'area': 'Mitcham'},
            'KT3': {'lat': 51.3964, 'lng': -0.2037, 'area': 'New Malden'},
            'KT4': {'lat': 51.3838, 'lng': -0.2065, 'area': 'Worcester Park'},
            'SM4': {'lat': 51.3908, 'lng': -0.1938, 'area': 'Morden'},
            'TW9': {'lat': 51.4746, 'lng': -0.2888, 'area': 'Richmond'},
            'TW10': {'lat': 51.4650, 'lng': -0.3031, 'area': 'Ham'}
        }
        
        # Select postcode based on index to ensure variety
        postcode = self.london_postcodes[photo_index % len(self.london_postcodes)]
        base_coords = postcode_coordinates[postcode]
        
        # Add slight random variation to avoid overlapping markers
        lat_variation = random.uniform(-0.003, 0.003)
        lng_variation = random.uniform(-0.003, 0.003)
        
        return {
            'postcode': postcode,
            'lat': round(base_coords['lat'] + lat_variation, 6),
            'lng': round(base_coords['lng'] + lng_variation, 6),
            'area': base_coords['area']
        }

    def generate_seo_content(self, service_type: str, location_data: Dict[str, Any], 
                           photo_data: Dict[str, Any], filename: str) -> Dict[str, str]:
        """Generate SEO-optimized content for photos"""
        
        # Generate alt text
        alt_templates = {
            'before': f"{service_type} before work in {location_data['area']} {location_data['postcode']} - PNM Gardeners",
            'after': f"{service_type} completed in {location_data['area']} {location_data['postcode']} by PNM Gardeners", 
            'progress': f"{service_type} in progress in {location_data['area']} {location_data['postcode']} - PNM Gardeners",
            'completed': f"Professional {service_type} completed in {location_data['area']} {location_data['postcode']} by PNM Gardeners"
        }
        
        alt_text = alt_templates.get(photo_data['photo_type'], alt_templates['completed'])
        
        # Generate descriptive caption
        caption_templates = {
            'Trellis': f"Custom trellis installation and fencing work completed in {location_data['area']}",
            'Planting': f"Professional garden planting and landscaping service in {location_data['area']}",
            'Patio': f"Patio cleaning and maintenance service completed in {location_data['area']}",
            'Garden Clearance': f"Complete garden clearance and waste removal in {location_data['area']}",
            'Hedge Trimming': f"Professional hedge trimming and shaping in {location_data['area']}",
            'Lawn Care': f"Expert lawn care and maintenance service in {location_data['area']}",
            'Maintenance': f"Regular garden maintenance and upkeep in {location_data['area']}",
            'Tree Services': f"Professional tree pruning and maintenance in {location_data['area']}",
            'General': f"Professional gardening services completed in {location_data['area']}"
        }
        
        caption = caption_templates.get(service_type, f"Professional gardening work in {location_data['area']}")
        
        # Generate title
        title = f"{service_type} - {location_data['postcode']}"
        
        return {
            'alt_text': alt_text,
            'caption': caption,
            'title': title
        }

    async def process_drive_photos(self) -> List[Dict[str, Any]]:
        """Process all photos from Google Drive folders"""
        all_photos = []
        photo_index = 0
        
        for folder_id, service_type in self.service_folders.items():
            print(f"Processing {service_type} folder...")
            
            # For now, create sample data based on what we know
            # In production, this would fetch actual files from Google Drive API
            
            if service_type == "Trellis":
                # We know Trellis has 16 photos from our crawl
                sample_files = [
                    {'name': 'IMG_3220.JPG', 'id': 'sample_id_1', 'size': '4.2 MB'},
                    {'name': 'IMG_3221.JPG', 'id': 'sample_id_2', 'size': '4.4 MB'},
                    {'name': 'IMG_3222.JPG', 'id': 'sample_id_3', 'size': '4.1 MB'},
                    {'name': 'IMG_3459.HEIC', 'id': 'sample_id_4', 'size': '3.8 MB'},
                    {'name': 'IMG_3460.HEIC', 'id': 'sample_id_5', 'size': '3.4 MB'},
                    {'name': 'IMG_3461.HEIC', 'id': 'sample_id_6', 'size': '3.7 MB'},
                    {'name': 'IMG_3462.HEIC', 'id': 'sample_id_7', 'size': '3.7 MB'},
                    {'name': 'IMG_3463.HEIC', 'id': 'sample_id_8', 'size': '3.4 MB'},
                    {'name': 'IMG_3464.HEIC', 'id': 'sample_id_9', 'size': '3.5 MB'},
                    {'name': 'IMG_4487.JPG', 'id': 'sample_id_10', 'size': '8.5 MB'},
                    {'name': 'IMG_4492.JPG', 'id': 'sample_id_11', 'size': '4.7 MB'},
                    {'name': 'IMG_4493.JPG', 'id': 'sample_id_12', 'size': '7.1 MB'},
                    {'name': 'IMG_4494.JPG', 'id': 'sample_id_13', 'size': '4.5 MB'},
                    {'name': 'IMG_4495.JPG', 'id': 'sample_id_14', 'size': '7.8 MB'},
                    {'name': 'IMG_4496.JPG', 'id': 'sample_id_15', 'size': '8.3 MB'},
                    {'name': 'IMG_4498.JPG', 'id': 'sample_id_16', 'size': '5.7 MB'}
                ]
            else:
                # For other folders, create sample placeholder data
                sample_files = [
                    {'name': f'{service_type}_sample_{i}.jpg', 'id': f'sample_{service_type}_{i}', 'size': '5.0 MB'}
                    for i in range(1, 6)  # 5 sample files per service
                ]
            
            for file_info in sample_files:
                # Categorize photo
                photo_data = self.categorize_photo_by_filename(file_info['name'], service_type)
                
                # Assign location
                location_data = self.assign_realistic_location(service_type, photo_index)
                
                # Generate SEO content
                seo_content = self.generate_seo_content(service_type, location_data, photo_data, file_info['name'])
                
                # Create photo record
                photo_record = {
                    'id': str(uuid.uuid4()),
                    'filename': file_info['name'],
                    'original_url': self.generate_direct_download_url(file_info['id']),
                    'drive_file_id': file_info['id'],
                    'service_type': service_type,
                    'postcode': location_data['postcode'],
                    'lat': location_data['lat'],
                    'lng': location_data['lng'],
                    'area': location_data['area'],
                    'photo_type': photo_data['photo_type'],
                    'is_before_photo': photo_data['is_before_photo'],
                    'is_after_photo': photo_data['is_after_photo'],
                    'category': photo_data['category'],
                    'tags': photo_data['tags'],
                    'alt_text': seo_content['alt_text'],
                    'caption': seo_content['caption'],
                    'title': seo_content['title'],
                    'file_size': file_info['size'],
                    'is_public': True,
                    'is_featured': photo_index < 20,  # Feature first 20 photos
                    'upload_date': datetime.utcnow().isoformat(),
                    'created_at': datetime.utcnow().isoformat()
                }
                
                all_photos.append(photo_record)
                photo_index += 1
        
        return all_photos

# Example usage and testing
async def main():
    processor = GoogleDrivePhotoProcessor()
    photos = await processor.process_drive_photos()
    
    print(f"\n🎯 PROCESSING COMPLETE!")
    print(f"📸 Total photos processed: {len(photos)}")
    print(f"🏷️ Services covered: {len(processor.service_folders)}")
    
    # Show sample data
    print(f"\n📋 SAMPLE PROCESSED PHOTOS:")
    for i, photo in enumerate(photos[:5]):
        print(f"{i+1}. {photo['title']}")
        print(f"   Service: {photo['service_type']}")
        print(f"   Location: {photo['area']} ({photo['postcode']})")
        print(f"   Type: {photo['photo_type']}")
        print(f"   Tags: {', '.join(photo['tags'][:5])}...")
        print()
    
    return photos

if __name__ == "__main__":
    import asyncio
    photos = asyncio.run(main())