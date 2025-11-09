import React from "react";
import { areasServed } from "../mock/data";
import { MapPin, Phone, Mail } from "lucide-react";
import { Button } from "./ui/button";
import { Card, CardContent } from "./ui/card";

const AreasServed = () => {
  // Scroll to contact section function
  const scrollToContact = () => {
    const element = document.getElementById('contact');
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section id="areas" className="py-20 bg-gray-50">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl lg:text-5xl font-bold text-gray-900 mb-6">
            We Cover South West London & Surrounding Areas
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            We provide professional gardening services across South West London and the surrounding areas. 
            If your area isn't listed, please contact us - we'd be happy to help!
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Areas List */}
          <div className="lg:col-span-2">
            <Card className="border-0 shadow-lg bg-white">
              <CardContent className="p-8">
                <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
                  <MapPin className="w-6 h-6 text-green-700 mr-2" />
                  Service Areas
                </h3>
                
                <div className="grid md:grid-cols-3 gap-4">
                  {areasServed.map((area, index) => (
                    <div
                      key={index}
                      className="flex items-center space-x-2 p-3 rounded-lg hover:bg-green-50 transition-colors cursor-pointer"
                    >
                      <div className="w-2 h-2 bg-green-700 rounded-full"></div>
                      <span className="text-gray-700 font-medium">{area}</span>
                    </div>
                  ))}
                </div>

                <div className="mt-8 p-6 bg-green-50 rounded-xl">
                  <p className="text-gray-700 leading-relaxed">
                    <strong>Primary Service Area:</strong> South West London, Tooting, Wandsworth, Clapham, Streatham, 
                    and surrounding South London areas. We also serve other London postcodes - 
                    please contact us to confirm coverage for your specific location.
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Contact Card */}
          <div>
            <Card className="border-0 shadow-lg bg-white sticky top-8">
              <CardContent className="p-8">
                <h3 className="text-xl font-bold text-gray-900 mb-6">
                  Get Your Free Quote Today
                </h3>
                
                <div className="space-y-6">
                  <p className="text-gray-600">
                    Hassle-free quoting & booking process for all gardening services in your area.
                  </p>

                  {/* Contact Options */}
                  <div className="space-y-4">
                    <div className="flex items-center space-x-3 p-3 bg-green-50 rounded-lg">
                      <Phone className="w-5 h-5 text-green-700" />
                      <div>
                        <div className="font-medium text-gray-900">Call or WhatsApp</div>
                        <div className="text-green-700 font-semibold">07340 833142</div>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-3 p-3 bg-green-50 rounded-lg">
                      <Mail className="w-5 h-5 text-green-700" />
                      <div>
                        <div className="font-medium text-gray-900">Email with Photos</div>
                        <div className="text-green-700 font-semibold">contact@pnmgardening.com</div>
                      </div>
                    </div>
                  </div>

                  {/* CTA Buttons */}
                  <div className="space-y-3">
                    <Button 
                      onClick={scrollToContact}
                      className="w-full bg-green-700 hover:bg-green-800 text-white"
                    >
                      Get Free Quote Now
                    </Button>
                    <Button 
                      variant="outline" 
                      className="w-full border-green-700 text-green-700 hover:bg-green-700 hover:text-white"
                      onClick={() => window.open('tel:07340833142')}
                    >
                      <Phone className="w-4 h-4 mr-2" />
                      Call Now
                    </Button>
                  </div>

                  {/* Service Promise */}
                  <div className="pt-4 border-t border-gray-200">
                    <div className="grid grid-cols-2 gap-4 text-center">
                      <div>
                        <div className="text-lg font-bold text-green-700">FREE</div>
                        <div className="text-xs text-gray-600">Quotes</div>
                      </div>
                      <div>
                        <div className="text-lg font-bold text-green-700">FAST</div>
                        <div className="text-xs text-gray-600">Response</div>
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </section>
  );
};

export default AreasServed;