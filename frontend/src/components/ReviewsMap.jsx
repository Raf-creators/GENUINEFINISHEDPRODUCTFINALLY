import React, { useState, useEffect } from "react";
import { MapContainer, TileLayer } from 'react-leaflet';
import { apiService, handleApiError } from "../services/api";
import { reviews as fallbackReviews } from "../mock/data";
import { Star, MapPin, Calendar, Image, Eye } from "lucide-react";
import { Badge } from "./ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import PhotoModal from "./PhotoModal";
import CustomPopupHandler from "./CustomPopupHandler";
import 'leaflet/dist/leaflet.css';

// Import and set up Leaflet properly
import L from 'leaflet';

// Fix default icon paths
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const ReviewsMap = () => {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedReview, setSelectedReview] = useState(null);
  const [photoModalOpen, setPhotoModalOpen] = useState(false);
  const [modalReview, setModalReview] = useState(null);

  useEffect(() => {
    const fetchReviews = async () => {
      try {
        setLoading(true);
        const data = await apiService.getReviews();
        setReviews(data);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch reviews for map, using fallback data:', err);
        const errorInfo = handleApiError(err);
        setError(errorInfo.message);
        setReviews(fallbackReviews);
      } finally {
        setLoading(false);
      }
    };

    fetchReviews();
  }, []);

  // Listen for custom marker click events
  useEffect(() => {
    const handleMarkerClick = (event) => {
      setSelectedReview(event.detail);
    };

    window.addEventListener('markerClicked', handleMarkerClick);
    return () => {
      window.removeEventListener('markerClicked', handleMarkerClick);
    };
  }, []);

  const openPhotoModal = (review) => {
    console.log('Opening photo modal for review:', review);
    console.log('Review images:', review.images);
    setModalReview(review);
    setPhotoModalOpen(true);
  };

  const closePhotoModal = () => {
    setPhotoModalOpen(false);
    setModalReview(null);
  };

  // London center coordinates
  const londonCenter = [51.5074, -0.1278];

  if (loading) {
    return (
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="text-center">
            <div className="text-xl text-gray-600">Loading reviews map...</div>
          </div>
        </div>
      </section>
    );
  }

  const reviewsWithCoords = reviews.filter(review => review.lat && review.lng);

  // Debug logging
  console.log('ReviewsMap Debug:', {
    totalReviews: reviews.length,
    reviewsWithCoords: reviewsWithCoords.length,
    reviewsData: reviewsWithCoords.map(r => ({
      id: r.id,
      postcode: r.postcode,
      lat: r.lat,
      lng: r.lng
    }))
  });

  return (
    <section className="py-20 bg-gray-50">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl lg:text-5xl font-bold text-gray-900 mb-6">
            Our Work Across London
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            See where we've completed gardening projects and read reviews from customers across London. 
            Click on the markers to see customer testimonials and photos of our work.
          </p>
          {error && (
            <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg text-sm text-yellow-800 max-w-md mx-auto">
              ⚠️ Using cached data: {error}
            </div>
          )}
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Map */}
          <div className="lg:col-span-2">
            <Card className="border-0 shadow-xl overflow-hidden">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center space-x-2">
                  <MapPin className="w-5 h-5 text-green-700" />
                  <span>Customer Reviews Map</span>
                </CardTitle>
                <p className="text-sm text-gray-600">
                  Click on any marker to see customer reviews and work photos
                </p>
              </CardHeader>
              <CardContent className="p-0">
                <div style={{ height: '500px', width: '100%' }}>
                  {reviewsWithCoords.length > 0 ? (
                    <MapContainer
                      center={londonCenter}
                      zoom={11}
                      style={{ height: '100%', width: '100%' }}
                    >
                      <TileLayer
                        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                      />
                      <CustomPopupHandler reviews={reviewsWithCoords} openPhotoModal={openPhotoModal} />
                    </MapContainer>
                  ) : (
                    <div className="h-full flex items-center justify-center bg-gray-100">
                      <div className="text-center">
                        <MapPin className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                        <p className="text-gray-600">Loading map markers...</p>
                      </div>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Selected Review Details */}
          <div>
            {selectedReview ? (
              <Card className="border-0 shadow-xl">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-lg">Work Completed</CardTitle>
                    <Badge variant="outline" className="text-green-700 border-green-200">
                      {selectedReview.postcode}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center space-x-2">
                    <div className="flex text-yellow-400">
                      {[...Array(5)].map((_, i) => (
                        <Star key={i} className={`w-4 h-4 ${i < Math.floor(selectedReview.rating / 2) ? 'fill-current' : ''}`} />
                      ))}
                    </div>
                    <span className="font-semibold text-lg">{(selectedReview.rating / 2).toFixed(1)}/5</span>
                  </div>

                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2">
                      {selectedReview.service}
                    </h4>
                    <p className="text-gray-600 leading-relaxed">
                      {selectedReview.text}
                    </p>
                  </div>

                  {selectedReview.images && selectedReview.images.length > 0 && (
                    <div>
                      <button
                        onClick={() => openPhotoModal(selectedReview)}
                        className="w-full bg-green-700 text-white px-4 py-3 rounded-lg font-medium hover:bg-green-800 transition-colors flex items-center justify-center space-x-2 mb-3"
                      >
                        <Eye className="w-5 h-5" />
                        <span>View {selectedReview.images.length} Work Photo{selectedReview.images.length !== 1 ? 's' : ''}</span>
                      </button>
                      
                      <div className="grid grid-cols-2 gap-2">
                        {selectedReview.images.slice(0, 4).map((image, index) => (
                          <img
                            key={index}
                            src={image}
                            alt={`Work completed ${index + 1}`}
                            className="w-full h-20 object-cover rounded-lg border cursor-pointer hover:opacity-80 transition-opacity"
                            onClick={() => openPhotoModal(selectedReview)}
                            onError={(e) => {
                              e.target.style.display = 'none';
                            }}
                          />
                        ))}
                      </div>
                    </div>
                  )}

                  <div className="pt-4 border-t border-gray-200">
                    <div className="flex items-center space-x-2 text-sm text-gray-500">
                      <Calendar className="w-4 h-4" />
                      <span>{selectedReview.date}</span>
                      <span>•</span>
                      <span>{selectedReview.name}</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ) : (
              <Card className="border-0 shadow-xl">
                <CardContent className="p-8 text-center">
                  <MapPin className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    Click a Marker
                  </h3>
                  <p className="text-gray-600">
                    Click on any marker on the map to see detailed customer reviews and photos of our completed work.
                  </p>
                </CardContent>
              </Card>
            )}
          </div>
        </div>

        {/* Stats */}
        <div className="mt-16 grid md:grid-cols-4 gap-6">
          <Card className="border-0 shadow-lg">
            <CardContent className="p-6 text-center">
              <div className="text-3xl font-bold text-green-700 mb-2">
                {reviews.length}
              </div>
              <div className="text-sm text-gray-600">Total Reviews</div>
            </CardContent>
          </Card>
          
          <Card className="border-0 shadow-lg">
            <CardContent className="p-6 text-center">
              <div className="text-3xl font-bold text-green-700 mb-2">
                4.9
              </div>
              <div className="text-sm text-gray-600">Average Rating (out of 5)</div>
            </CardContent>
          </Card>
          
          <Card className="border-0 shadow-lg">
            <CardContent className="p-6 text-center">
              <div className="text-3xl font-bold text-green-700 mb-2">
                {reviewsWithCoords.length}
              </div>
              <div className="text-sm text-gray-600">Areas Served</div>
            </CardContent>
          </Card>
          
          <Card className="border-0 shadow-lg">
            <CardContent className="p-6 text-center">
              <div className="text-3xl font-bold text-green-700 mb-2">
                100%
              </div>
              <div className="text-sm text-gray-600">Satisfaction Rate</div>
            </CardContent>
          </Card>
        </div>
        
        {/* Photo Modal */}
        <PhotoModal 
          isOpen={photoModalOpen}
          onClose={closePhotoModal}
          review={modalReview}
        />
      </div>
    </section>
  );
};

export default ReviewsMap;