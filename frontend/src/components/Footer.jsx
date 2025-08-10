import React from "react";
import { Phone, Mail, MapPin, Clock } from "lucide-react";

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gray-900 text-white">
      {/* Main Footer Content */}
      <div className="container mx-auto px-4 py-16">
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Company Info */}
          <div className="space-y-6">
            <div className="flex items-center space-x-3">
              <img 
                src="https://customer-assets.emergentagent.com/job_green-thumbs-balham/artifacts/qsdqvwf5_IMG_7243.jpeg" 
                alt="PNM Gardeners Logo" 
                className="h-12 w-12"
              />
              <div>
                <h3 className="text-2xl font-bold text-white">PNM Gardeners</h3>
              </div>
            </div>
            <p className="text-gray-300">
              Your trusted local gardening experts serving Balham and surrounding London areas 
              with professional, reliable gardening services.
            </p>
            
            <div className="space-y-3">
              <div className="flex items-center space-x-3">
                <Phone className="w-5 h-5 text-green-400" />
                <span>020 3488 1912</span>
              </div>
              <div className="flex items-center space-x-3">
                <Mail className="w-5 h-5 text-green-400" />
                <span>info@pnmgardeners.co.uk</span>
              </div>
              <div className="flex items-center space-x-3">
                <MapPin className="w-5 h-5 text-green-400" />
                <span>Balham, London SW12</span>
              </div>
            </div>
          </div>

          {/* Services */}
          <div>
            <h4 className="text-lg font-semibold mb-6">Our Services</h4>
            <ul className="space-y-3 text-gray-300">
              <li><a href="#services" className="hover:text-green-400 transition-colors">Garden Maintenance</a></li>
              <li><a href="#services" className="hover:text-green-400 transition-colors">Lawn Care Services</a></li>
              <li><a href="#services" className="hover:text-green-400 transition-colors">Hedge Trimming</a></li>
              <li><a href="#services" className="hover:text-green-400 transition-colors">Turfing Services</a></li>
              <li><a href="#services" className="hover:text-green-400 transition-colors">Pressure Washing</a></li>
              <li><a href="#services" className="hover:text-green-400 transition-colors">Tree Surgery</a></li>
            </ul>
          </div>

          {/* Areas Served */}
          <div>
            <h4 className="text-lg font-semibold mb-6">Areas We Serve</h4>
            <ul className="space-y-3 text-gray-300">
              <li>Balham</li>
              <li>Tooting</li>
              <li>Wandsworth</li>
              <li>Clapham</li>
              <li>Streatham</li>
              <li>Wimbledon</li>
              <li><a href="#areas" className="text-green-400 hover:text-green-300 transition-colors">View All Areas →</a></li>
            </ul>
          </div>

          {/* Business Hours */}
          <div>
            <h4 className="text-lg font-semibold mb-6">Business Hours</h4>
            <div className="space-y-3 text-gray-300">
              <div className="flex items-start space-x-3">
                <Clock className="w-5 h-5 text-green-400 mt-0.5" />
                <div>
                  <div className="font-medium">Monday - Friday</div>
                  <div>8:00 AM - 6:00 PM</div>
                </div>
              </div>
              <div className="pl-8">
                <div className="font-medium">Saturday</div>
                <div>8:00 AM - 5:00 PM</div>
              </div>
              <div className="pl-8">
                <div className="font-medium">Sunday</div>
                <div>9:00 AM - 4:00 PM</div>
              </div>
            </div>
            
            <div className="mt-6 p-4 bg-green-900 rounded-lg">
              <div className="text-sm">
                <div className="font-semibold text-green-300 mb-1">Emergency Services Available</div>
                <div className="text-gray-300">Call for urgent garden clearance & tree removal</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="border-t border-gray-800">
        <div className="container mx-auto px-4 py-8">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <div className="text-gray-400 text-sm">
              © {currentYear} PNM Gardeners. All rights reserved.
            </div>
            
            <div className="flex items-center space-x-6 text-sm text-gray-400">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                <span>Fully Licensed & Insured</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                <span>Free Quotes</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                <span>Waste Disposal Included</span>
              </div>
            </div>
          </div>

          <div className="mt-6 pt-6 border-t border-gray-800 text-center text-gray-500 text-sm">
            <p>
              Professional gardening services in Balham, London. Specializing in garden maintenance, 
              lawn care, hedge trimming, and complete garden transformations across South London.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;