import React from 'react';
import { Phone, Star, Award } from 'lucide-react';
import { Button } from '../components/ui/button';

const HeroSection = () => {
  const scrollToContact = () => {
    const element = document.getElementById('contact');
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section className="relative bg-gradient-to-br from-green-50 via-white to-green-50 pt-24 pb-16 overflow-hidden">
      {/* Decorative elements */}
      <div className="absolute top-0 right-0 w-72 h-72 bg-green-200 rounded-full blur-3xl opacity-20 -z-10"></div>
      <div className="absolute bottom-0 left-0 w-96 h-96 bg-green-300 rounded-full blur-3xl opacity-20 -z-10"></div>
      
      <div className="container mx-auto px-4">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <div className="space-y-6">
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold leading-tight">
              Professional Gardening Services in{' '}
              <span className="text-green-700">South West London</span>
            </h1>
            
            <p className="text-lg text-gray-600 leading-relaxed">
              Transform your outdoor space with expert garden design, maintenance, and landscaping services. 
              From small gardens to large projects, we bring your vision to life.
            </p>

            {/* Trust Indicators */}
            <div className="flex flex-wrap gap-6 py-4">
              <div className="flex items-center gap-2">
                <div className="bg-green-100 p-2 rounded-full">
                  <Star className="w-5 h-5 text-green-700" fill="currentColor" />
                </div>
                <div>
                  <div className="font-semibold text-gray-900">4.9/5 Rating</div>
                  <div className="text-sm text-gray-600">52+ Reviews</div>
                </div>
              </div>
              
              <div className="flex items-center gap-2">
                <div className="bg-green-100 p-2 rounded-full">
                  <Award className="w-5 h-5 text-green-700" />
                </div>
                <div>
                  <div className="font-semibold text-gray-900">Fully Insured</div>
                  <div className="text-sm text-gray-600">Licensed Professionals</div>
                </div>
              </div>
            </div>

            {/* CTA Buttons */}
            <div className="flex flex-wrap gap-4">
              <Button
                onClick={() => window.open('tel:07340833142')}
                className="bg-green-700 hover:bg-green-800 text-white px-8 py-6 text-lg"
              >
                <Phone className="w-5 h-5 mr-2" />
                07340 833142
              </Button>
              <Button
                onClick={scrollToContact}
                variant="outline"
                className="border-green-700 text-green-700 hover:bg-green-50 px-8 py-6 text-lg"
              >
                Get Free Quote
              </Button>
            </div>

            {/* Quick Info */}
            <div className="flex flex-wrap gap-4 pt-4 text-sm text-gray-600">
              <span>✓ Same Day Quotes</span>
              <span>✓ Free Consultations</span>
              <span>✓ No Hidden Costs</span>
            </div>
          </div>

          {/* Right Image */}
          <div className="relative">
            <div className="relative rounded-2xl overflow-hidden shadow-2xl">
              <img
                src="https://customer-assets.emergentagent.com/job_balham-gardening-hub/artifacts/vr6x6qen_27eea371-8cab-4d35-8c18-23b96c7feea6.JPG"
                alt="Beautiful Garden - Professional Landscaping by PNM Gardeners"
                className="w-full h-[500px] object-cover"
              />
              {/* Overlay Badge */}
              <div className="absolute bottom-6 left-6 right-6 bg-white/95 backdrop-blur-sm rounded-xl p-4 shadow-lg">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="text-2xl font-bold text-green-700">10+ Years</div>
                    <div className="text-sm text-gray-600">Professional Experience</div>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold text-green-700">100%</div>
                    <div className="text-sm text-gray-600">Customer Satisfaction</div>
                  </div>
                </div>
              </div>
            </div>
            
            {/* Decorative dot pattern */}
            <div className="absolute -bottom-4 -right-4 w-24 h-24 bg-green-700 rounded-lg -z-10 opacity-20"></div>
            <div className="absolute -top-4 -left-4 w-32 h-32 border-4 border-green-700 rounded-lg -z-10 opacity-20"></div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;