import React, { useState, useEffect } from "react";
import Header from "./Header";
import Footer from "./Footer";
import { Button } from "./ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { ArrowLeft, Loader2 } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { apiService, handleApiError } from "../services/api";

const MaintainServices = () => {
  const navigate = useNavigate();
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);

  const scrollToContact = () => {
    navigate('/#contact');
    setTimeout(() => {
      const element = document.getElementById('contact');
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
    }, 100);
  };

  useEffect(() => {
    const fetchServices = async () => {
      try {
        setLoading(true);
        const data = await apiService.getServices();
        
        // Filter only maintenance services
        const maintenanceServiceIds = ['1', '2', '3', '4']; // Garden Maintenance, Garden Clearance, Hedge Trimming, Turfing
        const filteredServices = data.filter(s => maintenanceServiceIds.includes(s.id));
        
        setServices(filteredServices);
      } catch (err) {
        console.error('Failed to fetch services:', err);
        // Fallback data
        setServices([
          {
            id: "1",
            title: "Garden Maintenance",
            description: "Comprehensive garden maintenance including lawn mowing, hedge trimming, weeding, and general upkeep. Professional service to keep your garden looking its best all year round.",
            image: "https://customer-assets.emergentagent.com/job_balham-gardening-hub/artifacts/iavpo09s_Garden%20Maintenance.jpeg",
            features: ["Lawn Mowing", "Hedge Trimming", "Weeding", "General Upkeep", "Seasonal Maintenance"],
          },
          {
            id: "2",
            title: "Garden Clearance",
            description: "Complete garden clearance services including removal of overgrown vegetation, waste disposal, and site preparation. Fast and efficient clearance with professional waste removal.",
            image: "https://customer-assets.emergentagent.com/job_balham-gardening-hub/artifacts/tu9u2wbq_Garden%20Clearance.jpeg",
            features: ["Overgrown Garden Clearance", "Waste Removal", "Site Preparation", "Ivy Removal", "Thorny Bush Disposal"],
          },
          {
            id: "3",
            title: "Hedge Trimming & Removal",
            description: "Professional hedge trimming and removal services. Expert maintenance to keep your hedges neat and healthy, or complete removal when needed.",
            image: "https://customer-assets.emergentagent.com/job_balham-gardening-hub/artifacts/ccw4wf98_Hedge%20Trimming.jpeg",
            features: ["Hedge Trimming", "Hedge Removal", "Hedge Shaping", "Pruning", "Cleanup Service"],
          },
          {
            id: "4",
            title: "Turfing",
            description: "Professional turf laying services to create beautiful, lush lawns. From ground preparation to final installation of premium quality turf.",
            image: "https://customer-assets.emergentagent.com/job_balham-gardening-hub/artifacts/p467qw39_Turfing.jpeg",
            features: ["Ground Preparation", "Turf Installation", "Lawn Creation", "Soil Treatment", "Aftercare Advice"],
          },
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchServices();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-white">
        <Header />
        <div className="flex items-center justify-center min-h-[60vh]">
          <div className="text-center">
            <Loader2 className="w-8 h-8 animate-spin mx-auto text-green-700" />
            <p className="mt-4 text-gray-600">Loading maintenance services...</p>
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
          
          <h1 className="text-5xl lg:text-6xl font-bold mb-6">
            Maintenance Services
          </h1>
          <p className="text-xl text-white/90 max-w-3xl">
            Ongoing expert gardening to keep your outdoor space perfect year-round. 
            Regular maintenance to ensure your garden always looks its best.
          </p>
        </div>
      </section>

      {/* Services Grid */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
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
                Keep Your Garden Perfect Year-Round
              </h3>
              <p className="text-gray-600 mb-6">
                Professional maintenance services to keep your garden healthy and beautiful
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

export default MaintainServices;
