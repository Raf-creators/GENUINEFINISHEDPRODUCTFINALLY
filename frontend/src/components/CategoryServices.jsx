import React, { useState, useEffect } from "react";
import { Button } from "./ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { useNavigate } from "react-router-dom";

const CategoryServices = ({ selectedCategory }) => {
  const navigate = useNavigate();

  const servicesData = {
    design: [
      {
        id: "garden-design-planning",
        title: "Garden Design Planning",
        description: "Comprehensive garden design planning service from initial concept to detailed implementation plans. We work with you to understand your vision and create a bespoke design that maximizes your outdoor space.",
        image: "https://images.unsplash.com/photo-1523726491678-bf852e717f6a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHw1fHxnYXJkZW4lMjBkZXNpZ24lMjBwbGFufGVufDB8fHx8MTc2MTEwNzAwNXww&ixlib=rb-4.1.0&q=85",
        features: ["Site Survey", "Concept Design", "Detailed Plans", "Material Selection", "Budget Planning"],
        hideGallery: true,
      },
      {
        id: "3d-visualization",
        title: "3D Visualization",
        description: "Advanced 3D visualization services to help you see your garden design before construction begins. Realistic renders show exactly how your finished garden will look.",
        image: "https://customer-assets.emergentagent.com/job_garden-reviews-map/artifacts/kzz3i5mi_image.png",
        features: ["3D Renders", "Virtual Walkthrough", "Day/Night Views", "Seasonal Variations", "Material Samples"],
        hideGallery: true,
      },
      {
        id: "planting-schemes",
        title: "Planting Schemes",
        description: "Expert planting scheme design tailored to your garden's conditions and your preferences. We select plants for year-round interest, considering color, texture, and maintenance requirements.",
        image: "https://customer-assets.emergentagent.com/job_garden-reviews-map/artifacts/djp6tot7_WhatsApp%20Image%202025-10-26%20at%2017.40.53_32bd7f7a%20%281%29.jpg",
        features: ["Plant Selection", "Seasonal Planning", "Color Schemes", "Soil Analysis", "Maintenance Guide"],
      },
      {
        id: "outdoor-lighting-design",
        title: "Outdoor Lighting Design",
        description: "Professional outdoor lighting design to enhance your garden's beauty and functionality. Create ambiance, highlight features, and improve safety with expertly placed lighting.",
        image: "https://customer-assets.emergentagent.com/job_garden-reviews-map/artifacts/3wo2r2yj_image.png",
        features: ["Lighting Plans", "Fixture Selection", "Energy Efficiency", "Smart Controls", "Installation"],
        hideGallery: true,
      },
    ],
    build: [
      {
        id: "hard-landscaping",
        title: "Hard Landscaping",
        description: "Skilled hard landscaping services for all structural elements of your outdoor space. From laying patios and pathways to building walls and fences, we create the durable framework for your perfect garden.",
        image: "https://customer-assets.emergentagent.com/job_garden-reviews-map/artifacts/zea9dvxg_image.png",
        features: ["Patio & Paving Installation", "Decking Construction", "Retaining Wall Building", "Fence Installation & Repair", "Shed & Outbuilding Bases"],
      },
      {
        id: "soft-landscaping",
        title: "Soft Landscaping",
        description: "Expert soft landscaping services focusing on the living elements of your garden, including the supply and installation of healthy plants, trees, and shrubs to bring your design to life.",
        image: "https://customer-assets.emergentagent.com/job_garden-reviews-map/artifacts/kp7rfulk_image.png",
        features: ["Plant Supply & Installation", "Tree & Shrub Planting", "Border Preparation", "Mulching & Soil Conditioning", "Feature Planting"],
      },
      {
        id: "fencing-decking-trellis",
        title: "Fences, Decking & Trellis",
        description: "Professional installation of garden fencing, decking, and trellis work. Quality carpentry and construction to enhance your outdoor living space with durable, attractive structures.",
        image: "https://customer-assets.emergentagent.com/job_garden-reviews-map/artifacts/y45z61te_image.png",
        features: ["Garden Fencing", "Decking Installation", "Trellis Work", "Privacy Screens", "Custom Carpentry"],
      },
    ],
    maintain: [
      {
        id: "garden-maintenance",
        title: "Garden Maintenance",
        description: "Comprehensive garden maintenance including lawn mowing, hedge trimming, weeding, and general upkeep. Professional service to keep your garden looking its best all year round.",
        image: "https://customer-assets.emergentagent.com/job_balham-gardening-hub/artifacts/iavpo09s_Garden%20Maintenance.jpeg",
        features: ["Lawn Mowing", "Hedge Trimming", "Weeding", "General Upkeep", "Seasonal Maintenance"],
      },
      {
        id: "garden-clearance",
        title: "Garden Clearance",
        description: "Complete garden clearance services including removal of overgrown vegetation, waste disposal, and site preparation. Fast and efficient clearance with professional waste removal.",
        image: "https://customer-assets.emergentagent.com/job_balham-gardening-hub/artifacts/tu9u2wbq_Garden%20Clearance.jpeg",
        features: ["Overgrown Garden Clearance", "Waste Removal", "Site Preparation", "Ivy Removal", "Thorny Bush Disposal"],
      },
      {
        id: "hedge-trimming",
        title: "Hedge Trimming & Removal",
        description: "Professional hedge trimming and removal services. Expert maintenance to keep your hedges neat and healthy, or complete removal when needed.",
        image: "https://customer-assets.emergentagent.com/job_garden-reviews-map/artifacts/ju1xb2ir_image.png",
        features: ["Hedge Trimming", "Hedge Removal", "Hedge Shaping", "Pruning", "Cleanup Service"],
      },
      {
        id: "turfing",
        title: "Turfing",
        description: "Professional turf laying services to create beautiful, lush lawns. From ground preparation to final installation of premium quality turf.",
        image: "https://customer-assets.emergentagent.com/job_balham-gardening-hub/artifacts/p467qw39_Turfing.jpeg",
        features: ["Ground Preparation", "Turf Installation", "Lawn Creation", "Soil Treatment", "Aftercare Advice"],
      },
    ],
  };

  const services = servicesData[selectedCategory] || [];

  const categoryTitles = {
    design: "Design Services",
    build: "Build Services",
    maintain: "Maintenance Services",
  };

  const categoryDescriptions = {
    design: "Professional garden design services to create bespoke, beautiful outdoor spaces tailored to your vision",
    build: "Expert construction and landscaping services to bring your garden design to life with quality craftsmanship",
    maintain: "Ongoing professional maintenance to keep your garden looking perfect throughout the year",
  };

  return (
    <section id="category-services" className="py-20 bg-white scroll-mt-20">
      <div className="container mx-auto px-4">
        {/* Category Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl lg:text-5xl font-bold text-gray-900 mb-6">
            {categoryTitles[selectedCategory]}
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            {categoryDescriptions[selectedCategory]}
          </p>
        </div>

        {/* Services Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {services.map((service) => (
            <Card key={service.id} className="group hover:shadow-xl transition-all duration-300 border-0 shadow-lg overflow-hidden">
              <div className="relative overflow-hidden">
                <img
                  src={service.image}
                  alt={service.title}
                  className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/30 to-transparent"></div>
              </div>
              
              <CardHeader className="pb-3">
                <CardTitle className="text-xl font-bold text-gray-900 group-hover:text-green-700 transition-colors">
                  {service.title}
                </CardTitle>
                <CardDescription className="text-gray-600 leading-relaxed">
                  {service.description}
                </CardDescription>
              </CardHeader>
              
              <CardContent className="pt-0">
                <div className="space-y-3">
                  <div className="text-sm font-medium text-gray-700 mb-2">Service Includes:</div>
                  <div className="flex flex-wrap gap-2">
                    {service.features.map((feature, index) => (
                      <Badge key={index} variant="outline" className="text-xs border-green-200 text-green-700">
                        {feature}
                      </Badge>
                    ))}
                  </div>
                </div>
              </CardContent>
              
              <CardFooter className="pt-4">
                {!service.hideGallery && (
                  <Button 
                    onClick={() => navigate(`/gallery/${service.id}`)}
                    className="w-full bg-green-700 hover:bg-green-800 text-white"
                  >
                    View Gallery
                  </Button>
                )}
              </CardFooter>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};

export default CategoryServices;
