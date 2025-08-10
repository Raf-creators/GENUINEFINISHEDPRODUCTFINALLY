# Photo Management Infrastructure for PNM Gardeners
# This file contains the structure and utilities for managing 500+ job photos

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

# Enhanced models for photo management
class JobPhoto(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    filename: str
    original_url: str
    thumbnail_url: Optional[str] = None
    compressed_url: Optional[str] = None  # For web optimization
    alt_text: str
    caption: Optional[str] = None
    
    # Photo metadata
    upload_date: datetime = Field(default_factory=datetime.utcnow)
    file_size: Optional[int] = None  # in bytes
    dimensions: Optional[Dict[str, int]] = None  # {"width": 1920, "height": 1080}
    
    # Job/project association
    job_id: Optional[str] = None
    review_id: Optional[str] = None
    service_type: Optional[str] = None
    
    # Location and categorization
    postcode: Optional[str] = None
    location_area: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    
    # Photo type and categorization
    photo_type: str = "work_completed"  # work_completed, before_after, progress, equipment
    category: str = "general"  # general, garden_clearance, hedge_trimming, lawn_care, etc.
    is_before_photo: bool = False
    is_after_photo: bool = False
    is_featured: bool = False  # For highlighting best photos
    
    # SEO and search
    tags: List[str] = []  # ["garden", "clearance", "transformation", "london"]
    is_searchable: bool = True
    is_public: bool = True
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class JobProject(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    service_type: str
    
    # Location details
    postcode: str
    area: str
    lat: Optional[float] = None
    lng: Optional[float] = None
    
    # Project details
    completion_date: datetime
    duration_days: Optional[int] = None
    project_cost: Optional[float] = None  # For showcasing project scale
    
    # Associated content
    review_id: Optional[str] = None  # Link to customer review
    photos: List[str] = []  # List of photo IDs
    before_photos: List[str] = []
    after_photos: List[str] = []
    
    # Project status and visibility
    is_featured: bool = False
    is_case_study: bool = False  # For detailed project showcases
    is_public: bool = True
    
    # SEO
    slug: Optional[str] = None  # URL-friendly project identifier
    meta_description: Optional[str] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Photo upload and processing utilities
class PhotoManager:
    """Utility class for managing photo uploads and processing"""
    
    @staticmethod
    def generate_photo_variants(original_url: str) -> Dict[str, str]:
        """Generate different sized versions of uploaded photos"""
        # This would integrate with image processing service
        base_url = original_url.rsplit('.', 1)[0]
        extension = original_url.rsplit('.', 1)[1]
        
        return {
            'thumbnail': f"{base_url}_thumb.{extension}",
            'medium': f"{base_url}_medium.{extension}", 
            'large': f"{base_url}_large.{extension}",
            'compressed': f"{base_url}_compressed.{extension}"
        }
    
    @staticmethod
    def extract_metadata_from_filename(filename: str) -> Dict[str, Any]:
        """Extract metadata from structured filename"""
        # Example filename: "SW12_garden_clearance_before_20250810_001.jpg"
        parts = filename.lower().replace('.jpg', '').replace('.jpeg', '').replace('.png', '').split('_')
        
        metadata = {
            'postcode': None,
            'service_type': None,
            'photo_type': 'general',
            'date': None,
            'sequence': None
        }
        
        # Postcode detection (SW12, SE22, etc.)
        postcode_patterns = ['sw', 'se', 'nw', 'ne', 'w', 'e', 'n', 's', 'cr', 'kt', 'sm', 'tw']
        for part in parts:
            if len(part) >= 2 and part[:2] in postcode_patterns:
                metadata['postcode'] = part.upper()
                break
        
        # Service type detection
        service_keywords = {
            'clearance': 'Garden Clearance',
            'hedge': 'Hedge Trimming',
            'lawn': 'Lawn Care',
            'patio': 'Patio Services',
            'maintenance': 'Garden Maintenance',
            'planting': 'Planting',
            'tree': 'Tree Services'
        }
        
        for part in parts:
            for keyword, service in service_keywords.items():
                if keyword in part:
                    metadata['service_type'] = service
                    break
        
        # Photo type detection
        if 'before' in parts:
            metadata['photo_type'] = 'before'
            metadata['is_before_photo'] = True
        elif 'after' in parts:
            metadata['photo_type'] = 'after'
            metadata['is_after_photo'] = True
        elif 'progress' in parts:
            metadata['photo_type'] = 'progress'
            
        return metadata

# Photo Upload Instructions for User
PHOTO_UPLOAD_INSTRUCTIONS = """
🎯 PHOTO UPLOAD GUIDE FOR 500+ PHOTOS

For best organization and automatic categorization, name your photos using this format:
[POSTCODE]_[SERVICE]_[TYPE]_[DATE]_[NUMBER].jpg

Examples:
- SW12_garden_clearance_before_20250810_001.jpg
- SW12_garden_clearance_after_20250810_002.jpg
- SW19_hedge_trimming_completed_20250809_001.jpg
- SE22_patio_cleaning_before_20250808_001.jpg

📁 RECOMMENDED FOLDER STRUCTURE:
├── Garden_Clearance/
│   ├── SW12_Before_After/
│   ├── SW16_Before_After/
│   └── SW19_Before_After/
├── Hedge_Trimming/
├── Lawn_Care/
├── Patio_Services/
├── Tree_Services/
└── Maintenance_General/

🏷️ AUTOMATIC FEATURES:
✅ Auto-categorization by service type
✅ Location mapping to London postcodes  
✅ Before/after photo pairing
✅ SEO-optimized alt text generation
✅ Searchable tags and keywords
✅ Integration with customer reviews

📸 PHOTO TYPES SUPPORTED:
• Before/After transformations
• Work in progress shots
• Equipment and team photos
• Detail shots of completed work
• Seasonal maintenance photos

When you upload, the system will:
1. Extract location and service info from filename
2. Generate thumbnails and compressed versions
3. Create searchable tags automatically
4. Link to existing customer reviews when possible
5. Make photos available in gallery and map
"""

if __name__ == "__main__":
    # Example usage
    sample_filenames = [
        "SW12_garden_clearance_before_20250810_001.jpg",
        "SW12_garden_clearance_after_20250810_002.jpg", 
        "SW19_hedge_trimming_completed_20250809_001.jpg",
        "SE22_patio_cleaning_before_20250808_001.jpg",
        "SE22_patio_cleaning_after_20250808_002.jpg"
    ]
    
    print("Photo Management System - Example Processing:")
    print("=" * 50)
    
    for filename in sample_filenames:
        manager = PhotoManager()
        metadata = manager.extract_metadata_from_filename(filename)
        
        print(f"\nFilename: {filename}")
        print(f"Postcode: {metadata.get('postcode', 'Not detected')}")
        print(f"Service: {metadata.get('service_type', 'Not detected')}")
        print(f"Photo Type: {metadata.get('photo_type', 'general')}")
    
    print("\n" + "=" * 50)
    print("Ready for 500+ photo upload! 📸")