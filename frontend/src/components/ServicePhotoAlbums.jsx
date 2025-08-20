import React, { useState, useEffect } from "react";
import { ArrowLeft, Image as ImageIcon, Eye, ChevronLeft, ChevronRight } from "lucide-react";
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

  // Load real service albums data from Google Drive
  useEffect(() => {
    const fetchRealAlbums = async () => {
      try {
        setLoading(true);
        
        console.log('Loading real Google Drive photos...');
        
        // Try to fetch from the public JSON file first
        try {
          const response = await fetch('/real_gallery_data.json');
          if (response.ok) {
            const realGalleryData = await response.json();
            const albumsArray = Object.values(realGalleryData);
            setAlbums(albumsArray);
            console.log('✅ Loaded real Google Drive photos from static file:', realGalleryData);
            setLoading(false);
            return;
          }
        } catch (staticError) {
          console.warn('Static file not available, trying API...', staticError);
        }
        
        // Fallback to API endpoint
        try {
          const backendUrl = process.env.REACT_APP_BACKEND_URL || import.meta.env.REACT_APP_BACKEND_URL;
          const apiResponse = await fetch(`${backendUrl}/api/gallery/real-photos`);
          
          if (apiResponse.ok) {
            const realGalleryData = await apiResponse.json();
            const albumsArray = Object.values(realGalleryData);
            setAlbums(albumsArray);
            console.log('✅ Loaded real Google Drive photos from API:', realGalleryData);
          } else {
            throw new Error(`API failed with status: ${apiResponse.status}`);
          }
        } catch (apiError) {
          console.error('API also failed:', apiError);
          
          // Final fallback: Use placeholder data with message
          console.log('Using fallback placeholder data...');
          setAlbums([
            {
              service_name: "Photos Loading...",
              photo_count: 0,
              description: "Real Google Drive photos are being loaded. Please refresh the page in a moment.",
              cover_photo: "https://images.unsplash.com/photo-1621460248083-6271cc4437a8?crop=entropy&cs=srgb&fm=jpg&w=800",
              photos: []
            }
          ]);
        }
        
        setLoading(false);
        
      } catch (error) {
        console.error('Error loading real albums:', error);
        setLoading(false);
        
        // Show error state
        setAlbums([
          {
            service_name: "Error Loading Photos",
            photo_count: 0,
            description: "There was an error loading the photo gallery. Please try refreshing the page.",
            cover_photo: "https://images.unsplash.com/photo-1621460248083-6271cc4437a8?crop=entropy&cs=srgb&fm=jpg&w=800",
            photos: []
          }
        ]);
      }
    };

    fetchRealAlbums();
  }, []);

  const openPhotoModal = (photo) => {
    // Create a proper modal photo object with better error handling
    const modalPhotoData = {
      images: [photo.url], // Use the full-size image URL
      service: photo.service || 'Garden Service',
      postcode: "SW12", 
      text: photo.description || `Professional ${photo.service} work`,
      name: "PNM Gardeners", 
      rating: 10,
      date: "Professional Work",
      photoName: photo.name
    };
    
    console.log('Opening photo modal with:', modalPhotoData.images[0]);
    setModalPhoto(modalPhotoData);
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
            <div className="text-xl text-gray-600">Loading real Google Drive photos...</div>
          </div>
        </div>
      </div>
    );
  }

  // Album selection view
  if (!selectedAlbum) {
    const totalPhotos = albums.reduce((total, album) => total + album.photo_count, 0);
    
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
              {totalPhotos} Real Photos from Google Drive • {albums.length} Service Albums
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
                  {/* Cover Photo - Real Google Drive Image */}
                  <div className="aspect-video bg-gray-100 rounded-t-lg overflow-hidden relative">
                    <img
                      src={album.cover_photo}
                      alt={`${album.service_name} gallery`}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                      onError={(e) => {
                        // Fallback if Google Drive image fails to load
                        e.target.src = "https://images.unsplash.com/photo-1621460248083-6271cc4437a8?crop=entropy&cs=srgb&fm=jpg&w=800";
                      }}
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
                        {album.photo_count} Real Photos
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

  // Album photo view - showing real Google Drive photos
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
              {selectedAlbum.photo_count} Real Google Drive Photos
            </div>
          </div>
        </div>

        {/* Photo Grid - Real Google Drive Images */}
        <div className="grid md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 mb-8">
          {currentPhotos.map((photo) => (
            <Card 
              key={photo.id} 
              className="border-0 shadow-md hover:shadow-lg transition-shadow cursor-pointer group"
              onClick={() => openPhotoModal(photo)}
            >
              <CardContent className="p-0">
                <div className="aspect-square bg-gray-100 rounded-lg overflow-hidden relative">
                  <img
                    src={photo.thumbnail_url}
                    alt={photo.name}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    onError={(e) => {
                      // Try the direct URL if thumbnail fails
                      if (e.target.src !== photo.url) {
                        e.target.src = photo.url;
                      } else {
                        // Final fallback
                        e.target.src = "https://images.unsplash.com/photo-1621460248083-6271cc4437a8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzd8MHwxfHNlYXJjaHwxfHxnYXJkZW5pbmd8ZW58MHx8fHwxNzU0ODM3OTM2fDA&ixlib=rb-4.1.0&q=85&w=400&h=400&fit=crop";
                      }
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
            
            {Array.from({ length: Math.min(totalPages, 10) }, (_, i) => {
              const page = i + 1;
              if (totalPages <= 10 || page <= 3 || page >= totalPages - 2 || Math.abs(page - currentPage) <= 1) {
                return (
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
                );
              } else if (page === 4 || page === totalPages - 3) {
                return <span key={page} className="px-2">...</span>;
              }
              return null;
            })}
            
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