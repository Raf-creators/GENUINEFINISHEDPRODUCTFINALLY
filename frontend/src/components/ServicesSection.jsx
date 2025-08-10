import React, { useState, useEffect } from "react";
import { apiService, handleApiError } from "../services/api";
import { services as fallbackServices } from "../mock/data";
import { Button } from "./ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { Loader2 } from "lucide-react";

const ServicesSection = () => {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Scroll to contact section function
  const scrollToContact = () => {
    const element = document.getElementById('contact');
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  useEffect(() => {
    const fetchServices = async () => {
      try {
        setLoading(true);
        const data = await apiService.getServices();
        setServices(data);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch services, using fallback data:', err);
        const errorInfo = handleApiError(err);
        setError(errorInfo.message);
        // Use fallback data if API fails
        setServices(fallbackServices);
      } finally {
        setLoading(false);
      }
    };

    fetchServices();
  }, []);

  if (loading) {
    return (
      <section id="services" className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center">
            <Loader2 className="w-8 h-8 animate-spin mx-auto text-green-700" />
            <p className="mt-4 text-gray-600">Loading our services...</p>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section id="services" className="py-20 bg-white">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl lg:text-5xl font-bold text-gray-900 mb-6">
            A Well-Kept Garden — Without Your Time Commitment
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Professional, reliable gardening services in Balham, London. 
            Call us at <span className="font-semibold text-green-700">020 3488 1912</span>. 
            We'll provide fast and free quotes for your requests.
          </p>
          {error && (
            <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg text-sm text-yellow-800">
              ⚠️ Using cached data: {error}
            </div>
          )}
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
              Ready to Transform Your Garden?
            </h3>
            <p className="text-gray-600 mb-6">
              Get your gardening services carried out by professional garden maintenance specialists
            </p>
            <Button className="bg-green-700 hover:bg-green-800 text-white px-8 py-3 text-lg">
              Get A Quote Now
            </Button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ServicesSection;