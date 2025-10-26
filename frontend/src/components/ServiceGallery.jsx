import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import Header from "./Header";
import Footer from "./Footer";
import PhotoModal from "./PhotoModal";
import { Button } from "./ui/button";
import { ArrowLeft, Loader2 } from "lucide-react";

const ServiceGallery = () => {
  const { serviceId } = useParams();
  const navigate = useNavigate();
  const [photos, setPhotos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedPhoto, setSelectedPhoto] = useState(null);
  const [serviceInfo, setServiceInfo] = useState(null);

  // Service information mapping
  const servicesInfo = {
    "garden-design-planning": {
      title: "Garden Design Planning Gallery",
      description: "Explore our portfolio of comprehensive garden design projects, from initial concepts to detailed implementation plans.",
      category: "design",
    },
    "3d-visualization": {
      title: "3D Visualization Gallery",
      description: "View our stunning 3D renders and visualizations that bring garden designs to life before construction begins.",
      category: "design",
    },
    "planting-schemes": {
      title: "Planting Schemes Gallery",
      description: "Discover our expertly designed planting schemes featuring year-round interest and beautiful color combinations.",
      category: "design",
    },
    "outdoor-lighting-design": {
      title: "Outdoor Lighting Design Gallery",
      description: "See how professional lighting design transforms gardens into stunning nighttime landscapes.",
      category: "design",
    },
    "hard-landscaping": {
      title: "Hard Landscaping Gallery",
      description: "Browse our portfolio of patios, pathways, walls, and structural garden features built to last.",
      category: "build",
    },
    "soft-landscaping": {
      title: "Soft Landscaping Gallery",
      description: "View our expert planting work including trees, shrubs, and borders that bring gardens to life.",
      category: "build",
    },
    "fencing-decking-trellis": {
      title: "Fences, Decking & Trellis Gallery",
      description: "Explore our quality carpentry work including fencing, decking, and custom trellis installations.",
      category: "build",
    },
    "garden-maintenance": {
      title: "Garden Maintenance Gallery",
      description: "See the results of our comprehensive garden maintenance services keeping gardens pristine year-round.",
      category: "maintain",
    },
    "garden-clearance": {
      title: "Garden Clearance Gallery",
      description: "Dramatic before and after transformations from our professional garden clearance services.",
      category: "maintain",
    },
    "hedge-trimming": {
      title: "Hedge Trimming & Removal Gallery",
      description: "Professional hedge trimming and removal work showcasing our expertise in hedge care.",
      category: "maintain",
    },
    "turfing": {
      title: "Turfing Gallery",
      description: "Beautiful lawn transformations from our professional turf laying services.",
      category: "maintain",
    },
  };

  useEffect(() => {
    const loadGalleryData = async () => {
      setLoading(true);
      
      // Set service info
      const info = servicesInfo[serviceId] || {
        title: "Service Gallery",
        description: "View our portfolio of completed projects.",
        category: "general",
      };
      setServiceInfo(info);

      try {
        // Try to load from real_gallery_data.json
        const response = await fetch('/real_gallery_data.json');
        const data = await response.json();
        
        // Filter photos for this service
        let servicePhotos = [];
        
        // Map service IDs to album names in the gallery data
        const serviceToAlbumMap = {
          "garden-maintenance": "Garden Maintenance",
          "garden-clearance": "Garden Clearance",
          "hedge-trimming": "Hedge Trimming",
          "turfing": "Turfing",
          "hard-landscaping": "Patio",
          "soft-landscaping": "Planting",
          "fencing-decking-trellis": "Trellis",
          "garden-design-planning": "Planting",
          "3d-visualization": "Planting",
          "planting-schemes": "Planting",
          "outdoor-lighting-design": "Planting",
        };
        
        const albumName = serviceToAlbumMap[serviceId];
        if (albumName && data[albumName]) {
          servicePhotos = data[albumName].photos || [];
        }
        
        // If no photos found, use placeholder
        if (servicePhotos.length === 0) {
          servicePhotos = [
            {
              url: "https://images.unsplash.com/photo-1558904541-efa843a96f01?w=800",
              thumbnail: "https://images.unsplash.com/photo-1558904541-efa843a96f01?w=400",
              caption: "Sample project - More photos coming soon",
            },
          ];
        }
        
        setPhotos(servicePhotos);
      } catch (error) {
        console.error("Error loading gallery:", error);
        // Use placeholder photos
        setPhotos([
          {
            url: "https://images.unsplash.com/photo-1558904541-efa843a96f01?w=800",
            thumbnail: "https://images.unsplash.com/photo-1558904541-efa843a96f01?w=400",
            caption: "Sample project",
          },
        ]);
      } finally {
        setLoading(false);
      }
    };

    loadGalleryData();
  }, [serviceId]);

  const scrollToContact = () => {
    navigate('/#contact');
    setTimeout(() => {
      const element = document.getElementById('contact');
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
    }, 100);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-white">
        <Header />
        <div className="flex items-center justify-center min-h-[60vh]">
          <div className="text-center">
            <Loader2 className="w-8 h-8 animate-spin mx-auto text-green-700" />
            <p className="mt-4 text-gray-600">Loading gallery...</p>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white">
      <Header />
      
      {/* Hero Section */}
      <section className="relative py-20 bg-gradient-to-r from-green-800 to-green-600 text-white">
        <div className="container mx-auto px-4">
          <button
            onClick={() => navigate('/')}
            className="flex items-center text-white/90 hover:text-white mb-6 transition-colors"
          >
            <ArrowLeft className="w-5 h-5 mr-2" />
            Back to Home
          </button>
          
          <h1 className="text-4xl lg:text-5xl font-bold mb-6">
            {serviceInfo?.title}
          </h1>
          <p className="text-xl text-white/90 max-w-3xl mb-8">
            {serviceInfo?.description}
          </p>
          
          <Button 
            onClick={scrollToContact}
            className="bg-white text-green-700 hover:bg-gray-100 px-8 py-3 text-lg font-semibold"
          >
            Book This Service
          </Button>
        </div>
      </section>

      {/* Gallery Grid */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {photos.map((photo, index) => (
              <div
                key={index}
                className="relative overflow-hidden rounded-lg shadow-md hover:shadow-xl transition-all duration-300 cursor-pointer group aspect-square"
                onClick={() => setSelectedPhoto({ ...photo, index })}
              >
                <img
                  src={photo.thumbnail || photo.url}
                  alt={photo.caption || `Photo ${index + 1}`}
                  className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                  loading="lazy"
                />
                <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors duration-300" />
              </div>
            ))}
          </div>

          {/* CTA Section */}
          <div className="text-center mt-16">
            <div className="bg-white rounded-2xl p-8 shadow-lg max-w-2xl mx-auto">
              <h3 className="text-2xl font-bold text-gray-900 mb-4">
                Ready to Transform Your Garden?
              </h3>
              <p className="text-gray-600 mb-6">
                Get in touch for a free consultation and quote for your project
              </p>
              <Button 
                onClick={scrollToContact}
                className="bg-green-700 hover:bg-green-800 text-white px-8 py-3 text-lg"
              >
                Request A Quote
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Photo Modal */}
      {selectedPhoto && (
        <PhotoModal
          photo={selectedPhoto}
          onClose={() => setSelectedPhoto(null)}
          allPhotos={photos}
          currentIndex={selectedPhoto.index}
        />
      )}

      <Footer />
    </div>
  );
};

export default ServiceGallery;
