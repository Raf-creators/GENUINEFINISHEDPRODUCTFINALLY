import React from "react";
import { Phone, Star, Award } from "lucide-react";
import { Button } from "./ui/button";

const HeroSection = () => {
  // Scroll to contact section function
  const scrollToContact = () => {
    const element = document.getElementById('contact');
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section className="relative bg-gradient-to-br from-green-50 to-green-100 py-20">
      <div className="container mx-auto px-4">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <div className="space-y-8">
            <div className="space-y-4">
              <h1 className="text-5xl lg:text-6xl font-bold text-gray-900 leading-tight">
                Your Local Gardeners In{" "}
                <span className="text-green-700">Balham, London</span>
              </h1>
              <p className="text-xl text-gray-600 leading-relaxed">
                Professional gardening services tailored to meet your specific needs. 
                From regular maintenance to complete garden transformations.
              </p>
            </div>

            {/* Stats */}
            <div className="flex items-center space-x-8">
              <div className="flex items-center space-x-2">
                <div className="flex text-yellow-400">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} className="w-5 h-5 fill-current" />
                  ))}
                </div>
                <span className="font-semibold">4.9/5</span>
              </div>
              <div className="flex items-center space-x-2">
                <Award className="w-5 h-5 text-green-700" />
                <span className="font-semibold">50+ Reviews</span>
              </div>
            </div>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4">
              <Button 
                onClick={scrollToContact}
                className="bg-green-700 hover:bg-green-800 text-white px-8 py-4 text-lg"
              >
                Book Free Quote Today
              </Button>
              <Button 
                variant="outline" 
                className="border-green-700 text-green-700 hover:bg-green-700 hover:text-white px-8 py-4 text-lg"
                onClick={() => window.open('tel:07748853590')}
              >
                <Phone className="w-5 h-5 mr-2" />
                07748 853590
              </Button>
            </div>

            {/* Quick Info */}
            <div className="grid grid-cols-2 gap-6 pt-8">
              <div className="text-center">
                <div className="text-2xl font-bold text-green-700">20+</div>
                <div className="text-sm text-gray-600">Years Experience</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-700">50+</div>
                <div className="text-sm text-gray-600">Happy Customers</div>
              </div>
            </div>
          </div>

          {/* Right Image */}
          <div className="relative">
            <div className="relative rounded-2xl overflow-hidden shadow-2xl">
              <img
                src="https://customer-assets.emergentagent.com/job_balham-gardening-hub/artifacts/vr6x6qen_27eea371-8cab-4d35-8c18-23b96c7feea6.JPG"
                alt="Beautiful Garden in Balham - Professional Landscaping by PNM Gardeners"
                className="w-full h-96 lg:h-[500px] object-cover"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent"></div>
            </div>
            
            {/* Floating Badge */}
            <div className="absolute -bottom-6 -left-6 bg-white p-4 rounded-xl shadow-lg border">
              <div className="text-center">
                <div className="text-2xl font-bold text-green-700">FREE</div>
                <div className="text-sm text-gray-600">No Obligation</div>
                <div className="text-sm text-gray-600">Quotes</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Trust Indicators */}
      <div className="container mx-auto px-4 mt-16">
        <div className="bg-white rounded-2xl shadow-lg p-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-2xl font-bold text-green-700">✓</div>
              <div className="text-sm text-gray-600 mt-2">Fully Licensed & Insured</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-green-700">✓</div>
              <div className="text-sm text-gray-600 mt-2">Free Waste Disposal</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-green-700">✓</div>
              <div className="text-sm text-gray-600 mt-2">All Tools Provided</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-green-700">✓</div>
              <div className="text-sm text-gray-600 mt-2">Same Day Service</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;