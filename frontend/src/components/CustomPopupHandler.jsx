import React, { useEffect } from 'react';
import { useMap } from 'react-leaflet';
import L from 'leaflet';

const CustomPopupHandler = ({ reviews, openPhotoModal }) => {
  const map = useMap();

  useEffect(() => {
    // Clear existing markers
    map.eachLayer((layer) => {
      if (layer instanceof L.Marker) {
        map.removeLayer(layer);
      }
    });

    // Add custom markers with proper event handling
    reviews.forEach((review) => {
      if (review.lat && review.lng) {
        const marker = L.marker([review.lat, review.lng]).addTo(map);
        
        // Create popup content as HTML string
        const popupContent = `
          <div class="max-w-sm">
            <div class="flex items-center space-x-2 mb-3">
              <div class="flex text-yellow-400">
                ${'★'.repeat(Math.floor(review.rating))}
              </div>
              <span class="font-semibold text-lg">${review.rating}/10</span>
              <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-50 text-green-700 border border-green-200">
                ${review.postcode}
              </span>
            </div>
            
            <h4 class="font-semibold text-gray-900 mb-2 text-lg">
              ${review.service}
            </h4>
            
            <p class="text-sm text-gray-600 mb-3 leading-relaxed">
              ${review.text.length > 100 ? review.text.substring(0, 100) + '...' : review.text}
            </p>

            ${review.images && review.images.length > 0 ? `
              <button 
                id="view-photos-${review.id}" 
                class="w-full bg-green-700 text-white px-3 py-2 rounded-md text-sm font-medium hover:bg-green-800 transition-colors flex items-center justify-center space-x-2 mb-3"
                style="cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px;"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/>
                  <circle cx="12" cy="12" r="3"/>
                </svg>
                <span>View ${review.images.length} Photo${review.images.length !== 1 ? 's' : ''}</span>
              </button>
            ` : ''}
            
            <div class="text-xs text-gray-500 border-t pt-2">
              <div class="flex items-center space-x-2">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                  <line x1="16" y1="2" x2="16" y2="6"/>
                  <line x1="8" y1="2" x2="8" y2="6"/>
                  <line x1="3" y1="10" x2="21" y2="10"/>
                </svg>
                <span>${review.date}</span>
                <span>•</span>
                <span>${review.name}</span>
              </div>
            </div>
          </div>
        `;

        const popup = L.popup().setContent(popupContent);
        marker.bindPopup(popup);

        // Add click handler for the photo button after popup opens
        marker.on('popupopen', () => {
          const button = document.getElementById(`view-photos-${review.id}`);
          if (button) {
            button.addEventListener('click', (e) => {
              e.preventDefault();
              e.stopPropagation();
              console.log('Photo button clicked for review:', review.id);
              openPhotoModal(review);
            });
          }
        });

        // Set selected review when marker is clicked
        marker.on('click', () => {
          // We need to access setSelectedReview from the parent component
          // For now, let's trigger a custom event
          window.dispatchEvent(new CustomEvent('markerClicked', { detail: review }));
        });
      }
    });

    return () => {
      // Cleanup markers when component unmounts
      map.eachLayer((layer) => {
        if (layer instanceof L.Marker) {
          map.removeLayer(layer);
        }
      });
    };
  }, [map, reviews, openPhotoModal]);

  return null;
};

export default CustomPopupHandler;