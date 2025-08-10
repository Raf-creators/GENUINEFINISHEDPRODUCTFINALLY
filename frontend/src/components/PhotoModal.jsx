import React, { useState } from "react";
import { ChevronLeft, ChevronRight, Star, MapPin, Calendar, Image as ImageIcon, X } from "lucide-react";
import { Modal, ModalHeader, ModalContent } from "./ui/modal";
import { Badge } from "./ui/badge";

const PhotoModal = ({ isOpen, onClose, review }) => {
  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  
  if (!review) return null;
  
  // Ensure images exist and is an array
  const images = Array.isArray(review.images) ? review.images : [];
  if (images.length === 0) {
    console.log('No images found for review:', review);
    return null;
  }

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
                {[...Array(Math.floor(review.rating))].map((_, i) => (
                  <Star key={i} className="w-4 h-4 fill-current" />
                ))}
              </div>
              <span className="font-semibold">{review.rating}/10</span>
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
              alt={`Work completed in ${review.postcode} - Image ${currentImageIndex + 1}`}
              className="w-full h-full object-cover"
              onError={(e) => {
                console.error('Failed to load image:', images[currentImageIndex]);
                e.target.src = "https://images.unsplash.com/photo-1621460248083-6271cc4437a8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzd8MHwxfHNlYXJjaHwxfHxnYXJkZW5pbmd8ZW58MHx8fHwxNzU0ODM3OTM2fDA&ixlib=rb-4.1.0&q=85";
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