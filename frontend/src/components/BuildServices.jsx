import React from "react";
import Header from "./Header";
import Footer from "./Footer";
import { Button } from "./ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { ArrowLeft } from "lucide-react";
import { useNavigate } from "react-router-dom";

const BuildServices = () => {
  const navigate = useNavigate();

  const scrollToContact = () => {
    navigate('/#contact');
    setTimeout(() => {
      const element = document.getElementById('contact');
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
    }, 100);
  };

  const buildServices = [
    {
      id: "hard-landscaping",
      title: "Hard Landscaping",
      description: "Skilled hard landscaping services for all structural elements of your outdoor space. From laying patios and pathways to building walls and fences, we create the durable framework for your perfect garden.",
      image: "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHw1fHxwYXRpb3xlbnwwfHx8fDE3NTQ4Mzc5NDJ8MA&ixlib=rb-4.1.0&q=85",
      features: ["Patio & Paving Installation", "Decking Construction", "Retaining Wall Building", "Fence Installation & Repair", "Shed & Outbuilding Bases"],
    },
    {
      id: "soft-landscaping",
      title: "Soft Landscaping",
      description: "Expert soft landscaping services focusing on the living elements of your garden, including the supply and installation of healthy plants, trees, and shrubs to bring your design to life.",
      image: "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHw2fHxwbGFudGluZ3xlbnwwfHx8fDE3NTQ4Mzc5NDJ8MA&ixlib=rb-4.1.0&q=85",
      features: ["Plant Supply & Installation", "Tree & Shrub Planting", "Border Preparation", "Mulching & Soil Conditioning", "Feature Planting"],
    },
    {
      id: "garden-design",
      title: "Garden Design",
      description: "Professional garden design services to create bespoke, beautiful outdoor spaces. Our experts work with you from concept to final plan to ensure a functional and stunning garden tailored to your needs.",
      image: "https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHwxfHxnYXJkZW4lMjBkZXNpZ258ZW58MHx8fHwxNzU0ODM3OTQyfDA&ixlib=rb-4.1.0&q=85",
      features: ["Site Survey & Analysis", "Concept Development", "2D & 3D Visuals", "Planting Plans", "Lighting & Irrigation Design"],
    },
  ];

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
          
          <h1 className="text-5xl lg:text-6xl font-bold mb-6">
            Build Services
          </h1>
          <p className="text-xl text-white/90 max-w-3xl">
            Bringing bespoke designs to life with precision and quality craftsmanship. 
            From soft planting to hard landscaping, we create beautiful, functional outdoor spaces.
          </p>
        </div>
      </section>

      {/* Services Grid */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {buildServices.map((service) => (
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
                  <Button 
                    onClick={scrollToContact}
                    className="w-full bg-green-700 hover:bg-green-800 text-white"
                  >
                    Book {service.title}
                  </Button>
                </CardFooter>
              </Card>
            ))}
          </div>

          {/* Bottom CTA */}
          <div className="text-center mt-16">
            <div className="bg-green-50 rounded-2xl p-8">
              <h3 className="text-2xl font-bold text-gray-900 mb-4">
                Ready to Build Your Dream Garden?
              </h3>
              <p className="text-gray-600 mb-6">
                Get expert construction and landscaping services with professional results
              </p>
              <Button 
                onClick={scrollToContact}
                className="bg-green-700 hover:bg-green-800 text-white px-8 py-3 text-lg"
              >
                Get A Free Quote
              </Button>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default BuildServices;
