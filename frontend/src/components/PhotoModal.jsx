import React, { useState } from "react";
import { ChevronLeft, ChevronRight, Star, MapPin, Calendar, Image as ImageIcon, X } from "lucide-react";
import { Modal, ModalHeader, ModalContent } from "./ui/modal";
import { Badge } from "./ui/badge";

const PhotoModal = ({ isOpen, onClose, review }) => {
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  
  if (!review) return null;
  
  // Ensure images exist and is an array
  let images = Array.isArray(review.images) ? review.images : [];
  if (images.length === 0) {
    console.log('No images found for review:', review);
    return null;
  }

  // Convert Google Storage URLs to proxy or handle them
  // Note: Google Storage URLs from Checkatrade have authentication tokens that expire
  // For now, we'll attempt to load them and show error message if they fail
  images = images.map(url => {
    if (url.includes('storage.googleapis.com') && url.includes('core-media-service')) {
      // These are Checkatrade's Google Cloud Storage URLs
      // They may have expired authentication tokens
      // Try to load them, but they might fail
      return url;
    }
    
    if (url.includes('drive.google.com')) {
      // Extract file ID from various Google Drive URL formats
      let fileId = null;
      
      // Format: https://drive.google.com/file/d/FILE_ID/view
      const fileMatch = url.match(/\/file\/d\/([a-zA-Z0-9_-]+)/);
      if (fileMatch) {
        fileId = fileMatch[1];
      }
      
      // Format: https://drive.google.com/uc?export=view&id=FILE_ID
      const idMatch = url.match(/[?&]id=([a-zA-Z0-9_-]+)/);
      if (idMatch) {
        fileId = idMatch[1];
      }
      
      // If we found a file ID, create a direct thumbnail URL
      if (fileId) {
        return `https://drive.google.com/thumbnail?id=${fileId}&sz=w1600`;
      }
    }
    
    // Return original URL
    return url;
  });

  const nextImage = () => {
    setCurrentImageIndex((prev) => (prev + 1) % images.length);
  };

  const prevImage = () => {
    setCurrentImageIndex((prev) => (prev - 1 + images.length) % images.length);
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} className="max-w-6xl">
      <ModalHeader>
        <div className="flex items-center justify-between pr-8">
          <div>
            <h3 className="text-2xl font-bold text-gray-900">{review.service}</h3>
            <div className="flex items-center space-x-2 mt-2">
              <Badge variant="outline" className="text-green-700 border-green-200">
                {review.postcode}
              </Badge>
              <div className="flex text-yellow-400">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className={`w-4 h-4 ${i < Math.floor(review.rating / 2) ? 'fill-current' : ''}`} />
                ))}
              </div>
              <span className="font-semibold">{(review.rating / 2).toFixed(1)}/5</span>
            </div>
          </div>
        </div>
      </ModalHeader>
      
      <ModalContent className="space-y-6">
        {/* Image Gallery */}
        <div className="relative">
          <div className="aspect-video bg-gray-100 rounded-lg overflow-hidden">
            <img
              src={images[currentImageIndex]}
              alt={`Professional work by ${review.name} - Image ${currentImageIndex + 1}`}
              className="w-full h-full object-cover"
              onError={(e) => {
                console.error('❌ Image failed to load:', images[currentImageIndex]);
                
                // Hide the image and show error message
                e.target.style.display = 'none';
                
                // Add error message if not already present
                if (!e.target.parentNode.querySelector('.error-message')) {
                  const errorDiv = document.createElement('div');
                  errorDiv.className = 'error-message';
                  errorDiv.innerHTML = `<div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background: rgba(239, 68, 68, 0.95); color: white; padding: 24px; border-radius: 12px; text-align: center; max-width: 80%;">
                    <div style="font-size: 48px; margin-bottom: 12px;">📷</div>
                    <div style="font-size: 18px; font-weight: 600; margin-bottom: 8px;">Image Unavailable</div>
                    <div style="font-size: 14px; opacity: 0.95;">This image could not be loaded</div>
                  </div>`;
                  e.target.parentNode.style.position = 'relative';
                  e.target.parentNode.appendChild(errorDiv);
                }
              }}
              onLoad={() => {
                console.log('✅ Modal image loaded successfully:', images[currentImageIndex]);
              }}
            />
          </div>
          
          {/* Navigation Arrows */}
          {images.length > 1 && (
            <>
              <button
                onClick={prevImage}
                className="absolute left-2 top-1/2 -translate-y-1/2 bg-white bg-opacity-80 hover:bg-opacity-100 rounded-full p-2 shadow-lg transition-all"
              >
                <ChevronLeft className="w-5 h-5" />
              </button>
              <button
                onClick={nextImage}
                className="absolute right-2 top-1/2 -translate-y-1/2 bg-white bg-opacity-80 hover:bg-opacity-100 rounded-full p-2 shadow-lg transition-all"
              >
                <ChevronRight className="w-5 h-5" />
              </button>
            </>
          )}
          
          {/* Image Counter */}
          {images.length > 1 && (
            <div className="absolute bottom-4 left-1/2 -translate-x-1/2 bg-black bg-opacity-50 text-white px-3 py-1 rounded-full text-sm">
              {currentImageIndex + 1} / {images.length}
            </div>
          )}
        </div>
        
        {/* Thumbnail Navigation */}
        {images.length > 1 && (
          <div className="flex space-x-2 overflow-x-auto pb-2">
            {images.map((image, index) => (
              <button
                key={index}
                onClick={() => setCurrentImageIndex(index)}
                className={`flex-shrink-0 w-20 h-20 rounded-lg overflow-hidden border-2 transition-all ${
                  index === currentImageIndex ? 'border-green-500' : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <img
                  src={image}
                  alt={`Thumbnail ${index + 1}`}
                  className="w-full h-full object-cover"
                  onError={(e) => {
                    e.target.style.display = 'none';
                  }}
                />
              </button>
            ))}
          </div>
        )}
        
        {/* Review Details */}
        <div className="space-y-4">
          <div>
            <h4 className="text-lg font-semibold text-gray-900 mb-2">Customer Review</h4>
            <p className="text-gray-600 leading-relaxed text-lg">
              "{review.text}"
            </p>
          </div>
          
          <div className="flex items-center space-x-4 text-sm text-gray-500 pt-4 border-t border-gray-200">
            <div className="flex items-center space-x-1">
              <Calendar className="w-4 h-4" />
              <span>{review.date}</span>
            </div>
            <div className="flex items-center space-x-1">
              <MapPin className="w-4 h-4" />
              <span>{review.postcode}</span>
            </div>
            <div className="flex items-center space-x-1">
              <ImageIcon className="w-4 h-4" />
              <span>{images.length} photo{images.length !== 1 ? 's' : ''}</span>
            </div>
            <span>•</span>
            <span>{review.name}</span>
          </div>
        </div>
      </ModalContent>
    </Modal>
  );
};

export default PhotoModal;