from pydantic import BaseModel, Field, EmailStr, validator
from typing import List, Optional
from datetime import datetime
import uuid

# Service Models
class Service(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    image: str
    features: List[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ServiceCreate(BaseModel):
    title: str
    description: str
    image: str
    features: List[str]

# Review Models
class Review(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    rating: int = Field(..., ge=1, le=10)  # Changed to allow ratings up to 10 to match Checkatrade
    date: str
    text: str
    service: str
    postcode: Optional[str] = None  # Added for location identification
    lat: Optional[float] = None  # Added for map coordinates
    lng: Optional[float] = None  # Added for map coordinates
    images: List[str] = []  # Added for work photos
    approved: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ReviewCreate(BaseModel):
    name: str
    rating: int = Field(..., ge=1, le=5)
    text: str
    service: str
    
    @validator('name')
    def validate_name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()

# Quote Request Models
class QuoteRequest(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: EmailStr
    phone: str
    service: str
    message: str
    status: str = "pending"
    created_at: datetime = Field(default_factory=datetime.utcnow)

class QuoteRequestCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    service: str
    message: str

    @validator('name', 'phone')
    def validate_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Field cannot be empty')
        return v.strip()

    @validator('phone')
    def validate_phone(cls, v):
        # Basic UK phone number validation - allow international format
        cleaned = ''.join(filter(str.isdigit, v))
        # Remove country code if present (+44 becomes 44)
        if v.startswith('+44'):
            cleaned = '0' + cleaned[2:]  # Convert +447... to 07...
        elif v.startswith('0044'):
            cleaned = '0' + cleaned[4:]  # Convert 00447... to 07...
        
        if len(cleaned) < 10 or len(cleaned) > 11:
            raise ValueError('Invalid phone number format')
        return v

# Contact Models
class Contact(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: EmailStr
    phone: str
    subject: str
    message: str
    status: str = "new"
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    subject: str
    message: str

    @validator('name', 'subject')
    def validate_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Field cannot be empty')
        return v.strip()

# Gallery Models
class GalleryImage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    src: str
    title: str
    category: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class GalleryImageCreate(BaseModel):
    src: str
    title: str
    category: str

# Response Models
class MessageResponse(BaseModel):
    message: str
    id: Optional[str] = None

class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None