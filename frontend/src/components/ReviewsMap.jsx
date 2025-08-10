import React, { useState, useEffect } from "react";
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import { apiService, handleApiError } from "../services/api";
import { reviews as fallbackReviews } from "../mock/data";
import { Star, MapPin, Calendar, Image } from "lucide-react";
import { Badge } from "./ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import 'leaflet/dist/leaflet.css';

// Fix for default markers in React Leaflet
import L from 'leaflet';
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Create custom icon for our markers
const createCustomIcon = (rating) => {
  const color = rating >= 9.5 ? '#16a34a' : rating >= 8 ? '#ca8a04' : '#dc2626';
  return L.divIcon({
    html: `
      <div style="
        background-color: ${color};
        color: white;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 12px;
        border: 2px solid white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
      ">${rating}</div>
    `,
    className: 'custom-marker',
    iconSize: [30, 30],
    iconAnchor: [15, 15]
  });
};

const ReviewsMap = () => {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedReview, setSelectedReview] = useState(null);

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
                  <MapContainer
                    center={londonCenter}
                    zoom={11}
                    style={{ height: '100%', width: '100%' }}
                  >
                    <TileLayer
                      attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                      url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    />
                    {reviewsWithCoords.map((review) => (
                      <Marker
                        key={review.id}
                        position={[review.lat, review.lng]}
                        icon={createCustomIcon(review.rating)}
                        eventHandlers={{
                          click: () => setSelectedReview(review)
                        }}
                      >
                        <Popup>
                          <div className="max-w-sm">
                            <div className="flex items-center space-x-2 mb-2">
                              <div className="flex text-yellow-400">
                                {[...Array(Math.floor(review.rating))].map((_, i) => (
                                  <Star key={i} className="w-4 h-4 fill-current" />
                                ))}
                              </div>
                              <span className="font-semibold">{review.rating}/10</span>
                              <Badge variant="outline" className="text-xs">
                                {review.postcode}
                              </Badge>
                            </div>
                            <h4 className="font-semibold text-gray-900 mb-2">
                              {review.service}
                            </h4>
                            <p className="text-sm text-gray-600 mb-2">
                              {review.text.length > 100 ? 
                                `${review.text.substring(0, 100)}...` : 
                                review.text
                              }
                            </p>
                            <div className="text-xs text-gray-500">
                              {review.date} • {review.name}
                            </div>
                          </div>
                        </Popup>
                      </Marker>
                    ))}
                  </MapContainer>
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
                    <CardTitle className="text-lg">Customer Review</CardTitle>
                    <Badge variant="outline" className="text-green-700 border-green-200">
                      {selectedReview.postcode}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center space-x-2">
                    <div className="flex text-yellow-400">
                      {[...Array(Math.floor(selectedReview.rating))].map((_, i) => (
                        <Star key={i} className="w-4 h-4 fill-current" />
                      ))}
                    </div>
                    <span className="font-semibold text-lg">{selectedReview.rating}/10</span>
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
                      <div className="flex items-center space-x-2 mb-3">
                        <Image className="w-4 h-4 text-gray-500" />
                        <span className="text-sm font-medium text-gray-700">Work Photos</span>
                      </div>
                      <div className="grid grid-cols-2 gap-2">
                        {selectedReview.images.map((image, index) => (
                          <img
                            key={index}
                            src={image}
                            alt={`Work photo ${index + 1}`}
                            className="w-full h-20 object-cover rounded-lg border"
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
                    Click on any marker on the map to see detailed customer reviews and photos of our work.
                  </p>
                </CardContent>
              </Card>
            )}

            {/* Map Legend */}
            <Card className="border-0 shadow-xl mt-6">
              <CardHeader>
                <CardTitle className="text-lg">Map Legend</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-center space-x-3">
                  <div className="w-6 h-6 bg-green-600 rounded-full flex items-center justify-center text-white text-xs font-bold">
                    10
                  </div>
                  <span className="text-sm">Excellent (9.5-10)</span>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="w-6 h-6 bg-yellow-600 rounded-full flex items-center justify-center text-white text-xs font-bold">
                    9
                  </div>
                  <span className="text-sm">Very Good (8-9.4)</span>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="w-6 h-6 bg-red-600 rounded-full flex items-center justify-center text-white text-xs font-bold">
                    7
                  </div>
                  <span className="text-sm">Good (Below 8)</span>
                </div>
              </CardContent>
            </Card>
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
                9.76
              </div>
              <div className="text-sm text-gray-600">Average Rating</div>
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
      </div>
    </section>
  );
};

export default ReviewsMap;