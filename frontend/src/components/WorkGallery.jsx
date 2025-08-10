import React, { useState, useEffect } from "react";
import { Search, Filter, MapPin, Calendar, Star, Eye, Grid, List } from "lucide-react";
import { apiService, handleApiError } from "../services/api";
import { reviews as fallbackReviews } from "../mock/data";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import PhotoModal from "./PhotoModal";

const WorkGallery = () => {
  const [reviews, setReviews] = useState([]);
  const [filteredReviews, setFilteredReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedService, setSelectedService] = useState("all");
  const [selectedLocation, setSelectedLocation] = useState("all");
  const [viewMode, setViewMode] = useState("grid"); // grid or list
  const [photoModalOpen, setPhotoModalOpen] = useState(false);
  const [modalReview, setModalReview] = useState(null);

  // Fetch reviews on component mount
  useEffect(() => {
    const fetchReviews = async () => {
      try {
        setLoading(true);
        const data = await apiService.getReviews();
        const reviewsWithPhotos = data.filter(review => review.images && review.images.length > 0);
        setReviews(reviewsWithPhotos);
        setFilteredReviews(reviewsWithPhotos);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch reviews:', err);
        const errorInfo = handleApiError(err);
        setError(errorInfo.message);
        const fallbackWithPhotos = fallbackReviews.filter(review => review.images && review.images.length > 0);
        setReviews(fallbackWithPhotos);
        setFilteredReviews(fallbackWithPhotos);
      } finally {
        setLoading(false);
      }
    };

    fetchReviews();
  }, []);

  // Filter reviews based on search and filters
  useEffect(() => {
    let filtered = reviews;

    // Search filter
    if (searchTerm) {
      filtered = filtered.filter(review => 
        review.service.toLowerCase().includes(searchTerm.toLowerCase()) ||
        review.text.toLowerCase().includes(searchTerm.toLowerCase()) ||
        review.postcode.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Service filter
    if (selectedService !== "all") {
      filtered = filtered.filter(review => 
        review.service.toLowerCase().includes(selectedService.toLowerCase())
      );
    }

    // Location filter
    if (selectedLocation !== "all") {
      filtered = filtered.filter(review => review.postcode === selectedLocation);
    }

    setFilteredReviews(filtered);
  }, [reviews, searchTerm, selectedService, selectedLocation]);

  const openPhotoModal = (review) => {
    setModalReview(review);
    setPhotoModalOpen(true);
  };

  const closePhotoModal = () => {
    setPhotoModalOpen(false);
    setModalReview(null);
  };

  // Get unique services and locations for filters
  const uniqueServices = [...new Set(reviews.map(review => {
    const service = review.service.toLowerCase();
    if (service.includes('garden') && service.includes('clearance')) return 'Garden Clearance';
    if (service.includes('hedge')) return 'Hedge Trimming';
    if (service.includes('lawn')) return 'Lawn Care';
    if (service.includes('maintenance')) return 'Garden Maintenance';
    if (service.includes('planting')) return 'Planting';
    if (service.includes('patio')) return 'Patio Services';
    if (service.includes('tree') || service.includes('pruning')) return 'Tree Services';
    return 'Other Services';
  }))];

  const uniqueLocations = [...new Set(reviews.map(review => review.postcode))].sort();

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-20">
        <div className="container mx-auto px-4">
          <div className="text-center">
            <div className="text-xl text-gray-600">Loading work gallery...</div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-20">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl lg:text-5xl font-bold text-gray-900 mb-6">
            Work Gallery
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Browse our completed projects across London. See before and after photos, 
            read customer testimonials, and discover the quality of our gardening services.
          </p>
          {error && (
            <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg text-sm text-yellow-800 max-w-md mx-auto">
              ⚠️ Using cached data: {error}
            </div>
          )}
        </div>

        {/* Filters and Search */}
        <Card className="mb-8 border-0 shadow-lg">
          <CardContent className="p-6">
            <div className="grid md:grid-cols-4 gap-4 items-end">
              {/* Search */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Search Projects
                </label>
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                  <input
                    type="text"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    placeholder="Search services, locations..."
                    className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-green-500 focus:border-green-500"
                  />
                </div>
              </div>

              {/* Service Filter */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Service Type
                </label>
                <select
                  value={selectedService}
                  onChange={(e) => setSelectedService(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-green-500 focus:border-green-500"
                >
                  <option value="all">All Services</option>
                  {uniqueServices.map(service => (
                    <option key={service} value={service}>{service}</option>
                  ))}
                </select>
              </div>

              {/* Location Filter */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Location
                </label>
                <select
                  value={selectedLocation}
                  onChange={(e) => setSelectedLocation(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-green-500 focus:border-green-500"
                >
                  <option value="all">All Locations</option>
                  {uniqueLocations.map(location => (
                    <option key={location} value={location}>{location}</option>
                  ))}
                </select>
              </div>

              {/* View Mode Toggle */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  View Mode
                </label>
                <div className="flex border border-gray-300 rounded-md overflow-hidden">
                  <button
                    onClick={() => setViewMode('grid')}
                    className={`px-3 py-2 flex items-center space-x-1 ${
                      viewMode === 'grid' 
                        ? 'bg-green-700 text-white' 
                        : 'bg-white text-gray-700 hover:bg-gray-50'
                    }`}
                  >
                    <Grid className="w-4 h-4" />
                    <span>Grid</span>
                  </button>
                  <button
                    onClick={() => setViewMode('list')}
                    className={`px-3 py-2 flex items-center space-x-1 border-l border-gray-300 ${
                      viewMode === 'list' 
                        ? 'bg-green-700 text-white' 
                        : 'bg-white text-gray-700 hover:bg-gray-50'
                    }`}
                  >
                    <List className="w-4 h-4" />
                    <span>List</span>
                  </button>
                </div>
              </div>
            </div>

            {/* Results Count */}
            <div className="mt-4 text-sm text-gray-600">
              Showing {filteredReviews.length} project{filteredReviews.length !== 1 ? 's' : ''} with photos
              {reviews.length > filteredReviews.length && (
                <span className="ml-2 text-green-700">
                  (filtered from {reviews.length} total)
                </span>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Gallery Content */}
        {filteredReviews.length > 0 ? (
          <div className={`grid gap-6 ${
            viewMode === 'grid' 
              ? 'md:grid-cols-2 lg:grid-cols-3' 
              : 'grid-cols-1 max-w-4xl mx-auto'
          }`}>
            {filteredReviews.map((review) => (
              <Card key={review.id} className="border-0 shadow-lg hover:shadow-xl transition-shadow">
                <CardContent className="p-0">
                  {viewMode === 'grid' ? (
                    // Grid View
                    <>
                      <div className="aspect-video bg-gray-100 rounded-t-lg overflow-hidden relative group">
                        <img
                          src={review.images[0]}
                          alt={`Work completed: ${review.service}`}
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                          onError={(e) => {
                            e.target.src = "https://images.unsplash.com/photo-1621460248083-6271cc4437a8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzd8MHwxfHNlYXJjaHwxfHxnYXJkZW5pbmd8ZW58MHx8fHwxNzU0ODM3OTM2fDA&ixlib=rb-4.1.0&q=85";
                          }}
                        />
                        
                        {/* Overlay */}
                        <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-all duration-300 flex items-center justify-center">
                          <button
                            onClick={() => openPhotoModal(review)}
                            className="opacity-0 group-hover:opacity-100 transition-opacity bg-white rounded-full p-3 shadow-lg"
                          >
                            <Eye className="w-5 h-5 text-gray-800" />
                          </button>
                        </div>
                        
                        {/* Photo Count Badge */}
                        {review.images.length > 1 && (
                          <div className="absolute top-3 right-3 bg-black bg-opacity-50 text-white px-2 py-1 rounded text-sm">
                            +{review.images.length - 1}
                          </div>
                        )}
                      </div>
                      
                      <div className="p-4">
                        <div className="flex items-center justify-between mb-2">
                          <Badge variant="outline" className="text-green-700 border-green-200">
                            {review.postcode}
                          </Badge>
                          <div className="flex items-center space-x-1">
                            <Star className="w-4 h-4 text-yellow-400 fill-current" />
                            <span className="text-sm font-medium">{review.rating}/10</span>
                          </div>
                        </div>
                        
                        <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2">
                          {review.service}
                        </h3>
                        
                        <p className="text-sm text-gray-600 mb-3 line-clamp-3">
                          "{review.text}"
                        </p>
                        
                        <div className="flex items-center justify-between text-xs text-gray-500">
                          <div className="flex items-center space-x-1">
                            <Calendar className="w-3 h-3" />
                            <span>{review.date}</span>
                          </div>
                          <button
                            onClick={() => openPhotoModal(review)}
                            className="text-green-700 hover:text-green-800 font-medium"
                          >
                            View Photos
                          </button>
                        </div>
                      </div>
                    </>
                  ) : (
                    // List View
                    <div className="flex space-x-4 p-6">
                      <div className="flex-shrink-0 w-48 h-32 bg-gray-100 rounded-lg overflow-hidden">
                        <img
                          src={review.images[0]}
                          alt={`Work completed: ${review.service}`}
                          className="w-full h-full object-cover"
                          onError={(e) => {
                            e.target.src = "https://images.unsplash.com/photo-1621460248083-6271cc4437a8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzd8MHwxfHNlYXJjaHwxfHxnYXJkZW5pbmd8ZW58MHx8fHwxNzU0ODM3OTM2fDA&ixlib=rb-4.1.0&q=85";
                          }}
                        />
                      </div>
                      
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-2">
                          <Badge variant="outline" className="text-green-700 border-green-200">
                            {review.postcode}
                          </Badge>
                          <div className="flex items-center space-x-1">
                            <Star className="w-4 h-4 text-yellow-400 fill-current" />
                            <span className="text-sm font-medium">{review.rating}/10</span>
                          </div>
                          <span className="text-xs text-gray-500">•</span>
                          <span className="text-xs text-gray-500">{review.images.length} photo{review.images.length !== 1 ? 's' : ''}</span>
                        </div>
                        
                        <h3 className="text-lg font-semibold text-gray-900 mb-2">
                          {review.service}
                        </h3>
                        
                        <p className="text-gray-600 mb-3">
                          "{review.text}"
                        </p>
                        
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-2 text-sm text-gray-500">
                            <Calendar className="w-4 h-4" />
                            <span>{review.date}</span>
                            <span>•</span>
                            <span>{review.name}</span>
                          </div>
                          <button
                            onClick={() => openPhotoModal(review)}
                            className="bg-green-700 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-green-800 transition-colors flex items-center space-x-2"
                          >
                            <Eye className="w-4 h-4" />
                            <span>View Photos</span>
                          </button>
                        </div>
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          // No Results
          <Card className="border-0 shadow-lg">
            <CardContent className="p-12 text-center">
              <Filter className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                No Projects Found
              </h3>
              <p className="text-gray-600 mb-4">
                Try adjusting your search terms or filters to see more results.
              </p>
              <button
                onClick={() => {
                  setSearchTerm("");
                  setSelectedService("all");
                  setSelectedLocation("all");
                }}
                className="bg-green-700 text-white px-4 py-2 rounded-md hover:bg-green-800 transition-colors"
              >
                Clear All Filters
              </button>
            </CardContent>
          </Card>
        )}

        {/* Photo Modal */}
        <PhotoModal 
          isOpen={photoModalOpen}
          onClose={closePhotoModal}
          review={modalReview}
        />
      </div>
    </div>
  );
};

export default WorkGallery;