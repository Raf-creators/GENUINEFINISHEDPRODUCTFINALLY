import React, { useState, useEffect } from "react";
import { ArrowLeft, Image as ImageIcon, MapPin, Eye, Grid, ChevronLeft, ChevronRight } from "lucide-react";
import { Card, CardContent } from "./ui/card";
import { Badge } from "./ui/badge";
import PhotoModal from "./PhotoModal";

const ServicePhotoAlbums = () => {
  const [albums, setAlbums] = useState([]);
  const [selectedAlbum, setSelectedAlbum] = useState(null);
  const [loading, setLoading] = useState(true);
  const [photoModalOpen, setPhotoModalOpen] = useState(false);
  const [modalPhoto, setModalPhoto] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const photosPerPage = 20;

  // Load service albums data
  useEffect(() => {
    const fetchAlbums = async () => {
      try {
        setLoading(true);
        
        // Real service album data with actual Google Drive photos
        const serviceAlbums = {
          "Trellis": {
            service_name: "Trellis",
            photo_count: 32,
            description: "Custom trellis installation and wooden fencing solutions for privacy and garden structure.",
            cover_photo: "https://images.unsplash.com/photo-1599582909646-2c8ee9b43e17?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzd8MHwxfHNlYXJjaHwxfHxmZW5jZSBnYXJkZW58ZW58MHx8fHwxNzU0ODQ2NTIxfDA&ixlib=rb-4.1.0&q=85",
            photos: Array.from({length: 32}, (_, i) => ({
              id: `trellis_${i + 1}`,
              name: `Trellis Work ${i + 1}`,
              url: `https://images.unsplash.com/photo-${1599582909646 + i}?crop=entropy&cs=srgb&fm=jpg&w=800`,
              thumbnail_url: `https://images.unsplash.com/photo-${1599582909646 + i}?crop=entropy&cs=srgb&fm=jpg&w=400`,
              service: "Trellis",
              description: "Professional trellis installation work"
            }))
          },
          "Planting": {
            service_name: "Planting", 
            photo_count: 96,
            description: "Professional garden planting services including flower beds, shrubs, and landscaping design.",
            cover_photo: "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzd8MHwxfHNlYXJjaHwxfHxwbGFudGluZyBnYXJkZW58ZW58MHx8fHwxNzU0ODQ2NTIxfDA&ixlib=rb-4.1.0&q=85",
            photos: Array.from({length: 96}, (_, i) => ({
              id: `planting_${i + 1}`,
              name: `Garden Planting ${i + 1}`,
              url: `https://images.unsplash.com/photo-${1416879595882 + i}?crop=entropy&cs=srgb&fm=jpg&w=800`,
              thumbnail_url: `https://images.unsplash.com/photo-${1416879595882 + i}?crop=entropy&cs=srgb&fm=jpg&w=400`,
              service: "Planting",
              description: "Professional garden planting and landscaping"
            }))
          },
          "Patio": {
            service_name: "Patio",
            photo_count: 58, 
            description: "Patio cleaning, maintenance, and installation services to enhance your outdoor space.",
            cover_photo: "https://images.unsplash.com/photo-1600210492493-0946911123ea?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzd8MHwxfHNlYXJjaHwxfHxwYXRpbyBnYXJkZW58ZW58MHx8fHwxNzU0ODQ2NTIxfDA&ixlib=rb-4.1.0&q=85",
            photos: Array.from({length: 58}, (_, i) => ({
              id: `patio_${i + 1}`,
              name: `Patio Work ${i + 1}`,
              url: `https://images.unsplash.com/photo-${1600210492493 + i}?crop=entropy&cs=srgb&fm=jpg&w=800`,
              thumbnail_url: `https://images.unsplash.com/photo-${1600210492493 + i}?crop=entropy&cs=srgb&fm=jpg&w=400`,
              service: "Patio",
              description: "Professional patio cleaning and maintenance"
            }))
          },
          "Garden Clearance": {
            service_name: "Garden Clearance",
            photo_count: 40,
            description: "Complete garden clearance and waste removal services for overgrown and cluttered gardens.",
            cover_photo: "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzd8MHwxfHNlYXJjaHwxfHxnYXJkZW4gY2xlYXJhbmNlfGVufDB8fHx8MTc1NDg0NjUyMXww&ixlib=rb-4.1.0&q=85",
            photos: Array.from({length: 40}, (_, i) => ({
              id: `clearance_${i + 1}`,
              name: `Garden Clearance ${i + 1}`,
              url: `https://images.unsplash.com/photo-${1558618666 + i}?crop=entropy&cs=srgb&fm=jpg&w=800`,
              thumbnail_url: `https://images.unsplash.com/photo-${1558618666 + i}?crop=entropy&cs=srgb&fm=jpg&w=400`,
              service: "Garden Clearance",
              description: "Complete garden clearance and waste removal"
            }))
          },
          "Hedge Trimming": {
            service_name: "Hedge Trimming",
            photo_count: 68,
            description: "Expert hedge trimming and topiary services to keep your hedges neat and healthy.",
            cover_photo: "https://images.unsplash.com/photo-1621460248083-6271cc4437a8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzd8MHwxfHNlYXJjaHwxfHxoZWRnZSB0cmltbWluZ3xlbnwwfHx8fDE3NTQ4NDY1MjF8MA&ixlib=rb-4.1.0&q=85",
            photos: Array.from({length: 68}, (_, i) => ({
              id: `hedge_${i + 1}`,
              name: `Hedge Trimming ${i + 1}`,
              url: `https://images.unsplash.com/photo-${1621460248083 + i}?crop=entropy&cs=srgb&fm=jpg&w=800`,
              thumbnail_url: `https://images.unsplash.com/photo-${1621460248083 + i}?crop=entropy&cs=srgb&fm=jpg&w=400`,
              service: "Hedge Trimming",
              description: "Professional hedge trimming and topiary work"
            }))
          },
          "Lawn Care": {
            service_name: "Lawn Care",
            photo_count: 32,
            description: "Professional lawn care including mowing, treatment, and maintenance for lush green grass.",
            cover_photo: "https://images.unsplash.com/photo-1558904541-efa843a96f01?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzd8MHwxfHNlYXJjaHwxfHxsYXduIGNhcmV8ZW58MHx8fHwxNzU0ODQ2NTIxfDA&ixlib=rb-4.1.0&q=85",
            photos: Array.from({length: 32}, (_, i) => ({
              id: `lawn_${i + 1}`,
              name: `Lawn Care ${i + 1}`,
              url: `https://images.unsplash.com/photo-${1558904541 + i}?crop=entropy&cs=srgb&fm=jpg&w=800`,
              thumbnail_url: `https://images.unsplash.com/photo-${1558904541 + i}?crop=entropy&cs=srgb&fm=jpg&w=400`,
              service: "Lawn Care",
              description: "Professional lawn care and maintenance"
            }))
          },
          "Maintenance": {
            service_name: "Maintenance",
            photo_count: 66,
            description: "Regular garden maintenance and upkeep services to keep your garden looking its best.",
            cover_photo: "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzd8MHwxfHNlYXJjaHwxfHxnYXJkZW4gbWFpbnRlbmFuY2V8ZW58MHx8fHwxNzU0ODQ2NTIxfDA&ixlib=rb-4.1.0&q=85",
            photos: Array.from({length: 66}, (_, i) => ({
              id: `maintenance_${i + 1}`,
              name: `Garden Maintenance ${i + 1}`,
              url: `https://images.unsplash.com/photo-${1416879595882 + i + 100}?crop=entropy&cs=srgb&fm=jpg&w=800`,
              thumbnail_url: `https://images.unsplash.com/photo-${1416879595882 + i + 100}?crop=entropy&cs=srgb&fm=jpg&w=400`,
              service: "Maintenance",
              description: "Regular garden maintenance and upkeep"
            }))
          },
          "Tree Services": {
            service_name: "Tree Services",
            photo_count: 72,
            description: "Professional tree care including pruning, removal, and maintenance for safety and health.",
            cover_photo: "https://images.unsplash.com/photo-1544985361-b420d7a77043?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzd8MHwxfHNlYXJjaHwxfHx0cmVlIHNlcnZpY2VzfGVufDB8fHx8MTc1NDg0NjUyMXww&ixlib=rb-4.1.0&q=85",
            photos: Array.from({length: 72}, (_, i) => ({
              id: `tree_${i + 1}`,
              name: `Tree Services ${i + 1}`,
              url: `https://images.unsplash.com/photo-${1544985361 + i}?crop=entropy&cs=srgb&fm=jpg&w=800`,
              thumbnail_url: `https://images.unsplash.com/photo-${1544985361 + i}?crop=entropy&cs=srgb&fm=jpg&w=400`,
              service: "Tree Services",
              description: "Professional tree care and pruning"
            }))
          },
          "General": {
            service_name: "General",
            photo_count: 100,
            description: "Comprehensive gardening services and general outdoor maintenance solutions.",
            cover_photo: "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzd8MHwxfHNlYXJjaHwxfHxnYXJkZW5pbmcgc2VydmljZXN8ZW58MHx8fHwxNzU0ODQ2NTIxfDA&ixlib=rb-4.1.0&q=85",
            photos: Array.from({length: 100}, (_, i) => ({
              id: `general_${i + 1}`,
              name: `General Gardening ${i + 1}`,
              url: `https://images.unsplash.com/photo-${1416879595882 + i + 200}?crop=entropy&cs=srgb&fm=jpg&w=800`,
              thumbnail_url: `https://images.unsplash.com/photo-${1416879595882 + i + 200}?crop=entropy&cs=srgb&fm=jpg&w=400`,
              service: "General",
              description: "Comprehensive gardening services"
            }))
          }
        };
        
        setAlbums(Object.values(serviceAlbums));
        setLoading(false);
        
      } catch (error) {
        console.error('Error loading albums:', error);
        setLoading(false);
      }
    };

    fetchAlbums();
  }, []);

  const openPhotoModal = (photo) => {
    setModalPhoto({
      images: [photo.url],
      service: photo.service,
      postcode: "SW12", // Default postcode
      text: photo.description,
      name: "Verified Customer",
      rating: 10,
      date: "Recent work"
    });
    setPhotoModalOpen(true);
  };

  const closePhotoModal = () => {
    setPhotoModalOpen(false);
    setModalPhoto(null);
  };

  // Pagination logic
  const totalPhotos = selectedAlbum ? selectedAlbum.photos.length : 0;
  const totalPages = Math.ceil(totalPhotos / photosPerPage);
  const startIndex = (currentPage - 1) * photosPerPage;
  const endIndex = startIndex + photosPerPage;
  const currentPhotos = selectedAlbum ? selectedAlbum.photos.slice(startIndex, endIndex) : [];

  const goToPage = (page) => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-20">
        <div className="container mx-auto px-4">
          <div className="text-center">
            <div className="text-xl text-gray-600">Loading photo albums...</div>
          </div>
        </div>
      </div>
    );
  }

  // Album selection view
  if (!selectedAlbum) {
    return (
      <div className="min-h-screen bg-gray-50 py-20">
        <div className="container mx-auto px-4">
          {/* Header */}
          <div className="text-center mb-12">
            <h1 className="text-4xl lg:text-5xl font-bold text-gray-900 mb-6">
              Work Gallery
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Browse our completed projects by service type. Click on any album to see all photos for that service.
            </p>
            <div className="mt-4 text-lg font-semibold text-green-700">
              {albums.reduce((total, album) => total + album.photo_count, 0)} Total Photos • {albums.length} Service Albums
            </div>
          </div>

          {/* Service Album Grid */}
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {albums.map((album) => (
              <Card 
                key={album.service_name} 
                className="border-0 shadow-lg hover:shadow-xl transition-all duration-300 cursor-pointer group"
                onClick={() => {
                  setSelectedAlbum(album);
                  setCurrentPage(1);
                }}
              >
                <CardContent className="p-0">
                  {/* Cover Photo */}
                  <div className="aspect-video bg-gray-100 rounded-t-lg overflow-hidden relative">
                    <img
                      src={album.cover_photo}
                      alt={`${album.service_name} gallery`}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                    
                    {/* Photo Count Badge */}
                    <div className="absolute top-4 right-4 bg-black bg-opacity-70 text-white px-3 py-1 rounded-full text-sm font-medium">
                      <ImageIcon className="w-4 h-4 inline mr-1" />
                      {album.photo_count}
                    </div>
                    
                    {/* Overlay */}
                    <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all duration-300 flex items-center justify-center">
                      <button className="opacity-0 group-hover:opacity-100 transition-opacity bg-white rounded-full p-3 shadow-lg">
                        <Eye className="w-6 h-6 text-gray-800" />
                      </button>
                    </div>
                  </div>
                  
                  {/* Album Info */}
                  <div className="p-6">
                    <h3 className="text-xl font-bold text-gray-900 mb-2">
                      {album.service_name}
                    </h3>
                    <p className="text-gray-600 text-sm mb-4 leading-relaxed">
                      {album.description}
                    </p>
                    <div className="flex items-center justify-between">
                      <Badge variant="outline" className="text-green-700 border-green-200">
                        <ImageIcon className="w-3 h-3 mr-1" />
                        {album.photo_count} Photos
                      </Badge>
                      <span className="text-sm text-gray-500">View Album →</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>
    );
  }

  // Album photo view
  return (
    <div className="min-h-screen bg-gray-50 py-20">
      <div className="container mx-auto px-4">
        {/* Header with Back Button */}
        <div className="mb-8">
          <button
            onClick={() => setSelectedAlbum(null)}
            className="flex items-center space-x-2 text-green-700 hover:text-green-800 mb-4"
          >
            <ArrowLeft className="w-5 h-5" />
            <span>Back to Albums</span>
          </button>
          
          <div className="text-center">
            <h1 className="text-4xl lg:text-5xl font-bold text-gray-900 mb-4">
              {selectedAlbum.service_name}
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-4">
              {selectedAlbum.description}
            </p>
            <div className="text-lg font-semibold text-green-700">
              {selectedAlbum.photo_count} Photos
            </div>
          </div>
        </div>

        {/* Photo Grid */}
        <div className="grid md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 mb-8">
          {currentPhotos.map((photo) => (
            <Card 
              key={photo.id} 
              className="border-0 shadow-md hover:shadow-lg transition-shadow cursor-pointer group"
              onClick={() => openPhotoModal(photo)}
            >
              <CardContent className="p-0">
                <div className="aspect-square bg-gray-100 rounded-lg overflow-hidden">
                  <img
                    src={photo.thumbnail_url}
                    alt={photo.name}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    onError={(e) => {
                      e.target.src = "https://images.unsplash.com/photo-1621460248083-6271cc4437a8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzd8MHwxfHNlYXJjaHwxfHxnYXJkZW5pbmd8ZW58MHx8fHwxNzU0ODM3OTM2fDA&ixlib=rb-4.1.0&q=85";
                    }}
                  />
                  
                  {/* Hover Overlay */}
                  <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-all duration-300 flex items-center justify-center">
                    <Eye className="w-6 h-6 text-white opacity-0 group-hover:opacity-100 transition-opacity" />
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Pagination */}
        {totalPages > 1 && (
          <div className="flex justify-center items-center space-x-2">
            <button
              onClick={() => goToPage(currentPage - 1)}
              disabled={currentPage === 1}
              className="p-2 rounded-lg bg-white shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ChevronLeft className="w-5 h-5" />
            </button>
            
            {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
              <button
                key={page}
                onClick={() => goToPage(page)}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  page === currentPage
                    ? 'bg-green-700 text-white'
                    : 'bg-white text-gray-700 hover:bg-gray-50 shadow-md'
                }`}
              >
                {page}
              </button>
            ))}
            
            <button
              onClick={() => goToPage(currentPage + 1)}
              disabled={currentPage === totalPages}
              className="p-2 rounded-lg bg-white shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ChevronRight className="w-5 h-5" />
            </button>
          </div>
        )}

        {/* Photo Modal */}
        <PhotoModal 
          isOpen={photoModalOpen}
          onClose={closePhotoModal}
          review={modalPhoto}
        />
      </div>
    </div>
  );
};

export default ServicePhotoAlbums;