import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { ArrowLeft, Image as ImageIcon } from "lucide-react";
import Header from './Header';
import Footer from './Footer';

const GalleryHome = () => {
  const navigate = useNavigate();
  const [selectedCategory, setSelectedCategory] = useState(null);

  // Service to gallery ID mapping
  const serviceGalleries = {
    design: [
      { id: "garden-design-planning", name: "Garden Design Planning", image: "https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=400" },
      { id: "3d-visualization", name: "3D Visualization", image: "https://images.unsplash.com/photo-1523726491678-bf852e717f6a?w=400" },
      { id: "planting-schemes", name: "Planting Schemes", image: "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400" },
      { id: "outdoor-lighting-design", name: "Outdoor Lighting Design", image: "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400" },
    ],
    build: [
      { id: "hard-landscaping", name: "Hard Landscaping", image: "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=400" },
      { id: "soft-landscaping", name: "Soft Landscaping", image: "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400" },
      { id: "fencing-decking-trellis", name: "Fences, Decking & Trellis", image: "https://images.unsplash.com/photo-1585128792020-803d29415281?w=400" },
    ],
    maintain: [
      { id: "garden-maintenance", name: "Garden Maintenance", image: "https://customer-assets.emergentagent.com/job_balham-gardening-hub/artifacts/iavpo09s_Garden%20Maintenance.jpeg" },
      { id: "garden-clearance", name: "Garden Clearance", image: "https://customer-assets.emergentagent.com/job_balham-gardening-hub/artifacts/tu9u2wbq_Garden%20Clearance.jpeg" },
      { id: "hedge-trimming", name: "Hedge Trimming & Removal", image: "https://customer-assets.emergentagent.com/job_balham-gardening-hub/artifacts/ccw4wf98_Hedge%20Trimming.jpeg" },
      { id: "turfing", name: "Turfing", image: "https://customer-assets.emergentagent.com/job_balham-gardening-hub/artifacts/p467qw39_Turfing.jpeg" },
    ],
  };

  const categories = [
    {
      id: "design",
      title: "DESIGN",
      description: "Innovative garden design concepts and visualizations",
      image: "https://images.unsplash.com/photo-1523726491678-bf852e717f6a?w=800",
      color: "from-blue-600 to-blue-800"
    },
    {
      id: "build",
      title: "BUILD",
      description: "Construction and landscaping projects brought to life",
      image: "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800",
      color: "from-green-600 to-green-800"
    },
    {
      id: "maintain",
      title: "MAINTAIN",
      description: "Ongoing maintenance and garden care projects",
      image: "https://images.unsplash.com/photo-1592419044706-39796d40f98c?w=800",
      color: "from-emerald-600 to-emerald-800"
    },
  ];

  const handleCategoryClick = (categoryId) => {
    setSelectedCategory(categoryId);
  };

  const handleServiceClick = (serviceId) => {
    navigate(`/gallery/${serviceId}`);
  };

  const handleBackToCategories = () => {
    setSelectedCategory(null);
  };

  const handleBackToHome = () => {
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      {/* Hero Section */}
      <section className="relative py-20 bg-gradient-to-r from-green-800 to-green-600 text-white">
        <div className="container mx-auto px-4">
          <button
            onClick={handleBackToHome}
            className="flex items-center text-white/90 hover:text-white mb-6 transition-colors"
          >
            <ArrowLeft className="w-5 h-5 mr-2" />
            Back to Home
          </button>
          
          <h1 className="text-5xl lg:text-6xl font-bold mb-6">
            {selectedCategory 
              ? `${categories.find(c => c.id === selectedCategory)?.title} Gallery`
              : "Work Gallery"}
          </h1>
          <p className="text-xl text-white/90 max-w-3xl">
            {selectedCategory 
              ? "Browse our portfolio of completed projects in this category"
              : "Explore our portfolio organized by Design, Build, and Maintenance services"}
          </p>
        </div>
      </section>

      {/* Content */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          {!selectedCategory ? (
            /* Category Selection */
            <div className="grid md:grid-cols-3 gap-8 max-w-7xl mx-auto">
              {categories.map((category) => (
                <Card
                  key={category.id}
                  onClick={() => handleCategoryClick(category.id)}
                  className="group cursor-pointer hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 border-0 shadow-xl overflow-hidden"
                >
                  <div className="relative h-64 overflow-hidden">
                    <img
                      src={category.image}
                      alt={category.title}
                      className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                    />
                    <div className={`absolute inset-0 bg-gradient-to-t ${category.color} opacity-60`}></div>
                    
                    <div className="absolute inset-0 flex flex-col justify-end p-6 text-white">
                      <h3 className="text-3xl font-bold mb-2 tracking-wider">
                        {category.title}
                      </h3>
                      <p className="text-base leading-relaxed opacity-90 mb-4">
                        {category.description}
                      </p>
                      
                      <div className="flex items-center text-sm font-semibold group-hover:translate-x-2 transition-transform duration-300">
                        <span>View Services</span>
                        <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                        </svg>
                      </div>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          ) : (
            /* Service Selection within Category */
            <div>
              <button
                onClick={handleBackToCategories}
                className="flex items-center text-gray-600 hover:text-gray-900 mb-8 transition-colors"
              >
                <ArrowLeft className="w-5 h-5 mr-2" />
                Back to Categories
              </button>

              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                {serviceGalleries[selectedCategory].map((service) => (
                  <Card
                    key={service.id}
                    onClick={() => handleServiceClick(service.id)}
                    className="group cursor-pointer hover:shadow-xl transition-all duration-300 border-0 shadow-lg overflow-hidden"
                  >
                    <div className="relative h-48 overflow-hidden">
                      <img
                        src={service.image}
                        alt={service.name}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
                    </div>
                    
                    <CardHeader className="pb-4">
                      <CardTitle className="text-xl font-bold text-gray-900 group-hover:text-green-700 transition-colors">
                        {service.name}
                      </CardTitle>
                    </CardHeader>
                    
                    <CardContent className="pt-0">
                      <Button 
                        className="w-full bg-green-700 hover:bg-green-800 text-white"
                      >
                        <ImageIcon className="w-4 h-4 mr-2" />
                        View Gallery
                      </Button>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          )}
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default GalleryHome;
